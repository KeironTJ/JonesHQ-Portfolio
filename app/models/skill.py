from app.extensions import db


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    icon = db.Column(db.String(64), nullable=True)       # Bootstrap Icons class, e.g. bi-python
    category = db.Column(db.String(64), nullable=True)   # Optional grouping label
    order = db.Column(db.Integer, nullable=False, default=0)
    is_visible = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self) -> str:
        return f"<Skill {self.name!r}>"
