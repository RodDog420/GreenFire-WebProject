from functools import wraps
from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__)


def require_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            if role == 'admin' and not current_user.is_admin:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ==========================================================================
# ADMIN — all routes require both @login_required and @require_role('admin')
# ==========================================================================

@admin_bp.route('/')
@login_required
@require_role('admin')
def dashboard():
    return render_template('admin/dashboard.html')