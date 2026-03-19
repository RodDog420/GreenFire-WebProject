from flask import Blueprint, render_template
from flask_login import login_required

admin_bp = Blueprint('admin', __name__)


# ==========================================================================
# ADMIN — all routes protected by login_required at blueprint level
# Add admin-only check to every route here
# ==========================================================================

@admin_bp.route('/')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')