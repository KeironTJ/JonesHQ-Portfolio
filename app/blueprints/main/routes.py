from flask import render_template

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
