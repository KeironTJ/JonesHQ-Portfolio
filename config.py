import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-key-change-in-production"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "app", "static", "uploads")
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB file upload limit

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DEV_DATABASE_URL") or "sqlite:///dev.db"
    )


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True

    # Heroku-style postgres:// -> postgresql:// fix
    _db_url = os.environ.get("DATABASE_URL") or ""
    SQLALCHEMY_DATABASE_URI = (
        _db_url.replace("postgres://", "postgresql://", 1)
        if _db_url.startswith("postgres://")
        else _db_url
    )

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        # Log to stderr in production
        import logging
        from logging import StreamHandler

        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
