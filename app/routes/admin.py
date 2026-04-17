import os
import json
from functools import wraps
from flask import (
    Blueprint, render_template, abort, redirect,
    url_for, flash, request, current_app,
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from app.models import Product, ProductImage

admin_bp = Blueprint('admin', __name__)

_ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}


# ==========================================================================
# AUTH DECORATOR
# ==========================================================================

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
# HELPERS
# ==========================================================================

def _parse_price(value):
    """Convert dollar string from form to cents integer."""
    try:
        return max(0, int(round(float(
            str(value).replace(',', '').strip()
        ) * 100)))
    except (ValueError, TypeError):
        return 0


def _parse_list_field(value):
    """Convert comma-separated string to JSON, or None if empty."""
    if not value:
        return None
    items = [v.strip() for v in value.split(',') if v.strip()]
    return json.dumps(items) if items else None


def _apply_form(product, form):
    """Write parsed form values onto a Product instance."""
    product.name             = form.get('name', '').strip()
    product.description      = form.get('description', '').strip()
    product.product_type     = form.get('product_type', '').strip()
    product.subcategory      = form.get('subcategory', '').strip() or None
    product.price_cents      = _parse_price(form.get('price_dollars', '0'))
    product.credit_label     = form.get('credit_label', '').strip() or None
    product.credit           = form.get('credit', '').strip() or None
    product.instagram        = form.get('instagram', '').strip() or None
    product.technique        = form.get('technique', '').strip() or None
    product.height           = form.get('height', '').strip() or None
    product.joint_size       = form.get('joint_size', '').strip() or None
    product.series           = form.get('series', '').strip() or None
    product.glass_color      = form.get('glass_color', '').strip() or None
    product.glass_color_company = form.get('glass_color_company', '').strip() or None
    product.collab           = form.get('collab', '').strip() or None
    product.perc             = form.get('perc', '').strip() or None
    product.includes         = form.get('includes', '').strip() or None
    product.metal_type       = form.get('metal_type', '').strip() or None
    product.meta_description = form.get('meta_description', '').strip() or None
    product.acquisition_type = form.get('acquisition_type', 'outright')
    product.gemstones        = 'gemstones'   in form
    product.electroform      = 'electroform' in form
    product.fume             = 'fume'        in form
    product.reclaimer        = 'reclaimer'   in form
    product.is_premium       = 'is_premium'  in form
    product.is_active        = 'is_active'   in form
    product.is_sold          = 'is_sold'     in form
    product.variants_json    = _parse_list_field(form.get('variants', ''))
    product.attributes_json  = _parse_list_field(form.get('attributes', ''))

    rate = form.get('consignment_rate', '').strip()
    product.consignment_rate = float(rate) if rate else None


def _save_images(product, files):
    """
    Save uploaded image files to static/images/products/<slug>/ and
    create ProductImage records. Updates product.primary_image.
    """
    valid = [f for f in files if f and f.filename]
    if not valid:
        return

    upload_dir = os.path.join(
        current_app.root_path, 'static', 'images', 'products', product.slug
    )
    os.makedirs(upload_dir, exist_ok=True)

    existing_count = ProductImage.query.filter_by(
        product_id=product.id
    ).count()

    for i, file in enumerate(valid):
        ext = os.path.splitext(secure_filename(file.filename))[1].lower()
        if ext not in _ALLOWED_EXTENSIONS:
            continue
        sort_order = existing_count + i
        filename   = f'{product.slug}_{sort_order + 1}{ext}'
        file.save(os.path.join(upload_dir, filename))
        db.session.add(ProductImage(
            product_id=product.id,
            image_url=f'images/products/{product.slug}/{filename}',
            alt_text=product.name,
            sort_order=sort_order,
        ))

    db.session.flush()
    first = (ProductImage.query
             .filter_by(product_id=product.id)
             .order_by(ProductImage.sort_order)
             .first())
    if first:
        product.primary_image = first.image_url


