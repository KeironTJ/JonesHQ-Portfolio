from functools import wraps

from flask import abort, render_template
from flask_login import current_user, login_required

from . import admin_bp


def admin_required(f):
    """Decorator: requires login AND is_admin flag."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    return render_template("admin/dashboard.html")
