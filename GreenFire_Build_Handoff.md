# Green Fire — Build Session Handoff
## Next Build Session — Product Catalogue Pages

---

## BEFORE YOU TOUCH ANYTHING

Read these documents in this order before starting any work:
1. `CLAUDE.md` (project root) — methodology, CSS conventions, cardinal rules
2. `FlaskApp_Landing_Page_Instructions.docx` — landing page and base.html recipe
3. `Navigation_Bar_Composition_Ordering.docx` — nav bar recipe

**The owner must explicitly approve every proposed build step before you begin it.
Do not build, scaffold, or generate any file without first stating what you intend
to do and receiving explicit confirmation. This is non-negotiable.**

---

## Current File Tree (Confirmed Clean)

```
greenFire-WebProject/
+--- app/
|    +--- __init__.py
|    +--- models.py
|    +--- routes/
|    |    +--- routes.py
|    |    +--- admin.py
|    +--- static/
|    |    +--- css/
|    |    |    +--- variables.css
|    |    |    +--- base.css
|    |    |    +--- components.css
|    |    |    +--- navigation.css
|    |    +--- images/
|    |    |    +--- accessories/
|    |    |    +--- archive/
|    |    |    +--- edited/
|    |    |    +--- heady/
|    |    |    +--- logos/
|    |    |    +--- prodo/
|    |    +--- js/
|    |         +--- age-gate.js
|    |         +--- chat.js
|    |         +--- nav.js
|    +--- templates/
|         +--- base.html          ← fully built, nav + footer inline
|         +--- index.html         ← fully built landing page
|         +--- heady_glass.html   ← stub
|         +--- prodo_pieces.html  ← stub
|         +--- vapes_accessories.html ← stub
|         +--- product.html       ← stub
|         +--- archive.html       ← stub
|         +--- about.html         ← stub
|         +--- artists.html       ← stub
|         +--- cart.html          ← stub
|         +--- account_dashboard.html ← stub
|         +--- account_orders.html    ← stub
|         +--- account_wishlist.html  ← stub
|         +--- admin_dashboard.html   ← stub
|         +--- login.html         ← stub
|         +--- logout.html        ← stub
|         +--- register.html      ← stub
|         +--- contact.html       ← stub
|         +--- privacy.html       ← stub
|         +--- returns.html       ← stub
|         +--- shipping.html      ← stub
|         +--- terms.html         ← stub
+--- migrations/
+--- CLAUDE.md
+--- greenfire.py
+--- config.py
+--- requirements.txt
+--- .flaskenv
+--- .env
+--- .gitignore
```

---

## What Is Built and Working

- Full Flask scaffold — app factory, blueprints, config, greenfire.py, .flaskenv
- PostgreSQL models in models.py — User, Artist, Product, ProductImage, Order,
  OrderItem, Review, WishlistItem, DiscountCode (defined but NOT migrated — no
  tables exist yet, database setup is handled in a separate chat)
- All routes registered in routes.py and admin.py — serving stubs or built templates
- Full CSS design system:
  - variables.css — colors only + --nav-height
  - base.css — reset, typography, global defaults, page-specific at bottom
  - components.css — buttons, badges, cards, chat bubble, age gate, modal
  - navigation.css — nav bar, hamburger, dropdowns
- base.html — age gate, sticky nav (position: sticky + overflow-x: clip), footer,
  chat bubble, color dictionary in HTML comment at bottom
- index.html — landing page fully built: hero, heady glass, prodo glass, location sections
- Domain: greenfireglass.com registered at Namecheap

---

## CSS Color System — Know This Before Touching Any CSS

Colors live in variables.css only. No semantic alias layer — direct color variables only.
The color dictionary in base.html lists every color with its hex value. VS Code shows
color swatches next to hex values — use this to know what you're looking at.

Key colors:
- `--color-dark-section: #3E473B` — hero, prodo sections, dark split sections
- `--color-nav-dark: #2A302A` — nav bar, footer, dropdown panels
- `--color-forest-green: #3A6B1A` — primary brand, buttons, links
- `--color-burnt-orange: #C4622D` — accent CTAs, chat bubble

---

## DATABASE NOTE

The database does NOT exist yet. Tables have not been migrated. All database-dependent
features (product pages, cart, auth, admin) require the DB to be set up first.
DB setup is handled in a separate chat. Do not attempt to run migrations or build
DB-dependent features in this session unless the owner confirms the DB is live.

When the DB is ready, run:
```
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

---

## PRE-BUILD DECISION: Slug Architecture (CONFIRMED)

All products — headies AND prodos — use a single universal route:

```
/product/<slug>
```

One route, one template (product.html), handles everything. The Product model has a
`product_type` field ('heady' or 'prodo'). The template uses Jinja2 conditionals to
render heady-specific or prodo-specific elements. Slugs generated from artist name +
piece name: e.g. `/product/josh-mann-uptake-rig`, `/product/us-tubes-beaker-14mm`.

Catalogue listing pages (/headies, /prodos) filter by product_type. All individual
product detail pages live under /product/.

This is confirmed and locked. Do not propose an alternative without flagging it first.

---

## PRIMARY BUILD TASK: Product Catalogue Pages

Build in this order. Confirm each step with the owner before starting it.

### Step 1 — /headies catalogue page (heady_glass.html)

Card grid of all heady pieces. Each card contains:
- Single product photo
- Artist name (if known)
- Price
- "Sold" badge — pill-style overlay on photo corner, NOT a diagonal ribbon
- Click anywhere on card → /product/<slug>

Sorted alphabetically by artist name. Unknown/unsigned pieces sort at end under
"Various Artists". Admin can set sort_order integer or featured boolean.

### Step 2 — /prodos catalogue page (prodo_pieces.html)

Same card grid pattern as headies but sectioned with anchor links:
- #dry-pipes
- #bubblers
- #beakers
- #oil-rigs

Nav subcategory links use anchor links: `/prodos#dry-pipes` etc.