# ==========================================================================
# DASHBOARD
# ==========================================================================

@admin_bp.route('/')
@login_required
@require_role('admin')
def dashboard():
    product_count = Product.query.count()
    active_count  = Product.query.filter_by(is_active=True, is_sold=False).count()
    sold_count    = Product.query.filter_by(is_sold=True).count()
    return render_template(
        'admin_dashboard.html',
        product_count=product_count,
        active_count=active_count,
        sold_count=sold_count,
    )


# ==========================================================================
# PRODUCT LIST
# ==========================================================================

@admin_bp.route('/products')
@login_required
@require_role('admin')
def products():
    all_products = (Product.query
                    .order_by(Product.product_type, Product.name)
                    .all())
    return render_template('admin_products.html', products=all_products)


# ==========================================================================
# ADD PRODUCT
# ==========================================================================

@admin_bp.route('/products/new', methods=['GET', 'POST'])
@login_required
@require_role('admin')
def product_new():
    if request.method == 'POST':
        slug = request.form.get('slug', '').strip()
        name = request.form.get('name', '').strip()

        if not name or not slug:
            flash('Name and slug are required.', 'error')
            return render_template('admin_product_form.html', product=None)

        if Product.query.filter_by(slug=slug).first():
            flash(f'Slug "{slug}" is already in use. Choose a different slug.', 'error')
            return render_template('admin_product_form.html', product=None)

        product = Product(slug=slug)
        _apply_form(product, request.form)
        db.session.add(product)
        db.session.flush()

        _save_images(product, request.files.getlist('images'))
        db.session.commit()

        flash(f'"{product.name}" added.', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin_product_form.html', product=None)


# ==========================================================================
# EDIT PRODUCT
# ==========================================================================

@admin_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@require_role('admin')
def product_edit(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        _apply_form(product, request.form)
        _save_images(product, request.files.getlist('images'))
        db.session.commit()
        flash(f'"{product.name}" updated.', 'success')
        return redirect(url_for('admin.products'))

    existing_images = (ProductImage.query
                       .filter_by(product_id=product.id)
                       .order_by(ProductImage.sort_order)
                       .all())
    return render_template(
        'admin_product_form.html',
        product=product,
        existing_images=existing_images,
    )


# ==========================================================================
# QUICK ACTIONS
# ==========================================================================

@admin_bp.route('/products/<int:product_id>/sold', methods=['POST'])
@login_required
@require_role('admin')
def product_toggle_sold(product_id):
    product = Product.query.get_or_404(product_id)
    product.is_sold = not product.is_sold
    db.session.commit()
    status = 'Marked as sold' if product.is_sold else 'Marked as available'
    flash(f'{status}: {product.name}', 'success')
    return redirect(url_for('admin.products'))


@admin_bp.route('/products/<int:product_id>/active', methods=['POST'])
@login_required
@require_role('admin')
def product_toggle_active(product_id):
    product = Product.query.get_or_404(product_id)
    product.is_active = not product.is_active
    db.session.commit()
    status = 'Activated' if product.is_active else 'Deactivated'
    flash(f'{status}: {product.name}', 'success')
    return redirect(url_for('admin.products'))


# ==========================================================================
# DELETE IMAGE
# ==========================================================================

@admin_bp.route(
    '/products/<int:product_id>/images/<int:image_id>/delete',
    methods=['POST'],
)
@login_required
@require_role('admin')
def product_image_delete(product_id, image_id):
    img = ProductImage.query.filter_by(
        id=image_id, product_id=product_id
    ).first_or_404()

    file_path = os.path.join(
        current_app.root_path, 'static', img.image_url
    )
    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(img)

    product = Product.query.get_or_404(product_id)
    first = (ProductImage.query
             .filter_by(product_id=product_id)
             .order_by(ProductImage.sort_order)
             .first())
    product.primary_image = first.image_url if first else None
    db.session.commit()

    flash('Image deleted.', 'success')
    return redirect(url_for('admin.product_edit', product_id=product_id))
