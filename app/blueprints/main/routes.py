from flask import abort, render_template
from flask_login import current_user

from app.models.project import Project
from app.models.skill import Skill

from . import main_bp


def _section_form():
    """Return a ProjectSectionForm only when needed (avoids circular import at module level)."""
    from app.blueprints.admin.forms import ProjectSectionForm
    return ProjectSectionForm()


@main_bp.route("/")
def index():
    projects = (
        Project.query
        .filter_by(is_visible=True)
        .order_by(Project.order, Project.created_at)
        .all()
    )
    skills = (
        Skill.query
        .filter_by(is_visible=True)
        .order_by(Skill.category, Skill.order, Skill.name)
        .all()
    )
    return render_template("main/index.html", projects=projects, skills=skills)


@main_bp.route("/projects/<slug>")
def project_detail(slug):
    project = Project.query.filter_by(slug=slug).first_or_404()
    # Hidden projects: 404 for guests; admins can preview
    if not project.is_visible and not current_user.is_authenticated:
        abort(404)
    section_form = _section_form() if current_user.is_authenticated else None
    return render_template("main/project_detail.html", project=project, section_form=section_form)
