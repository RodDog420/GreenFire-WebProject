from flask import (
    Blueprint, render_template, request, jsonify,
    redirect, url_for, flash,
)
from flask_login import login_required, logout_user, login_user, current_user
from app import limiter, db
from app.models import User, Product

routes_bp = Blueprint('routes', __name__)


# ==========================================================================
# CATALOGUE HELPERS — DB queries
# ==========================================================================

def _headies():
    products = (Product.query
                .filter_by(product_type='heady', is_active=True, is_sold=False)
                .all())
    return sorted(products,
                  key=lambda p: (p.credit is None, p.credit or '', p.name))


def _sold_headies():
    products = (Product.query
                .filter_by(product_type='heady', is_sold=True)
                .all())
    return sorted(products,
                  key=lambda p: (p.credit is None, p.credit or '', p.name))


def _prodos():
    return (Product.query
            .filter_by(product_type='prodo', is_active=True)
            .all())


def _vapes():
    return (Product.query
            .filter_by(product_type='vape', is_active=True)
            .all())


def _product_neighbours(product):
    ptype = product.product_type
    if ptype == 'heady':
        catalogue = _sold_headies() if product.is_sold else _headies()
    elif ptype == 'prodo':
        catalogue = _prodos()
    else:
        catalogue = _vapes()

    slugs = [p.slug for p in catalogue]
    if product.slug not in slugs:
        return None, None

    idx    = slugs.index(product.slug)
    prev_p = catalogue[idx - 1] if idx > 0 else None
    next_p = catalogue[idx + 1] if idx < len(catalogue) - 1 else None
    return prev_p, next_p


# ==========================================================================
# AUTO META DESCRIPTION
# ==========================================================================

_SUBCATEGORY_LABELS = {
    'dry-pipes':          'dry pipe',
    'bubblers':           'bubbler',
    'beakers':            'beaker',
    'oil-rigs':           'oil rig',
    'vaporizers':         'vaporizer',
    'flower-accessories': 'flower accessory',
    'oil-accessories':    'oil accessory',
}
_META_SUFFIX_HEADY = ' — heady glass at Green Fire, Lincoln NE.'
_META_SUFFIX_PRODO = ' — American production glass at Green Fire, Lincoln NE.'
_META_SUFFIX_VAPE  = ' at Green Fire, Lincoln NE.'
_META_LIMIT        = 155


def _build_meta(base, specs, suffix):
    result = base
    for spec in specs:
        candidate = result + ', ' + spec + suffix
        if len(candidate) <= _META_LIMIT:
            result += ', ' + spec
    return result + suffix


def _auto_meta(p):
    ptype = p.product_type
    if ptype == 'heady':
        base  = (p.credit + ' ' + p.name) if p.credit else p.name
        specs = []
        if p.technique:          specs.append(p.technique)
        if p.glass_color:
            c = p.glass_color
            if p.glass_color_company:
                c += ' (' + p.glass_color_company + ')'
            specs.append(c)
        if p.gemstones:          specs.append('gemstone accents')
        if p.electroform:        specs.append('electroformed')
        if p.fume:               specs.append('fumed')
        if p.height:             specs.append(p.height)
        if p.joint_size:         specs.append(p.joint_size)
        return _build_meta(base, specs, _META_SUFFIX_HEADY)
    elif ptype == 'prodo':
        base = (p.credit + ' ' + p.name) if p.credit else p.name
        cat  = _SUBCATEGORY_LABELS.get(p.subcategory or '', '')
        if cat:
            base += ' ' + cat
        specs = []
        if p.perc:               specs.append(p.perc)
        if p.height:             specs.append(p.height)
        if p.joint_size:         specs.append(p.joint_size)
        if p.fume:               specs.append('fumed')
        if p.reclaimer:          specs.append('with reclaimer')
        return _build_meta(base, specs, _META_SUFFIX_PRODO)
    else:
        base = (p.credit + ' ' + p.name) if p.credit else p.name
        cat  = _SUBCATEGORY_LABELS.get(p.subcategory or '', '')
        if cat:
            base += ' ' + cat
        specs = []
        if p.attributes:         specs.extend(p.attributes)
        if p.metal_type:         specs.append(p.metal_type)
        if p.is_premium:         specs.append('premium')
        return _build_meta(base, specs, _META_SUFFIX_VAPE)


# ==========================================================================
# MAIN
# ==========================================================================

@routes_bp.route('/')
def index():
    return render_template('index.html')

