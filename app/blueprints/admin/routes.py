from functools import wraps

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models.project import Project
from app.models.settings import SiteSettings

from . import admin_bp
from .forms import ProjectForm, SettingsForm


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
            return render_template("admin/project_form.html", form=form, project=None)

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
        )
        db.session.add(project)
        db.session.commit()
        flash(f"Project '{project.title}' created.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/project_form.html", form=form, project=None)


# ── Edit project ──────────────────────────────────────────────────────────────

@admin_bp.route("/projects/<int:id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def project_edit(id):
    project = db.get_or_404(Project, id)
    form = ProjectForm(obj=project)

    if form.validate_on_submit():
        existing = Project.query.filter_by(slug=form.slug.data).first()
        if existing and existing.id != project.id:
            form.slug.errors.append("This slug is already in use.")
            return render_template("admin/project_form.html", form=form, project=project)

        project.title = form.title.data
        project.slug = form.slug.data
        project.description = form.description.data
        project.tags = form.tags.data or ""
        project.icon = form.icon.data or "bi-code-square"
        project.url = form.url.data or None
        project.repo_url = form.repo_url.data or None
        project.order = form.order.data if form.order.data is not None else 0
        project.is_visible = form.is_visible.data
        db.session.commit()
        flash(f"Project '{project.title}' updated.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/project_form.html", form=form, project=project)


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


# ── Site settings ─────────────────────────────────────────────────────────────

@admin_bp.route("/settings", methods=["GET", "POST"])
@login_required
@admin_required
def settings():
    site_settings = SiteSettings.get()
    form = SettingsForm(obj=site_settings)

    if form.validate_on_submit():
        site_settings.display_name = form.display_name.data
        site_settings.bio = form.bio.data
        site_settings.github_url = form.github_url.data or None
        site_settings.linkedin_url = form.linkedin_url.data or None
        site_settings.twitter_url = form.twitter_url.data or None
        db.session.commit()
        flash("Settings saved.", "success")
        return redirect(url_for("admin.settings"))

    return render_template("admin/settings.html", form=form)
