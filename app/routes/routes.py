from flask import Blueprint, render_template, request, jsonify

routes_bp = Blueprint('routes', __name__)


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
    return render_template('heady_glass.html')

@routes_bp.route('/featured-artist')
def featured_artist():
    return render_template('artists.html')

@routes_bp.route('/archive')
def archive():
    return render_template('archive.html')


# ==========================================================================
# PRODUCTION GLASS
# Subcategories are sections on /prodos, accessed via anchor links
# ==========================================================================

@routes_bp.route('/prodos')
def prodos():
    return render_template('prodo_pieces.html')


# ==========================================================================
# VAPES & ACCESSORIES
# Subcategories are sections on /vapes-accessories, accessed via anchor links
# ==========================================================================

@routes_bp.route('/vapes-accessories')
def vapes_accessories():
    return render_template('vapes_accessories.html')


# ==========================================================================
# PRODUCT DETAIL — universal route for all products
# ==========================================================================

@routes_bp.route('/product/<slug>')
def product_detail(slug):
    return render_template('product.html', slug=slug)


# ==========================================================================
# AUTH
# ==========================================================================

@routes_bp.route('/login')
def login():
    return render_template('login.html')

@routes_bp.route('/register')
def register():
    return render_template('register.html')

@routes_bp.route('/logout')
def logout():
    return render_template('logout.html')


# ==========================================================================
# CART
# ==========================================================================

@routes_bp.route('/cart')
def cart():
    return render_template('cart.html')


# ==========================================================================
# ACCOUNT
# ==========================================================================

@routes_bp.route('/account')
def account_dashboard():
    return render_template('account_dashboard.html')

@routes_bp.route('/account/orders')
def account_orders():
    return render_template('account_orders.html')

@routes_bp.route('/account/wishlist')
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