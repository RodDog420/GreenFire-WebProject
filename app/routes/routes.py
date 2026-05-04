import os
import anthropic
import stripe
from flask import (
    Blueprint, render_template, request, jsonify,
    redirect, url_for, flash, session, current_app,
)
from flask_login import login_required, logout_user, login_user, current_user
from flask_mail import Message
from app import limiter, db, csrf, mail
from app.models import User, Product, WishlistItem, Order, OrderItem

routes_bp = Blueprint('routes', __name__)


# ==========================================================================
# PENNY — AI CHAT AGENT SYSTEM PROMPT
# Cached on first call. Update here when store info or policies change.
# ==========================================================================

_PENNY_SYSTEM_PROMPT = """You are Penny, the chat assistant for Green Fire — an American \
functional glass gallery and future licensed cannabis retailer at 2401 N 48th St, \
University Place neighborhood, Lincoln, Nebraska.

GREEN FIRE'S STORY
Green Fire opened in Seattle in 2013 as a gallery-quality adult-use retailer — not a head \
shop. We were among the first licensed adult-use retailers in Washington state. After ten \
years, we left Seattle and came to Lincoln on purpose: Nebraska is building a new legal \
cannabis market and we intend to be part of it from the ground floor, the same way we were \
in Washington. Green Fire is currently applying for a Nebraska State Medical Cannabis retail \
license.

YOUR ROLE
You are a knowledgeable functional glass expert and cannabis-informed retail assistant. You \
answer questions about: glass craft and technique, cannabis consumption methods and how \
different pipe types serve them, the current in-store inventory, artists, shipping, returns, \
and Green Fire's story.

GLASS EXPERTISE — USE THIS FREELY
You know American functional glass deeply: borosilicate vs. soft glass, lampworking, fuming \
(gold and silver), color techniques, implosion marbles, sandblasting, electroforming, worked \
and sculpted glass, scientific glass, the history of the American glass art movement, what \
separates heady from production work, and how quality shows in a piece. Speak to this \
confidently.

CANNABIS AND CONSUMPTION KNOWLEDGE — USE THIS FREELY
Flower (combustion): dry pipes, bubblers, beakers, straight tubes. Water pieces filter and \
cool smoke. More water volume equals a smoother experience.

Concentrates and dabs: oil rigs are purpose-built for concentrates. High-heat surfaces — \
bangers (quartz or ceramic) or nails — vaporize the concentrate. A carb cap controls \
airflow and traps vapor. Lower temp equals more flavor; higher temp equals bigger hit.

Vaporization: vaporizers heat flower or concentrate below combustion temperature. Convection \
vs. conduction heating. Desktop vs. portable. Flower vapes, concentrate vapes, dual-use.

Terminology you use naturally: dab, banger, nail, carb cap, terp pearl, concentrate, wax, \
shatter, live resin, rosin, reclaim, reclaimer, quartz vs. titanium, perc, percolator, \
diffusion, drag.

You can explain what makes a good rig for concentrates, why someone would choose a bubbler \
over a dry pipe, how water filtration affects the experience, and what to look for in \
quality glass.

NEBRASKA CANNABIS CONTEXT
Nebraska passed the Medical Cannabis Act via ballot initiative in November 2024. The Nebraska \
Medical Cannabis Commission was established to regulate the program. Green Fire is applying \
for a retail license. Medical cannabis patients in Nebraska are 18+ with a valid medical card; \
all glass customers must be 21+.

INDUSTRY TERMINOLOGY (use naturally)
Heady: artistic, one-of-a-kind, high-craft functional glass.
Prodo: production glass series — consistent, reliable, well-made.
Rig: oil and concentrate pipe.
Bubbler: water pipe with integrated water chamber.
Beaker: flat-bottom water pipe.
Straight tube: cylindrical water pipe.
Banger: quartz or ceramic bucket used for dabbing.
Perc / percolator: internal water filtration chamber.

FEATURED ARTIST
Josh Mann — Green Fire carries his heady work and has a direct personal relationship with \
him. We only carry artists we know personally. No catalog orders.

SHIPPING (domestic US only — must be 21+ to purchase)
Under $50: $8 flat rate.
$50 to $150: $12 flat rate.
Over $150: free shipping.

RETURNS
Glass: final sale — no returns or exchanges.
Non-glass items: 14-day return window.

TONE
Direct, knowledgeable, and genuinely helpful — the way someone on a real gallery floor \
would speak. Not salesy. Not preachy. If you don't know something specific, say so honestly \
and suggest the customer contact the store directly. Never make medical claims or dosage \
recommendations. Always frame cannabis discussion in a legal-age, legal-jurisdiction context."""


