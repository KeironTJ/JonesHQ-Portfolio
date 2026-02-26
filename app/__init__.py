import click
import mistune
from flask import Flask
from flask.cli import with_appcontext

from config import config

from .errors import register_error_handlers
from .extensions import csrf, db, login_manager, migrate


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Blueprints
    from .blueprints.auth import auth_bp
    from .blueprints.main import main_bp
    from .blueprints.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    # Markdown filter (escape=True prevents XSS from user-supplied HTML)
    _md = mistune.create_markdown(escape=True, plugins=["strikethrough"])

    @app.template_filter("markdown")
    def markdown_filter(text: str) -> str:
        return _md(text or "")

    # Error handlers
    register_error_handlers(app)

    # Template context processors
    @app.context_processor
    def inject_globals():
        from datetime import datetime
        from sqlalchemy.exc import OperationalError
        from .models.settings import SiteSettings
        try:
            site_settings = SiteSettings.get()
        except OperationalError:
            # DB not yet migrated — return defaults so templates don't break
            site_settings = SiteSettings()
        return {"now": datetime.utcnow(), "settings": site_settings}

    # CLI commands
    app.cli.add_command(create_admin_command)

    return app


# ── CLI commands ──────────────────────────────────────────────────────────────

@click.command("create-admin")
@click.argument("username")
@click.argument("password")
@with_appcontext
def create_admin_command(username: str, password: str):
    """Create (or reset) the admin user account."""
    from .models.user import User

    user = User.query.filter_by(username=username).first()
    if user:
        user.set_password(password)
        click.echo(f"Password updated for existing user '{username}'.")
    else:
        user = User(username=username, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        click.echo(f"Admin user '{username}' created.")

    db.session.commit()
