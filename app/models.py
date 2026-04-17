import json
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


# ==========================================================================
# USER
# ==========================================================================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(254), unique=True, nullable=False, index=True)
    username      = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin      = db.Column(db.Boolean, default=False, nullable=False)
    is_active     = db.Column(db.Boolean, default=True, nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login    = db.Column(db.DateTime, nullable=True)

    # Relationships
    orders         = db.relationship('Order', backref='customer', lazy='dynamic')
    reviews        = db.relationship('Review', backref='author', lazy='dynamic')
    wishlist_items = db.relationship('WishlistItem', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


# ==========================================================================
# ARTIST
# Optional — used for the Featured Artist page and heady product attribution.
# Products reference artist_id when a full artist record exists.
# ==========================================================================

class Artist(db.Model):
    __tablename__ = 'artists'

    id               = db.Column(db.Integer, primary_key=True)
    name             = db.Column(db.String(128), nullable=False, index=True)
    slug             = db.Column(db.String(128), unique=True, nullable=False, index=True)
    bio              = db.Column(db.Text, nullable=True)
    instagram_handle = db.Column(db.String(64), nullable=True)
    is_active        = db.Column(db.Boolean, default=True, nullable=False)
    is_archived      = db.Column(db.Boolean, default=False, nullable=False)
    is_featured      = db.Column(db.Boolean, default=False, nullable=False)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Artist {self.name}>'


# ==========================================================================
# PRODUCT
# ==========================================================================

class Product(db.Model):
    __tablename__ = 'products'

    id                   = db.Column(db.Integer, primary_key=True)
    name                 = db.Column(db.String(256), nullable=False)
    slug                 = db.Column(db.String(256), unique=True, nullable=False, index=True)
    description          = db.Column(db.Text, nullable=False, default='')

    # heady / prodo / vape
    product_type         = db.Column(db.String(16), nullable=False, index=True)

    # Subcategory — used by prodo and vape to group products into page sections.
    # prodo:  dry-pipes | bubblers | beakers | oil-rigs
    # vape:   vaporizers | flower-accessories | oil-accessories
    subcategory          = db.Column(db.String(32), nullable=True)

    # Pricing
    price_cents          = db.Column(db.Integer, nullable=False)
    original_price_cents = db.Column(db.Integer, nullable=True)
    discount_start       = db.Column(db.DateTime, nullable=True)
    discount_end         = db.Column(db.DateTime, nullable=True)

    # Artist / credit
    # artist_id is set when a full Artist record exists (heady pieces).
    # credit and credit_label are used for prodo/vape where no Artist record exists.
    artist_id            = db.Column(
                               db.Integer,
                               db.ForeignKey('artists.id'),
                               nullable=True,
                               index=True,
                           )
    credit_label         = db.Column(db.String(32), nullable=True)
    credit               = db.Column(db.String(128), nullable=True)
    instagram            = db.Column(db.String(64), nullable=True)

    # Specs — shared
    technique            = db.Column(db.String(256), nullable=True)
    height               = db.Column(db.String(32), nullable=True)
    joint_size           = db.Column(db.String(16), nullable=True)
    thickness            = db.Column(db.String(32), nullable=True)

    # Heady-specific
    series               = db.Column(db.String(128), nullable=True)
    glass_type           = db.Column(db.String(64), nullable=True)
    glass_color          = db.Column(db.String(64), nullable=True)
    glass_color_company  = db.Column(db.String(64), nullable=True)
    gemstones            = db.Column(db.Boolean, default=False, nullable=False)
    electroform          = db.Column(db.Boolean, default=False, nullable=False)
    fume                 = db.Column(db.Boolean, default=False, nullable=False)
    collab               = db.Column(db.String(128), nullable=True)

    # Prodo-specific
    perc                 = db.Column(db.String(64), nullable=True)
    reclaimer            = db.Column(db.Boolean, default=False, nullable=False)
    includes             = db.Column(db.String(256), nullable=True)

    # Vape/Accessory-specific
    metal_type           = db.Column(db.String(64), nullable=True)
    is_premium           = db.Column(db.Boolean, default=False, nullable=False)

    # Variant options e.g. ['Red', 'Blue', 'Green'] — stored as JSON
    variants_json        = db.Column(db.Text, nullable=True)

    # Attribute tags e.g. ['convection', 'dual-use'] — stored as JSON
    attributes_json      = db.Column(db.Text, nullable=True)

    # Business
    # outright | consignment
    acquisition_type     = db.Column(
                               db.String(16), nullable=False, default='outright'
                           )
    consignment_rate     = db.Column(db.Numeric(5, 2), nullable=True)
    consignment_paid     = db.Column(db.Boolean, nullable=True)
    sku                  = db.Column(db.String(64), unique=True, nullable=True)

    # Status
    is_sold              = db.Column(db.Boolean, default=False, nullable=False)
    is_active            = db.Column(db.Boolean, default=True, nullable=False)

    # Primary image path (static-relative) and SEO
    primary_image        = db.Column(db.String(512), nullable=True)
    meta_description     = db.Column(db.String(320), nullable=True)

    created_at           = db.Column(
                               db.DateTime, default=datetime.utcnow, nullable=False
                           )
    updated_at           = db.Column(
                               db.DateTime,
                               default=datetime.utcnow,
                               onupdate=datetime.utcnow,
                               nullable=False,
                           )

    # Relationships
    artist       = db.relationship('Artist', backref='products', lazy='select')
    images       = db.relationship(
                       'ProductImage',
                       backref='product',
                       lazy='select',
                       cascade='all, delete-orphan',
                       order_by='ProductImage.sort_order',
                   )

    @property
    def variants(self):
        if self.variants_json:
            return json.loads(self.variants_json)
        return None

    @property
    def attributes(self):
        if self.attributes_json:
            return json.loads(self.attributes_json)
        return None

    def __repr__(self):
        return f'<Product {self.slug}>'


# ==========================================================================
# PRODUCT IMAGE
# One row per image. sort_order 0 = primary.
# ==========================================================================

class ProductImage(db.Model):
    __tablename__ = 'product_images'

    id         = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
                     db.Integer,
                     db.ForeignKey('products.id'),
                     nullable=False,
                     index=True,
                 )
    image_url  = db.Column(db.String(512), nullable=False)
    alt_text   = db.Column(db.String(256), nullable=False, default='')
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<ProductImage product={self.product_id} order={self.sort_order}>'


# ==========================================================================
# ORDER
# ==========================================================================

class Order(db.Model):
    __tablename__ = 'orders'

    id      = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
                  db.Integer,
                  db.ForeignKey('users.id'),
                  nullable=True,
                  index=True,
              )

    # pending → paid → shipped → delivered → cancelled / refunded
    status  = db.Column(
                  db.String(16), nullable=False, default='pending', index=True
              )

    # Stripe references — Stripe owns payment data, we store references only
    stripe_payment_intent_id = db.Column(
                                   db.String(256), nullable=True, unique=True
                               )
    stripe_charge_id         = db.Column(db.String(256), nullable=True)

    # Discount
    discount_code_id      = db.Column(
                                db.Integer,
                                db.ForeignKey('discount_codes.id'),
                                nullable=True,
                            )
    discount_amount_cents = db.Column(db.Integer, default=0, nullable=False)

    # Totals in cents
    subtotal_cents = db.Column(db.Integer, nullable=False, default=0)
    shipping_cents = db.Column(db.Integer, nullable=False, default=0)
    total_cents    = db.Column(db.Integer, nullable=False, default=0)

    # Shipping address
    shipping_name      = db.Column(db.String(256), nullable=True)
    shipping_address_1 = db.Column(db.String(256), nullable=True)
    shipping_address_2 = db.Column(db.String(256), nullable=True)
    shipping_city      = db.Column(db.String(128), nullable=True)
    shipping_state     = db.Column(db.String(64), nullable=True)
    shipping_zip       = db.Column(db.String(16), nullable=True)
    shipping_country   = db.Column(db.String(64), default='US', nullable=True)

    # Fulfilment
    tracking_number = db.Column(db.String(256), nullable=True)
    shipped_at      = db.Column(db.DateTime, nullable=True)
    notes           = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
                     db.DateTime,
                     default=datetime.utcnow,
                     onupdate=datetime.utcnow,
                     nullable=False,
                 )

    # Relationships
    items = db.relationship(
                'OrderItem',
                backref='order',
                lazy='dynamic',
                cascade='all, delete-orphan',
            )

    @property
    def total_dollars(self):
        return self.total_cents / 100

    def __repr__(self):
        return f'<Order {self.id} — {self.status}>'


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id         = db.Column(db.Integer, primary_key=True)
    order_id   = db.Column(
                     db.Integer,
                     db.ForeignKey('orders.id'),
                     nullable=False,
                     index=True,
                 )
    product_id = db.Column(
                     db.Integer,
                     db.ForeignKey('products.id'),
                     nullable=False,
                     index=True,
                 )
    quantity   = db.Column(db.Integer, nullable=False, default=1)
    # Price snapshot at time of purchase — never recalculate from current product price
    price_cents = db.Column(db.Integer, nullable=False)

    @property
    def price_dollars(self):
        return self.price_cents / 100

    @property
    def line_total_cents(self):
        return self.price_cents * self.quantity

    def __repr__(self):
        return f'<OrderItem order={self.order_id} product={self.product_id}>'