# ==========================================================================
# CATALOGUE HELPERS — DB queries
# ==========================================================================

def _headies():
    products = (Product.query
                .filter_by(product_type='heady', is_active=True, is_sold=False)
                .all())
    return sorted(products,
                  key=lambda p: (p.display_order is None,
                                 p.display_order or 0,
                                 p.credit is None,
                                 p.credit or '',
                                 p.name))


def _sold_headies():
    products = (Product.query
                .filter_by(product_type='heady', is_sold=True)
                .all())
    return sorted(products,
                  key=lambda p: (p.display_order is None,
                                 p.display_order or 0,
                                 p.credit is None,
                                 p.credit or '',
                                 p.name))


def _prodos():
    products = (Product.query
                .filter_by(product_type='prodo', is_active=True)
                .all())
    return sorted(products,
                  key=lambda p: (p.display_order is None,
                                 p.display_order or 0,
                                 p.name))


def _vapes():
    products = (Product.query
                .filter(Product.product_type.in_(['vape', 'tool']),
                        Product.is_active == True)
                .all())
    return sorted(products,
                  key=lambda p: (p.display_order is None,
                                 p.display_order or 0,
                                 p.name))


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

@routes_bp.route('/contact', methods=['GET', 'POST'])
@limiter.limit('5 per minute')
def contact():
    if request.method == 'POST':
        name    = request.form.get('name', '').strip()
        email   = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not email or not message:
            flash('Please fill in all required fields.', 'error')
            return render_template('contact.html',
                                   name=name,
                                   email=email,
                                   subject=subject,
                                   message=message)

        try:
            msg = Message(
                subject=f"Green Fire Contact: {subject or 'No subject'}",
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[current_app.config['MAIL_DEFAULT_SENDER']],
                reply_to=email,
                body=f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\nMessage:\n{message}"
            )
            mail.send(msg)
            flash("Thanks for reaching out \u2014 we\u2019ll get back to you soon.", 'success')
        except Exception:
            flash("Something went wrong sending your message. Please try again.", 'error')
            return render_template('contact.html',
                                   name=name,
                                   email=email,
                                   subject=subject,
                                   message=message)
        return redirect(url_for('routes.contact'))

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
    products = (Product.query
                .filter(
                    Product.is_featured == True,
                    Product.is_active == True,
                )
                .order_by(
                    Product.featured_order.is_(None),
                    Product.featured_order,
                    Product.created_at.desc(),
                )
                .all())

    portraits_dir = os.path.join(
        current_app.root_path, 'static',
        'images', 'featured_artist', 'josh_mann', 'portraits',
    )
    portraits = []
    for i in range(1, 11):
        for ext in ('png', 'jpg', 'jpeg', 'webp'):
            path = os.path.join(portraits_dir, f'{i}.{ext}')
            if os.path.exists(path):
                portraits.append(
                    f'images/featured_artist/josh_mann/portraits/{i}.{ext}'
                )
                break

    return render_template('artists.html',
                           products=products,
                           portraits=portraits)

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


