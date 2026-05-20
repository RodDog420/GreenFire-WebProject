# Green Fire — American Functional Glass

E-commerce and gallery web application for **Green Fire**, a functional glass gallery located in the University Place Creative District, Lincoln, Nebraska. Formerly a licensed adult-use retailer in Seattle for over a decade, Green Fire carries American-made heady glass and production pieces sourced directly from artists.

**Live site:** [greenfireglass.com](https://greenfireglass.com)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3 / Flask |
| Database | PostgreSQL (Render managed) |
| ORM | SQLAlchemy + Flask-Migrate |
| Templating | Jinja2 |
| Auth | Flask-Login |
| Forms / CSRF | Flask-WTF |
| Email | Flask-Mail (Gmail SMTP) |
| Security | Flask-Talisman (CSP, HSTS, security headers) |
| Rate limiting | Flask-Limiter |
| AI chat | Anthropic Claude API |
| Hosting | Render (paid tier, warm instance) |
| Frontend | Vanilla JS, custom CSS — no frameworks |

---

## Features

### Public Storefront
- **Heady glass catalogue** — one-of-a-kind and limited-run artist pieces with individual product detail pages, image lightbox, and full product metadata
- **Production glass catalogue** — sectioned by subcategory (dry pipes, bubblers, beakers, oil rigs) with anchor navigation
- **Vapes and accessories catalogue** — sectioned by subcategory (vaporizers, flower accessories, oil accessories)
- **Archive** — permanent record of sold heady pieces
- **Featured artist** — rotating spotlight page for a specific artist
- **Artist-direct sourcing** — all inventory sourced from artists the owner knows personally

### E-Commerce
- Shopping cart with session-based persistence
- Checkout flow with payment processing integration
- Order confirmation and history
- Customer accounts with wishlist
- Notify-me alerts for out-of-stock items
- Shipping rates by order subtotal — free shipping over $150

### AI Chat Assistant
- **Penny** — an AI chat agent powered by the Anthropic Claude API, embedded on every page
- Knows the inventory, glass terminology, artists, and techniques
- Designed for real customer service — not a generic chatbot

### Admin Panel
- Full inventory management — add, edit, delete products
- Image manager — multiple images per product with primary image designation
- Display order control — manual sort order with subcategory reference panel
- Product activation / deactivation (sold toggle)
- Inventory backup and restore (JSON)

### Security
- Flask-Talisman with strict Content Security Policy
- CSRF protection on all forms (Flask-WTF)
- Secure, HttpOnly, SameSite session cookies
- Per-endpoint rate limiting
- Admin routes protected by role assertion
- 21+ age gate on entry
- Passwords hashed with Werkzeug — never stored plaintext
- No payment card data ever touches the application

---

## Project Structure

```
greenfire-webproject/
├── app/
│   ├── __init__.py          # App factory — extensions, blueprints, Talisman CSP
│   ├── models.py            # All database models
│   ├── routes/
│   │   ├── routes.py        # All public routes
│   │   └── admin.py         # Admin-only routes
│   ├── static/
│   │   ├── css/
│   │   │   ├── variables.css    # Color variables and --nav-height only
│   │   │   ├── base.css         # Reset, typography, global + page-specific
│   │   │   ├── components.css   # Buttons, cards, shared UI
│   │   │   ├── navigation.css   # Nav bar, hamburger, dropdowns
│   │   │   └── admin.css        # Admin interface
│   │   ├── js/
│   │   │   ├── nav.js           # Hamburger, dropdowns, iOS Safari safe
│   │   │   ├── age-gate.js      # Age gate logic
│   │   │   ├── chat.js          # Penny chat UI
│   │   │   ├── checkout.js      # Checkout payment form
│   │   │   └── admin.js         # Admin form: slug, field visibility, display order
│   │   └── images/
│   └── templates/           # Flat — no subfolders. Nav and footer inline in base.html.
├── migrations/
├── config.py                # Config and DevConfig classes
├── greenfire.py             # Flask entry point
├── .flaskenv                # FLASK_APP, FLASK_DEBUG
└── requirements.txt
```

---

## Local Development Setup

### Prerequisites
- Python 3.10+
- PostgreSQL (local instance or Render dev database)
- Git

### Steps

```bash
# Clone the repo
git clone https://github.com/RodDog420/GreenFire-WebProject.git
cd GreenFire-WebProject

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Create your .env file (see Environment Variables below)
cp .env.example .env

# Run database migrations
flask db upgrade

# Start the development server
flask run --port 5001 --with-threads
```

Visit `http://localhost:5001`

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the values. Never commit `.env`.

| Variable | Description |
|---|---|
| `SECRET_KEY` | Flask secret key — use a long random string |
| `DATABASE_URL` | PostgreSQL connection string |
| `ANTHROPIC_API_KEY` | Anthropic API key for Penny chat |
| `MAIL_USERNAME` | Gmail address for outbound email |
| `MAIL_PASSWORD` | Gmail app password (not account password) |
| `MAIL_DEFAULT_SENDER` | Display name + address for sent mail |
| `STRIPE_PUBLIC_KEY` | Stripe publishable key (payment integration) |
| `STRIPE_SECRET_KEY` | Stripe secret key |

---

## CSS Architecture

All styling is written in plain CSS — no Sass, no Tailwind, no utility framework. The architecture follows a strict set of conventions:

- **`variables.css`** — color custom properties and `--nav-height` only. Nothing else.
- **`base.css`** — reset, typography, global defaults. Page-specific rules appended at the bottom under labeled section headers.
- **`components.css`** — buttons, cards, badges, forms, chat UI.
- **`navigation.css`** — nav bar, hamburger menu, dropdowns.

Mobile-first. Base styles target 320px. All breakpoints in `rem`, never `px`. No inline styles. No `!important`.

---

## Deployment

The site deploys automatically to [Render](https://render.com) on every push to `main`. Render manages the PostgreSQL database and all environment variables. No build step required — Render detects the Flask app and runs it via Gunicorn.

---

## License

Proprietary. All rights reserved. Green Fire LLC, Lincoln, Nebraska.
