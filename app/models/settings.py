from app.extensions import db


class SiteSettings(db.Model):
    """
    Singleton settings row — always exactly one record.
    Use SiteSettings.get() to retrieve (creates defaults on first call).
    """
    __tablename__ = "site_settings"

    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(128), nullable=False, default="Keiron Jones")
    tagline = db.Column(
        db.String(256),
        nullable=False,
        default="Production Planning Manager, developer, and lifelong problem solver.",
    )
    bio = db.Column(
        db.Text,
        nullable=False,
        default=(
            "A collection of personal projects spanning web development, data, and "
            "automation. Built for learning, built for use."
        ),
    )
    github_url = db.Column(db.String(256), nullable=True)
    linkedin_url = db.Column(db.String(256), nullable=True)
    twitter_url = db.Column(db.String(256), nullable=True)
    contact_email = db.Column(db.String(256), nullable=True)
    skills_heading = db.Column(db.String(128), nullable=True, default="Skills")

    @classmethod
    def get(cls) -> "SiteSettings":
        """Return the singleton row, creating it with defaults if absent."""
        instance = cls.query.first()
        if instance is None:
            instance = cls()
            db.session.add(instance)
            db.session.commit()
        return instance

    def __repr__(self) -> str:
        return f"<SiteSettings id={self.id}>"