# ==========================================================================
# REVIEW
# Reviews apply to prodo pieces only.
# ==========================================================================

class Review(db.Model):
    __tablename__ = 'reviews'

    id                = db.Column(db.Integer, primary_key=True)
    product_id        = db.Column(
                            db.Integer,
                            db.ForeignKey('products.id'),
                            nullable=False,
                            index=True,
                        )
    user_id           = db.Column(
                            db.Integer,
                            db.ForeignKey('users.id'),
                            nullable=False,
                            index=True,
                        )
    rating            = db.Column(db.Integer, nullable=False)
    title             = db.Column(db.String(128), nullable=True)
    body              = db.Column(db.Text, nullable=False)
    verified_purchase = db.Column(db.Boolean, default=False, nullable=False)
    is_approved       = db.Column(db.Boolean, default=False, nullable=False)
    is_flagged        = db.Column(db.Boolean, default=False, nullable=False)
    created_at        = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Review {self.id} — {self.rating} stars>'


# ==========================================================================
# WISHLIST
# ==========================================================================

class WishlistItem(db.Model):
    __tablename__ = 'wishlist_items'

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(
                     db.Integer,
                     db.ForeignKey('users.id'),
                     nullable=False,
                     index=True,
                 )
    product_id = db.Column(
                     db.Integer,
                     db.ForeignKey('products.id'),
                     nullable=False,
                     index=True,
                 )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        db.UniqueConstraint(
            'user_id', 'product_id', name='uq_wishlist_user_product'
        ),
    )

    def __repr__(self):
        return f'<WishlistItem user={self.user_id} product={self.product_id}>'


