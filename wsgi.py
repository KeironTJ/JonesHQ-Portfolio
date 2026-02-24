"""
WSGI entry point for production servers (Gunicorn, uWSGI, etc.).

Example Gunicorn command:
    gunicorn wsgi:app --bind 0.0.0.0:8000 --workers 4

Set environment variables before running:
    export FLASK_CONFIG=production
    export SECRET_KEY=<your-secret>
    export DATABASE_URL=<your-db-url>
"""
import os
from app import create_app

app = create_app(os.environ.get("FLASK_CONFIG", "production"))