@routes_bp.route('/about')
def about():
    return render_template('about.html')

@routes_bp.route('/shipping-returns')
def shipping_returns():
    return render_template('shipping_returns.html')

@routes_bp.route('/contact')
def contact():
    return render_template('contact.html')

@routes_bp.route('/privacy')
def privacy():
    return render_template('privacy.html')

@routes_bp.route('/terms')
def terms():
    return render_template('terms.html')


# ==========================================================================
# HEADY GLASS
# ==========================================================================

@routes_bp.route('/headies')
def headies():
    products = _headies()
    return render_template('heady_glass.html', products=products)

@routes_bp.route('/featured-artist')
def featured_artist():
    return render_template('artists.html')

@routes_bp.route('/archive')
def archive():
    products = _sold_headies()
    return render_template('archive.html', products=products)


# ==========================================================================
# PRODUCTION GLASS
# Subcategories are sections on /prodos, accessed via anchor links
# ==========================================================================

@routes_bp.route('/prodos')
def prodos():
    products = _prodos()
    return render_template('prodo_pieces.html', products=products)


# ==========================================================================
# VAPES & ACCESSORIES
# Subcategories are sections on /vapes-accessories, accessed via anchor links
# ==========================================================================

@routes_bp.route('/vapes-accessories')
def vapes_accessories():
    products = _vapes()
    return render_template('vapes_accessories.html', products=products)


# ==========================================================================
# PRODUCT DETAIL — universal route for all products
# ==========================================================================

@routes_bp.route('/product/<slug>')
def product_detail(slug):
    product = Product.query.filter_by(slug=slug).first_or_404()
    prev_product, next_product = _product_neighbours(product)
    meta_desc = product.meta_description or _auto_meta(product)
    return render_template(
        'product.html',
        product=product,
        prev_product=prev_product,
        next_product=next_product,
        meta_desc=meta_desc,
    )


# ==========================================================================
# AUTH
# ==========================================================================

@routes_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit('10 per minute')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter(
            db.func.lower(User.email) == email
        ).first()

        # Generic message — never reveal whether the email exists
        if not user or not user.check_password(password):
            flash('Invalid email or password.', 'error')
            return render_template('login.html')

        if not user.is_active:
            flash('Invalid email or password.', 'error')
            return render_template('login.html')

        login_user(user)

        next_page = request.args.get('next')
        if next_page and next_page.startswith('/'):
            return redirect(next_page)
        if user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('routes.index'))

    return render_template('login.html')


@routes_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        return redirect(url_for('routes.index'))
    return render_template('logout.html')


@routes_bp.route('/register')
def register():
    return render_template('register.html')


# ==========================================================================
# CART
# ==========================================================================

@routes_bp.route('/cart')
def cart():
    return render_template('cart.html')

@routes_bp.route('/cart/add', methods=['POST'])
@limiter.limit('30 per minute')
def add_to_cart():
    # Stub — full implementation when cart is built
    flash('Cart coming soon.', 'info')
    return redirect(request.referrer or url_for('routes.index'))

@routes_bp.route('/cart/wishlist/add', methods=['POST'])
@limiter.limit('30 per minute')
@login_required
def add_to_wishlist():
    # Stub — full implementation when auth is built
    flash('Wishlist coming soon.', 'info')
    return redirect(request.referrer or url_for('routes.index'))


# ==========================================================================
# NOTIFY ME — sold heady pieces
# ==========================================================================

@routes_bp.route('/notify-me', methods=['POST'])
@limiter.limit('5 per minute')
def notify_me():
    # Stub — full implementation when email service is configured
    flash(
        "We\u2019ll let you know when this artist has new work.",
        'success'
    )
    return redirect(request.referrer or url_for('routes.index'))


# ==========================================================================
# ACCOUNT
# ==========================================================================

@routes_bp.route('/account')
@login_required
def account_dashboard():
    return render_template('account_dashboard.html')

@routes_bp.route('/account/orders')
@login_required
def account_orders():
    return render_template('account_orders.html')

@routes_bp.route('/account/wishlist')
@login_required
def account_wishlist():
    return render_template('account_wishlist.html')


# ==========================================================================
# CHAT API
# ==========================================================================

@routes_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    return jsonify({'reply': 'Chat agent coming soon.'})


# ==========================================================================
# HEALTH CHECK
# ==========================================================================

@routes_bp.route('/health')
def health():
    return jsonify({'status': 'ok'})