# ==========================================================================
# DISCOUNT CODE
# ==========================================================================

class DiscountCode(db.Model):
    __tablename__ = 'discount_codes'

    id                      = db.Column(db.Integer, primary_key=True)
    code                    = db.Column(
                                  db.String(64), unique=True, nullable=False, index=True
                              )
    # percentage | fixed
    discount_type           = db.Column(db.String(16), nullable=False)
    discount_value          = db.Column(db.Numeric(10, 2), nullable=False)
    valid_from              = db.Column(db.DateTime, nullable=True)
    valid_until             = db.Column(db.DateTime, nullable=True)
    max_uses                = db.Column(db.Integer, nullable=True)
    times_used              = db.Column(db.Integer, default=0, nullable=False)
    single_use_per_customer = db.Column(db.Boolean, default=False, nullable=False)
    is_active               = db.Column(db.Boolean, default=True, nullable=False)
    created_at              = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    orders = db.relationship('Order', backref='discount_code', lazy='dynamic')

    @property
    def is_valid(self):
        now = datetime.utcnow()
        if not self.is_active:
            return False
        if self.valid_from and now < self.valid_from:
            return False
        if self.valid_until and now > self.valid_until:
            return False
        if self.max_uses and self.times_used >= self.max_uses:
            return False
        return True

    def __repr__(self):
        return f'<DiscountCode {self.code}>'
