from flask import render_template

from . import main_bp

# Placeholder project data — replace with DB queries once Project model is added.
PROJECTS = [
    {
        "title": "Project One",
        "slug": "project-one",
        "description": "A short description of what this project does and why it matters.",
        "tags": ["Python", "Flask"],
        "url": "#",
        "repo_url": "#",
    },
    {
        "title": "Project Two",
        "slug": "project-two",
        "description": "A short description of what this project does and why it matters.",
        "tags": ["JavaScript", "API"],
        "url": "#",
        "repo_url": "#",
    },
]


@main_bp.route("/")
def index():
    return render_template("main/index.html", projects=PROJECTS)
