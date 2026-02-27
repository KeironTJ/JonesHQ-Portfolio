from datetime import datetime

from app.extensions import db


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    slug = db.Column(db.String(128), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    # Comma-separated tag string, e.g. "Python, Flask, Bootstrap"
    tags = db.Column(db.String(256), nullable=False, default="")
    icon = db.Column(db.String(64), nullable=False, default="bi-code-square")
    url = db.Column(db.String(256), nullable=True)
    repo_url = db.Column(db.String(256), nullable=True)
    # Lower number = displayed first
    order = db.Column(db.Integer, nullable=False, default=0)
    is_visible = db.Column(db.Boolean, nullable=False, default=True)
    # Status: planning | in_development | live | parked | archived
    status = db.Column(db.String(32), nullable=False, default="in_development")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    sections = db.relationship(
        "ProjectSection",
        back_populates="project",
        order_by="ProjectSection.order",
        cascade="all, delete-orphan",
    )

    @property
    def tags_list(self) -> list[str]:
        """Return tags as a list, splitting on commas."""
        return [t.strip() for t in self.tags.split(",") if t.strip()]

    def __repr__(self) -> str:
        return f"<Project {self.slug}>"
