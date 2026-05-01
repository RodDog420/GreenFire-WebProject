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

_BACKUP_PATH = os.environ.get(
    'INVENTORY_BACKUP_PATH',
    r'C:\Users\rodkr\GreenFire-WebProject_Support'
    r'\GreenFireSite_BackUp\GF_Inventory_Backup'
    r'\gf_inventory_backup.json'
)

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


def _sync_primary(product_id):
    """Set product.primary_image to the image with the lowest sort_order."""
    product = Product.query.get_or_404(product_id)
    first = (ProductImage.query
             .filter_by(product_id=product_id)
             .order_by(ProductImage.sort_order)
             .first())
    product.primary_image = first.image_url if first else None


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
    product.quantity         = int(form.get('quantity', 1) or 1)
    product.acquisition_type = form.get('acquisition_type', 'outright')
    product.gemstones        = 'gemstones'   in form
    product.electroform      = 'electroform' in form
    product.fume             = 'fume'        in form
    product.reclaimer        = 'reclaimer'   in form
    product.is_premium       = 'is_premium'  in form
    product.is_active        = 'is_active'   in form
    product.is_sold          = 'is_sold'     in form
    product.is_featured      = 'is_featured' in form
    fo = form.get('featured_order', '').strip()
    product.featured_order   = int(fo) if fo.isdigit() else None
    do = form.get('display_order', '').strip()
    product.display_order    = int(do) if do.isdigit() else None
    product.notes            = form.get('notes', '').strip() or None
    product.variants_json    = _parse_list_field(form.get('variants', ''))
    product.attributes_json  = _parse_list_field(form.get('attributes', ''))

    rate = form.get('consignment_rate', '').strip()
    product.consignment_rate = float(rate) if rate else None


def _reference_products():
    """Return products grouped by subcategory for the display-order reference panel."""
    all_prods = Product.query.order_by(Product.name).all()
    keys = [
        'heady',
        'dry-pipes', 'bubblers', 'beakers', 'oil-rigs',
        'vaporizers', 'flower-accessories', 'oil-accessories',
    ]
    ref = {k: {'numbered': [], 'unnumbered': []} for k in keys}
    for p in all_prods:
        if p.product_type == 'heady':
            key = 'heady'
        elif p.subcategory and p.subcategory in ref:
            key = p.subcategory
        else:
            continue
        if p.display_order is not None:
            ref[key]['numbered'].append(p)
        else:
            ref[key]['unnumbered'].append(p)
    for key in ref:
        ref[key]['numbered'].sort(key=lambda p: p.display_order)
    return ref


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
# INVENTORY BACKUP & SEED
# ==========================================================================