Each section has an id matching its anchor. Prodo cards show star rating summary
if reviews exist.

### Step 3 — /vapes-accessories page (vapes_accessories.html)

Same sectioned pattern as prodos:
- #vaporizers
- #flower-accessories
- #oil-accessories

### Step 4 — /product/<slug> universal detail page (product.html)

One template handles heady and prodo via Jinja2 conditionals.
No empty spaces — if a field has no content, the element does not render.

**Left side — Photo gallery:**
- Vertical thumbnail strip on far left — only renders if product has 2+ images
- Large primary image in center
- Clicking a thumbnail swaps the primary image (vanilla JS)
- Zoom on hover: lens-style, small lens box on image, zoomed panel beside it
- If only one photo: just the large image, no thumbnail strip

**Right side — Product info (all fields optional, none render if empty):**
- Artist name
- Instagram link — clickable icon, only renders if present
- Height — e.g. "8 inches"
- Brief description — one or two lines max
- Price
- Add to cart button
- Wishlist button
- Prodo only: star rating + review count near price

**Below product info:**
- "Back to [category]" breadcrumb
- Previous / Next navigation — moves through alphabetically sorted catalogue
- Share button — copies URL to clipboard
- Heady sold pieces: "Notify me if this artist returns" replaces add to cart

**Sold state:**
- "Sold" pill badge overlaid on primary photo top-left corner
- Page remains accessible when sold — does not 404
- Add to cart replaced with sold messaging
- Sold heady pieces automatically appear in /archive — no manual step

### Step 5 — /archive page (archive.html)

All sold pieces displayed permanently. Same card grid and product detail layout
as active catalogue. "Sold" badge always shown. "Notify me if this artist returns"
on every piece. Sorted alphabetically by artist name. Massive SEO value.

---

## OPEN DECISIONS — Resolve Before Building Blocked Features

These are unresolved. Do not build the blocked feature until the owner decides.
Present each as a clear choice with tradeoffs — do not advocate for one option
without being asked.

**1. Instagram embed approach**
Blocks: Featured Artist page (Josh Mann, @joshmann_glass)
Options: Meta Basic Display API (free, complex) vs third-party service like
Curator.io (~$25/month, easy). Not urgent for current build session.

**2. Analytics**
Blocks: Deployment
Options: Google Analytics (free, sends data to Google) vs Plausible/Fathom
(~$9-19/month, privacy-focused). Decide before going live.

**3. AI chat agent name**
Blocks: Chat feature build
The chat bubble exists visually. The agent needs a display name for the chat
window header. Not yet decided.

**4. Shipping rates**
Blocks: Stripe checkout build
Options: flat rate, free over $X threshold, actual carrier cost by weight/destination.
Must be decided before checkout is built.

**5. Artist terms — consignment vs outright purchase**
Blocks: Finalizing the Product data model
Consignment requires tracking artist percentage and payment status in the database.
Outright purchase does not. Must be confirmed before models are finalized.

**6. POS integration**
Currently manual reconciliation (Option D). No decision needed now.
Revisit when sales volume justifies integration.

---

## REMAINING PAGES TO BUILD (after catalogue)

- about.html — Seattle legacy, relocation story, cannabis heritage, curation philosophy
- Auth pages — login, register, logout (Flask-Login + Flask-WTF)
- Cart + Stripe checkout
- Admin dashboard — products, orders, discount codes, reviews, low stock alerts
- AI chat agent (/api/chat stub exists)
- Featured Artist page — Josh Mann (@joshmann_glass)
- Content for shipping, returns, contact, privacy, terms stubs

---

## ENVIRONMENT VARIABLES REQUIRED (for when DB is live)

```
SECRET_KEY
DATABASE_URL
STRIPE_PUBLIC_KEY
STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET
MAIL_USERNAME
MAIL_PASSWORD
ANTHROPIC_API_KEY
```

---

## BUSINESS CONTEXT (do not invent beyond this)

Green Fire is a premium American Functional Glass shop at 2401 N 48th St,
University Place neighborhood, Lincoln Nebraska — inside the Uni Place Creative
District. The long-term goal is a Nebraska medical cannabis license. The retail
glass shop is both a standalone business and a foundation for that future.

Target customers: Nebraska Wesleyan students and young adults, older heady glass
collectors, cannabis culture demographic.

All glass is American-made. Artist relationships are direct. Curation is selective.

Industry terminology — use exactly as written, do not invent:
- "Heady" — decorated, artistic, high-craft functional glass
- "Prodo" — production glass, regularly produced series
- "Rig" — oil/concentrate pipe
- "Bubbler" — water pipe with built-in water chamber
