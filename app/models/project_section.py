from app.extensions import db

SECTION_TYPES = [
    ("text",     "Text / paragraph"),
    ("features", "Feature list"),
    ("image",    "Image"),
    ("code",     "Code snippet"),
]


class ProjectSection(db.Model):
    __tablename__ = "project_sections"

    id           = db.Column(db.Integer, primary_key=True)
    project_id   = db.Column(
        db.Integer,
        db.ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    heading      = db.Column(db.String(128), nullable=True)
    body         = db.Column(db.Text, nullable=False, default="")
    section_type = db.Column(db.String(32), nullable=False, default="text")
    # type-specific: code language (e.g. "python") or image caption
    meta         = db.Column(db.String(128), nullable=True)
    order        = db.Column(db.Integer, nullable=False, default=0)

    project = db.relationship("Project", back_populates="sections")

    def __repr__(self) -> str:
        return f"<ProjectSection {self.section_type} #{self.order} project={self.project_id}>"
