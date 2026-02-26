from flask import abort, render_template
from flask_login import current_user

from app.models.project import Project

from . import main_bp


@main_bp.route("/")
def index():
    projects = (
        Project.query
        .filter_by(is_visible=True)
        .order_by(Project.order, Project.created_at)
        .all()
    )
    return render_template("main/index.html", projects=projects)


@main_bp.route("/projects/<slug>")
def project_detail(slug):
    project = Project.query.filter_by(slug=slug).first_or_404()
    # Hidden projects: 404 for guests; admins can preview
    if not project.is_visible and not current_user.is_authenticated:
        abort(404)
    return render_template("main/project_detail.html", project=project)
