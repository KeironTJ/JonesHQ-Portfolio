import os
import uuid
from functools import wraps

from flask import abort, current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models.project import Project
from app.models.project_section import ProjectSection
from app.models.settings import SiteSettings

from . import admin_bp
from .forms import ProjectForm, ProjectSectionForm, SettingsForm

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "svg"}


def _save_upload(file) -> str | None:
    """Save an uploaded image file; return the static URL path or None."""
    if not file or not file.filename:
        return None
    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return None
    filename = f"{uuid.uuid4().hex}.{ext}"
    dest = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(dest)
    return f"/static/uploads/{filename}"


def admin_required(f):
    """Decorator: requires login AND is_admin flag."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated


# ── Dashboard ─────────────────────────────────────────────────────────────────

@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    projects = Project.query.order_by(Project.order, Project.created_at).all()
    return render_template("admin/dashboard.html", projects=projects)


# ── Add project ───────────────────────────────────────────────────────────────

@admin_bp.route("/projects/new", methods=["GET", "POST"])
@login_required
@admin_required
def project_new():
    form = ProjectForm()
    if form.validate_on_submit():
        if Project.query.filter_by(slug=form.slug.data).first():
            form.slug.errors.append("This slug is already in use.")
            return render_template("admin/project_form.html", form=form, project=None, section_form=None)

        project = Project(
            title=form.title.data,
            slug=form.slug.data,
            description=form.description.data,
            tags=form.tags.data or "",
            icon=form.icon.data or "bi-code-square",
            url=form.url.data or None,
            repo_url=form.repo_url.data or None,
            order=form.order.data if form.order.data is not None else 0,
            is_visible=form.is_visible.data,
            status=form.status.data,
        )
        db.session.add(project)
        db.session.commit()
        flash(f"Project '{project.title}' created. You can now add sections.", "success")
        return redirect(url_for("admin.project_edit", id=project.id))

    return render_template("admin/project_form.html", form=form, project=None, section_form=None)


# ── Edit project ──────────────────────────────────────────────────────────────

@admin_bp.route("/projects/<int:id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def project_edit(id):
    project = db.get_or_404(Project, id)
    form = ProjectForm(obj=project)
    section_form = ProjectSectionForm()

    if form.validate_on_submit():
        existing = Project.query.filter_by(slug=form.slug.data).first()
        if existing and existing.id != project.id:
            form.slug.errors.append("This slug is already in use.")
            return render_template("admin/project_form.html", form=form, project=project,
                                   section_form=section_form)

        project.title = form.title.data
        project.slug = form.slug.data
        project.description = form.description.data
        project.tags = form.tags.data or ""
        project.icon = form.icon.data or "bi-code-square"
        project.url = form.url.data or None
        project.repo_url = form.repo_url.data or None
        project.order = form.order.data if form.order.data is not None else 0
        project.is_visible = form.is_visible.data
        project.status = form.status.data
        db.session.commit()
        flash(f"Project '{project.title}' updated.", "success")
        return redirect(url_for("admin.project_edit", id=project.id))

    return render_template("admin/project_form.html", form=form, project=project,
                           section_form=section_form)


# ── Delete project ────────────────────────────────────────────────────────────

@admin_bp.route("/projects/<int:id>/delete", methods=["POST"])
@login_required
@admin_required
def project_delete(id):
    project = db.get_or_404(Project, id)
    title = project.title
    db.session.delete(project)
    db.session.commit()
    flash(f"Project '{title}' deleted.", "info")
    return redirect(url_for("admin.dashboard"))


# ── Toggle visibility ─────────────────────────────────────────────────────────

@admin_bp.route("/projects/<int:id>/toggle", methods=["POST"])
@login_required
@admin_required
def project_toggle(id):
    project = db.get_or_404(Project, id)
    project.is_visible = not project.is_visible
    db.session.commit()
    return redirect(url_for("admin.dashboard"))


# ── Project sections ──────────────────────────────────────────────────────────

@admin_bp.route("/projects/<int:id>/sections/add", methods=["POST"])
@login_required
@admin_required
def section_add(id):
    from flask import request
    project = db.get_or_404(Project, id)
    form = ProjectSectionForm()
    next_url = request.form.get("next") or url_for("admin.project_edit", id=id)
    if form.validate_on_submit():
        body = form.body.data
        # For image sections, a file upload overrides the URL body field
        if form.section_type.data == "image":
            uploaded = _save_upload(request.files.get("image_file"))
            if uploaded:
                body = uploaded
        max_order = db.session.query(db.func.max(ProjectSection.order)).filter_by(project_id=id).scalar() or -1
        section = ProjectSection(
            project_id=project.id,
            heading=form.heading.data or None,
            body=body,
            section_type=form.section_type.data,
            meta=form.extra.data or None,
            order=max_order + 1,
        )
        db.session.add(section)
        db.session.commit()
        flash("Section added.", "success")
    else:
        for field_errors in form.errors.values():
            for error in field_errors:
                flash(error, "danger")
    return redirect(next_url)


@admin_bp.route("/sections/<int:sid>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def section_edit(sid):
    from flask import request
    section = db.get_or_404(ProjectSection, sid)
    form = ProjectSectionForm(obj=section)
    next_url = request.args.get("next") or request.form.get("next") or url_for("admin.project_edit", id=section.project_id)
    # `meta` DB column → `extra` form field (name differs to avoid WTForms reserved word)
    if not form.is_submitted():
        form.extra.data = section.meta
    if form.validate_on_submit():
        body = form.body.data
        if form.section_type.data == "image":
            uploaded = _save_upload(request.files.get("image_file"))
            if uploaded:
                body = uploaded
        section.heading = form.heading.data or None
        section.body = body
        section.section_type = form.section_type.data
        section.meta = form.extra.data or None
        db.session.commit()
        flash("Section updated.", "success")
        return redirect(next_url)
    return render_template("admin/section_form.html", form=form, section=section, next_url=next_url)


@admin_bp.route("/sections/<int:sid>/delete", methods=["POST"])
@login_required
@admin_required
def section_delete(sid):
    from flask import request
    section = db.get_or_404(ProjectSection, sid)
    project_id = section.project_id
    next_url = request.form.get("next") or url_for("admin.project_edit", id=project_id)
    db.session.delete(section)
    db.session.commit()
    flash("Section deleted.", "info")
    return redirect(next_url)


@admin_bp.route("/sections/<int:sid>/move", methods=["POST"])
@login_required
@admin_required
def section_move(sid):
    from flask import request
    section = db.get_or_404(ProjectSection, sid)
    next_url = request.form.get("next") or url_for("admin.project_edit", id=section.project_id)
    direction = request.form.get("direction")  # "up" or "down"
    siblings = (
        ProjectSection.query
        .filter_by(project_id=section.project_id)
        .order_by(ProjectSection.order)
        .all()
    )
    idx = next((i for i, s in enumerate(siblings) if s.id == section.id), None)
    if idx is None:
        return redirect(url_for("admin.project_edit", id=section.project_id))

    swap_idx = idx - 1 if direction == "up" else idx + 1
    if 0 <= swap_idx < len(siblings):
        # Swap order values
        siblings[idx].order, siblings[swap_idx].order = siblings[swap_idx].order, siblings[idx].order
        db.session.commit()
    return redirect(next_url)


# ── Site settings ─────────────────────────────────────────────────────────────

@admin_bp.route("/settings", methods=["GET", "POST"])
@login_required
@admin_required
def settings():
    site_settings = SiteSettings.get()
    form = SettingsForm(obj=site_settings)

    if form.validate_on_submit():
        site_settings.display_name = form.display_name.data
        site_settings.tagline = form.tagline.data
        site_settings.bio = form.bio.data
        site_settings.github_url = form.github_url.data or None
        site_settings.linkedin_url = form.linkedin_url.data or None
        site_settings.twitter_url = form.twitter_url.data or None
        db.session.commit()
        flash("Settings saved.", "success")
        return redirect(url_for("admin.settings"))

    return render_template("admin/settings.html", form=form)