def _export_backup():
    """
    Write the current DB product state to the inventory backup JSON file.
    Called after every seed and after every product add/edit/delete.
    """
    products = (Product.query
                .order_by(Product.product_type, Product.name)
                .all())
    data = []
    for p in products:
        images = (ProductImage.query
                  .filter_by(product_id=p.id)
                  .order_by(ProductImage.sort_order)
                  .all())
        data.append({
            'slug':                p.slug,
            'name':                p.name,
            'product_type':        p.product_type,
            'subcategory':         p.subcategory,
            'series':              p.series,
            'credit_label':        p.credit_label,
            'credit':              p.credit,
            'instagram':           p.instagram,
            'collab':              p.collab,
            'price_cents':         p.price_cents,
            'height':              p.height,
            'technique':           p.technique,
            'joint_size':          p.joint_size,
            'glass_color':         p.glass_color,
            'glass_color_company': p.glass_color_company,
            'gemstones':           p.gemstones,
            'electroform':         p.electroform,
            'fume':                p.fume,
            'description':         p.description,
            'is_sold':             p.is_sold,
            'is_active':           p.is_active,
            'is_featured':         p.is_featured,
            'featured_order':      p.featured_order,
            'quantity':            p.quantity,
            'meta_description':    p.meta_description,
            'perc':                p.perc,
            'reclaimer':           p.reclaimer,
            'includes':            p.includes,
            'variants':            p.variants,
            'attributes':          p.attributes,
            'is_premium':          p.is_premium,
            'metal_type':          p.metal_type,
            'primary_image':       p.primary_image,
            'acquisition_type':    p.acquisition_type,
            'images': [img.image_url for img in images],
        })
    os.makedirs(os.path.dirname(_BACKUP_PATH), exist_ok=True)
    with open(_BACKUP_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def _seed_from_products():
    """
    Insert products from the backup JSON into the DB.
    Skips any slug that already exists.
    Returns (inserted, skipped) counts.
    """
    with open(_BACKUP_PATH, 'r', encoding='utf-8') as f:
        PRODUCTS = json.load(f)
    inserted = 0
    skipped  = 0
    for p in PRODUCTS:
        if Product.query.filter_by(slug=p['slug']).first():
            skipped += 1
            continue
        product = Product(
            slug=                p['slug'],
            name=                p['name'],
            product_type=        p['product_type'],
            subcategory=         p.get('subcategory'),
            series=              p.get('series'),
            credit_label=        p.get('credit_label'),
            credit=              p.get('credit'),
            instagram=           p.get('instagram'),
            collab=              p.get('collab'),
            price_cents=         p['price_cents'],
            height=              p.get('height'),
            technique=           p.get('technique'),
            joint_size=          p.get('joint_size'),
            glass_color=         p.get('glass_color'),
            glass_color_company= p.get('glass_color_company'),
            gemstones=           p.get('gemstones', False),
            electroform=         p.get('electroform', False),
            fume=                p.get('fume', False),
            description=         p.get('description', ''),
            is_sold=             p.get('is_sold', False),
            is_active=           p.get('is_active', True),
            is_featured=         p.get('is_featured', False),
            featured_order=      p.get('featured_order'),
            quantity=            p.get('quantity', 1),
            meta_description=    p.get('meta_description'),
            perc=                p.get('perc'),
            reclaimer=           p.get('reclaimer', False),
            includes=            p.get('includes'),
            variants_json=       json.dumps(p['variants'])
                                 if p.get('variants') else None,
            attributes_json=     json.dumps(p['attributes'])
                                 if p.get('attributes') else None,
            is_premium=          p.get('is_premium', False),
            metal_type=          p.get('metal_type'),
            primary_image=       p.get('primary_image'),
            acquisition_type=    p.get('acquisition_type', 'outright'),
        )
        db.session.add(product)
        db.session.flush()
        # All images in order — backup JSON images list is the
        # complete ordered set (sort_order 0, 1, 2 ...)
        for i, img_url in enumerate(p.get('images', [])):
            db.session.add(ProductImage(
                product_id= product.id,
                image_url=  img_url,
                alt_text=   product.name,
                sort_order= i,
            ))
        inserted += 1
    db.session.commit()
    return inserted, skipped


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
# SEED / RESTORE
# ==========================================================================

@admin_bp.route('/seed', methods=['POST'])
@login_required
@require_role('admin')
def seed_products():
    try:
        inserted, skipped = _seed_from_products()
        _export_backup()
        flash(
            f'Inventory loaded: {inserted} added, {skipped} already existed.',
            'success'
        )
    except Exception as e:
        db.session.rollback()
        flash(f'Seed failed: {e}', 'error')
    return redirect(url_for('admin.dashboard'))


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
            return render_template('admin_product_form.html',
                                   product=None,
                                   ref_products=_reference_products())

        if Product.query.filter_by(slug=slug).first():
            flash(f'Slug "{slug}" is already in use. Choose a different slug.', 'error')
            return render_template('admin_product_form.html',
                                   product=None,
                                   ref_products=_reference_products())

        product = Product(slug=slug)
        _apply_form(product, request.form)
        db.session.add(product)
        db.session.flush()

        _save_images(product, request.files.getlist('images'))
        db.session.commit()
        _export_backup()

        flash(f'"{product.name}" added.', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin_product_form.html',
                           product=None,
                           ref_products=_reference_products())


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
        _export_backup()
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
        ref_products=_reference_products(),
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
    _export_backup()
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
    _export_backup()
    status = 'Activated' if product.is_active else 'Deactivated'
    flash(f'{status}: {product.name}', 'success')
    return redirect(url_for('admin.products'))


# ==========================================================================
# DELETE PRODUCT
# ==========================================================================

@admin_bp.route('/products/<int:product_id>/delete', methods=['POST'])
@login_required
@require_role('admin')
def product_delete(product_id):
    product = Product.query.get_or_404(product_id)
    name = product.name

    images = ProductImage.query.filter_by(product_id=product_id).all()
    for img in images:
        file_path = os.path.join(
            current_app.root_path, 'static', img.image_url
        )
        if os.path.exists(file_path):
            os.remove(file_path)

    upload_dir = os.path.join(
        current_app.root_path, 'static', 'images', 'products', product.slug
    )
    if os.path.isdir(upload_dir) and not os.listdir(upload_dir):
        os.rmdir(upload_dir)

    db.session.delete(product)
    db.session.commit()
    _export_backup()

    flash(f'"{name}" deleted.', 'success')
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

    _sync_primary(product_id)
    db.session.commit()
    _export_backup()

    flash('Image deleted.', 'success')
    return redirect(url_for('admin.product_edit', product_id=product_id))


@admin_bp.route(
    '/products/<int:product_id>/images/<int:image_id>/move-up',
    methods=['POST'],
)
@login_required
@require_role('admin')
def product_image_move_up(product_id, image_id):
    img = ProductImage.query.filter_by(
        id=image_id, product_id=product_id
    ).first_or_404()
    prev = (ProductImage.query
            .filter_by(product_id=product_id)
            .filter(ProductImage.sort_order < img.sort_order)
            .order_by(ProductImage.sort_order.desc())
            .first())
    if prev:
        img.sort_order, prev.sort_order = prev.sort_order, img.sort_order
        _sync_primary(product_id)
        db.session.commit()
    return redirect(url_for('admin.product_edit', product_id=product_id))


@admin_bp.route(
    '/products/<int:product_id>/images/<int:image_id>/move-down',
    methods=['POST'],
)
@login_required
@require_role('admin')
def product_image_move_down(product_id, image_id):
    img = ProductImage.query.filter_by(
        id=image_id, product_id=product_id
    ).first_or_404()
    next_img = (ProductImage.query
                .filter_by(product_id=product_id)
                .filter(ProductImage.sort_order > img.sort_order)
                .order_by(ProductImage.sort_order)
                .first())
    if next_img:
        img.sort_order, next_img.sort_order = next_img.sort_order, img.sort_order
        _sync_primary(product_id)
        db.session.commit()
    return redirect(url_for('admin.product_edit', product_id=product_id))