@routes_bp.route('/register', methods=['GET', 'POST'])
@limiter.limit('5 per minute')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

        error = None

        if not email or not username or not password or not confirm:
            error = 'All fields are required.'
        elif len(username) < 3 or len(username) > 64:
            error = 'Username must be between 3 and 64 characters.'
        elif len(password) < 8:
            error = 'Password must be at least 8 characters.'
        elif password != confirm:
            error = 'Passwords do not match.'
        elif (User.query.filter(db.func.lower(User.email) == email).first() or
              User.query.filter(db.func.lower(User.username) == username.lower()).first()):
            # Generic — never reveal whether email or username is taken
            error = 'Unable to create account. Please check your details and try again.'

        if error:
            flash(error, 'error')
            return render_template('register.html',
                                   email=email,
                                   username=username)

        user = User(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Welcome to Green Fire!', 'success')
        return redirect(url_for('routes.index'))

    return render_template('register.html')


# ==========================================================================
# CART — session-based, no DB
# session['cart'] = [{'slug', 'name', 'price_cents', 'variant', 'qty'}, ...]
# ==========================================================================

def _sync_cart_count():
    cart = session.get('cart', [])
    session['cart_count'] = sum(item['qty'] for item in cart)


@routes_bp.route('/cart')
def cart():
    raw = session.get('cart', [])
    cart_items = []
    changed = False

    for item in raw:
        product = Product.query.filter_by(
            slug=item['slug'], is_active=True, is_sold=False
        ).first()
        if not product:
            changed = True
            continue
        cart_items.append({
            'slug':        item['slug'],
            'name':        item['name'],
            'price_cents': item['price_cents'],
            'variant':     item.get('variant'),
            'qty':         item['qty'],
            'line_cents':  item['price_cents'] * item['qty'],
            'image':       product.primary_image,
        })

    if changed:
        session['cart'] = [{k: v for k, v in i.items()
                            if k != 'line_cents' and k != 'image'}
                           for i in cart_items]
        _sync_cart_count()
        flash('One or more items were removed because they are no longer available.',
              'info')

    subtotal_cents = sum(i['line_cents'] for i in cart_items)
    return render_template('cart.html',
                           cart_items=cart_items,
                           subtotal_cents=subtotal_cents)


@routes_bp.route('/cart/add', methods=['POST'])
@limiter.limit('30 per minute')
def add_to_cart():
    slug        = request.form.get('product_slug', '').strip()
    variant     = request.form.get('variant') or None

    product = Product.query.filter_by(
        slug=slug, is_active=True, is_sold=False
    ).first()
    if not product:
        flash('This item is no longer available.', 'error')
        return redirect(request.referrer or url_for('routes.index'))

    cart = session.get('cart', [])
    for item in cart:
        if item['slug'] == slug and item.get('variant') == variant:
            if item['qty'] < product.quantity:
                item['qty'] += 1
            break
    else:
        cart.append({
            'slug':        product.slug,
            'name':        product.name,
            'price_cents': product.price_cents,
            'variant':     variant,
            'qty':         1,
        })

    session['cart'] = cart
    _sync_cart_count()
    flash(f'\u201c{product.name}\u201d added to your cart.', 'success')
    return redirect(request.referrer or url_for('routes.index'))


@routes_bp.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    slug    = request.form.get('product_slug', '').strip()
    variant = request.form.get('variant') or None

    cart = session.get('cart', [])
    cart = [i for i in cart
            if not (i['slug'] == slug and i.get('variant') == variant)]
    session['cart'] = cart
    _sync_cart_count()
    return redirect(url_for('routes.cart'))


@routes_bp.route('/cart/wishlist/add', methods=['POST'])
@limiter.limit('30 per minute')
@login_required
def add_to_wishlist():
    slug = request.form.get('product_slug', '').strip()
    product = Product.query.filter_by(slug=slug, is_active=True).first()
    if not product:
        flash('That product is no longer available.', 'error')
        return redirect(request.referrer or url_for('routes.index'))

    existing = WishlistItem.query.filter_by(
        user_id=current_user.id, product_id=product.id
    ).first()
    if existing:
        flash(f'\u201c{product.name}\u201d is already in your wish list.', 'info')
    else:
        db.session.add(WishlistItem(user_id=current_user.id, product_id=product.id))
        db.session.commit()
        flash(f'\u201c{product.name}\u201d saved to your wish list.', 'success')

    return redirect(request.referrer or url_for('routes.index'))


@routes_bp.route('/wishlist/remove', methods=['POST'])
@login_required
def remove_from_wishlist():
    slug = request.form.get('product_slug', '').strip()
    product = Product.query.filter_by(slug=slug).first()
    if product:
        WishlistItem.query.filter_by(
            user_id=current_user.id, product_id=product.id
        ).delete()
        db.session.commit()
    return redirect(url_for('routes.account_wishlist'))


# ==========================================================================
# NOTIFY ME — sold heady pieces
# ==========================================================================

@routes_bp.route('/notify-me', methods=['POST'])
@limiter.limit('5 per minute')
def notify_me():
    email        = request.form.get('email', '').strip()
    artist       = request.form.get('artist_credit', '').strip()
    product_slug = request.form.get('product_slug', '').strip()

    if not email:
        flash('Please enter your email address.', 'error')
        return redirect(request.referrer or url_for('routes.index'))

    try:
        store_msg = Message(
            subject=f"Green Fire — Notify Me: {artist or product_slug}",
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[current_app.config['MAIL_DEFAULT_SENDER']],
            body=(
                f"Notify request received.\n\n"
                f"Email: {email}\n"
                f"Artist: {artist}\n"
                f"Product: {product_slug}"
            )
        )
        mail.send(store_msg)

        confirm_msg = Message(
            subject="Green Fire — We'll Keep You Posted",
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[email],
            body=(
                f"Hi,\n\n"
                f"Thanks for your interest in {artist}'s work. "
                f"We'll reach out as soon as new pieces are available.\n\n"
                f"Green Fire\n"
                f"2401 N 48th St, Lincoln, Nebraska"
            )
        )
        mail.send(confirm_msg)
    except Exception:
        pass

    flash("We'll let you know when this artist has new work.", 'success')
    return redirect(request.referrer or url_for('routes.index'))


# ==========================================================================
# ACCOUNT
# ==========================================================================

@routes_bp.route('/account')
@login_required
def account_dashboard():
    wishlist_count = WishlistItem.query.filter_by(user_id=current_user.id).count()
    order_count    = Order.query.filter_by(user_id=current_user.id).count()
    return render_template('account_dashboard.html',
                           wishlist_count=wishlist_count,
                           order_count=order_count)

@routes_bp.route('/account/orders')
@login_required
def account_orders():
    orders = (Order.query
              .filter_by(user_id=current_user.id)
              .order_by(Order.created_at.desc())
              .all())
    return render_template('account_orders.html', orders=orders)

@routes_bp.route('/account/wishlist')
@login_required
def account_wishlist():
    items = (WishlistItem.query
             .filter_by(user_id=current_user.id)
             .join(Product)
             .order_by(WishlistItem.created_at.desc())
             .all())
    return render_template('account_wishlist.html', items=items)


# ==========================================================================
# CHECKOUT
# ==========================================================================

def _shipping_cents(subtotal_cents):
    if subtotal_cents >= 15000:   # $150+  → free
        return 0
    elif subtotal_cents >= 5000:  # $50–$150 → $12
        return 1200
    return 800                    # under $50 → $8


@routes_bp.route('/checkout')
@login_required
def checkout():
    raw = session.get('cart', [])
    if not raw:
        flash('Your cart is empty.', 'info')
        return redirect(url_for('routes.cart'))

    cart_items = []
    for item in raw:
        product = Product.query.filter_by(
            slug=item['slug'], is_active=True, is_sold=False
        ).first()
        if not product:
            continue
        cart_items.append({
            'slug':        item['slug'],
            'name':        item['name'],
            'price_cents': item['price_cents'],
            'variant':     item.get('variant'),
            'qty':         item['qty'],
            'line_cents':  item['price_cents'] * item['qty'],
        })

    if not cart_items:
        flash('One or more items are no longer available.', 'info')
        return redirect(url_for('routes.cart'))

    subtotal_cents = sum(i['line_cents'] for i in cart_items)
    shipping_cents = _shipping_cents(subtotal_cents)
    total_cents    = subtotal_cents + shipping_cents

    return render_template(
        'checkout.html',
        cart_items=cart_items,
        subtotal_cents=subtotal_cents,
        shipping_cents=shipping_cents,
        total_cents=total_cents,
        stripe_public_key=current_app.config['STRIPE_PUBLIC_KEY'],
    )


@routes_bp.route('/checkout/create-intent', methods=['POST'])
@login_required
@limiter.limit('10 per minute')
@csrf.exempt
def create_payment_intent():
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

    raw = session.get('cart', [])
    if not raw:
        return jsonify({'error': 'Cart is empty'}), 400

    subtotal_cents = sum(i['price_cents'] * i['qty'] for i in raw)
    total_cents    = subtotal_cents + _shipping_cents(subtotal_cents)

    try:
        intent = stripe.PaymentIntent.create(
            amount=total_cents,
            currency='usd',
            metadata={
                'user_id':  str(current_user.id),
                'username': current_user.username,
            },
        )
        return jsonify({'client_secret': intent.client_secret})
    except stripe.StripeError as e:
        return jsonify({'error': str(e)}), 400


@routes_bp.route('/checkout/confirm', methods=['POST'])
@login_required
@limiter.limit('10 per minute')
def checkout_confirm():
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

    payment_intent_id = request.form.get('payment_intent_id', '').strip()
    if not payment_intent_id:
        flash('Payment information missing. Please try again.', 'error')
        return redirect(url_for('routes.checkout'))

    # Verify with Stripe — never trust client-side success alone
    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
    except stripe.StripeError:
        flash('Could not verify payment. Please contact us.', 'error')
        return redirect(url_for('routes.checkout'))

    if intent.status != 'succeeded':
        flash('Payment was not completed. Please try again.', 'error')
        return redirect(url_for('routes.checkout'))

    # Idempotency — redirect if order already created
    existing = Order.query.filter_by(
        stripe_payment_intent_id=payment_intent_id
    ).first()
    if existing:
        return redirect(url_for('routes.checkout_success', order_id=existing.id))

    # Rebuild totals from current cart (source of truth)
    raw = session.get('cart', [])
    subtotal_cents = 0
    order_items    = []

    for item in raw:
        product = Product.query.filter_by(
            slug=item['slug'], is_active=True
        ).first()
        if not product:
            continue
        subtotal_cents += item['price_cents'] * item['qty']
        order_items.append({
            'product':     product,
            'qty':         item['qty'],
            'price_cents': item['price_cents'],
        })

    if not order_items:
        flash('No valid items found. Please contact us.', 'error')
        return redirect(url_for('routes.cart'))

    shipping_cents = _shipping_cents(subtotal_cents)
    total_cents    = subtotal_cents + shipping_cents

    order = Order(
        user_id                  = current_user.id,
        status                   = 'paid',
        stripe_payment_intent_id = payment_intent_id,
        subtotal_cents           = subtotal_cents,
        shipping_cents           = shipping_cents,
        total_cents              = total_cents,
        shipping_name            = request.form.get('shipping_name', '').strip(),
        shipping_address_1       = request.form.get('shipping_address_1', '').strip(),
        shipping_address_2       = request.form.get('shipping_address_2', '').strip() or None,
        shipping_city            = request.form.get('shipping_city', '').strip(),
        shipping_state           = request.form.get('shipping_state', '').strip(),
        shipping_zip             = request.form.get('shipping_zip', '').strip(),
        shipping_country         = 'US',
    )
    db.session.add(order)
    db.session.flush()

    for oi in order_items:
        db.session.add(OrderItem(
            order_id    = order.id,
            product_id  = oi['product'].id,
            quantity    = oi['qty'],
            price_cents = oi['price_cents'],
        ))
        if oi['product'].product_type == 'heady':
            oi['product'].is_sold = True

    db.session.commit()

    session.pop('cart', None)
    session.pop('cart_count', None)

    return redirect(url_for('routes.checkout_success', order_id=order.id))


@routes_bp.route('/checkout/success/<int:order_id>')
@login_required
def checkout_success(order_id):
    order = Order.query.filter_by(
        id=order_id, user_id=current_user.id
    ).first_or_404()
    items = order.items.all()
    return render_template('checkout_success.html', order=order, items=items)


# ==========================================================================
# CHAT API — Penny
# ==========================================================================

@routes_bp.route('/api/chat', methods=['POST'])
@limiter.limit('30 per minute')
@csrf.exempt
def chat():
    data = request.get_json(silent=True) or {}
    history = data.get('history', [])
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'reply': "I didn't catch that — what can I help you with?"})

    api_key = current_app.config.get('ANTHROPIC_API_KEY')
    if not api_key:
        return jsonify({'reply': 'Chat is temporarily unavailable. Try again later.'})

    # Build live inventory block — fresh each session, not cached
    try:
        active = (Product.query
                  .filter_by(is_active=True, is_sold=False)
                  .order_by(Product.product_type, Product.name)
                  .all())
        if active:
            lines = ['CURRENT IN-STOCK INVENTORY\n']
            for p in active:
                price = f'${p.price_cents / 100:.2f}'
                artist = f' by {p.credit}' if p.credit else ''
                ptype = p.product_type.upper()
                lines.append(f'- [{ptype}] {p.name}{artist} — {price} — /product/{p.slug}')
            inventory_text = '\n'.join(lines)
        else:
            inventory_text = 'CURRENT INVENTORY: No products currently in stock.'
    except Exception:
        inventory_text = 'CURRENT INVENTORY: Unable to retrieve at this time.'

    # Validate and build message history
    messages = []
    for turn in history:
        role = turn.get('role')
        content = (turn.get('content') or '').strip()
        if role in ('user', 'assistant') and content:
            messages.append({'role': role, 'content': content})
    messages.append({'role': 'user', 'content': user_message})

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=512,
            system=[
                {
                    'type': 'text',
                    'text': _PENNY_SYSTEM_PROMPT,
                    'cache_control': {'type': 'ephemeral'},
                },
                {
                    'type': 'text',
                    'text': inventory_text,
                },
            ],
            messages=messages,
        )
        return jsonify({'reply': response.content[0].text})

    except Exception:
        return jsonify({'reply': 'Having trouble right now. Try again in a moment.'})


# ==========================================================================
# HEALTH CHECK
# ==========================================================================

@routes_bp.route('/health')
def health():
    return jsonify({'status': 'ok'})