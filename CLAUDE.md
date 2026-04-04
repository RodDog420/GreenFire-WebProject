# CLAUDE.md
# Flask Web Design Methodology Primer
# Universal Baseline — All Projects — All Sessions

---

# 1.0 Cardinal Rules

**⚠ Before any work begins:** Confirm the correct file. Ask to see existing code before
assuming a solution does not exist. Read the ENTIRE file before editing any part of it.
Never make assumptions — always ask first. This applies every session without exception.

## 1.1 Before Building Anything Structural

Before building any new folder, file, or architectural element, Claude must state explicitly
what it intends to create, why it is needed, and wait for explicit confirmation before
touching anything.

**⚠ This applies to new folders, new files, new routes, new blueprints, and any change to
the project architecture. Claude proposes. The owner decides.**

## 1.2 Agreed Implementation Approaches Are Binding

When an implementation approach has been explicitly agreed upon, it cannot be changed without
flagging the reason and getting explicit confirmation first. Not mid-build. Not silently.
Not ever.

Real example of a violation: the row-reversal class (.split-inner--reversed) was explicitly
agreed upon as the mechanism for alternating desktop layouts. Mid-build, Claude abandoned it
silently and introduced a dual-image approach without flagging the change. This caused hours
of rework.

## 1.3 Do Not Invent Industry-Specific Names or Assumptions

- Never guess at industry-specific terminology, naming conventions, or product categories
- Ask the owner for naming conventions before creating routes, templates, or database fields
  that carry business meaning
- Never argue that an invented name is correct or a best practice — it is an assumption

**⚠ If Claude is uncertain what something should be called: ask. Do not guess and then
defend the guess.**

## 1.4 Arbitrary Assumptions Are Not Best Practices

When the owner questions a decision, Claude must honestly assess whether it is a genuine
best practice or an assumption. If it is an assumption, Claude acknowledges it immediately
and defers. Claude never suggests the owner may have a memory problem as a way of defending
an arbitrary choice.

## 1.5 Session Sync Checklist — Required After Every Build Session

At the end of every build session, Claude must produce an explicit sync checklist containing
every file created or changed, its exact destination path, and confirmation that the owner
has placed it before proceeding.

**⚠ Never assume a file was placed. Never proceed to the next feature without confirming
sync.**

## 1.6 Teaching vs Deferring

- **Code quality, maintainability, standards** → Teach proactively
- **Personal workflow, naming, organisation** → Ask first
- **Unclear** → Ask first

## 1.7 When in Doubt, Dig Deep Before Responding

When a problem cannot be diagnosed from the surface, Claude must read every relevant file
completely and reason systematically from what is actually there — before offering any
suggestion. Offering plausible-sounding guesses, asking the owner to repeat tests already
completed, or deflecting to caching and environmental factors are not acceptable substitutes
for thorough analysis.

The correct sequence when facing a difficult problem:
1. Read all relevant files in full
2. Search for the specific property or rule causing the issue
3. Reason from evidence to a single specific diagnosis
4. Propose that diagnosis and the fix — one clear proposal, not a series of darts

If thorough analysis does not yield a diagnosis, say so honestly rather than continuing to
guess. Do not wait for the owner to express frustration before digging deep. Dig deep
the first time.

---

# 2.0 Project Structure, File Naming & Organisation

## 2.1 The App Folder

**⚠ The Flask application package is always named `app`. Never anything else.**

## 2.2 The Entry Point File

**⚠ The Flask entry point is always named after the project (e.g. `greenfire.py`).
A `.flaskenv` file tells Flask where to find it.**

## 2.3 File Count Philosophy — Fewer Files, Longer Files

The default instinct should always be consolidation, not proliferation. Push files out
vertically (longer), not horizontally (more files).

- Routes: consolidate into the fewest blueprints that make logical sense. Two files
  (`routes.py` and `admin.py`) is usually sufficient.
- Models: all database models in one `models.py` file. Not a `models/` subdirectory.
- Templates: flat structure inside `templates/`. No subfolders. Nav and footer live
  inline in `base.html`.
- CSS: page-specific styles appended to bottom of `base.css` with a clear section header.

**⚠ The owner decides how routes, models, and templates are split. Claude proposes —
the owner confirms.**

## 2.4 Standard Project Structure

Claude must present this complete diagram at the start of every new project before creating
any files. The owner must confirm before any files are built.

```
projectname/
+--- app/                          <- Flask app package. Always named app.
|    +--- __init__.py              <- app factory: create_app()
|    +--- models.py                <- ALL database models in one file
|    +--- routes/
|    |    +--- __init__.py         <- empty
|    |    +--- routes.py           <- all public routes, auth, cart, account, chat
|    |    +--- admin.py            <- admin-only routes, login_required
|    +--- static/
|    |    +--- css/
|    |    |    +--- variables.css  <- COLOURS ONLY + --nav-height
|    |    |    +--- base.css       <- reset, typography, global + page-specific at bottom
|    |    |    +--- components.css <- buttons, cards, shared UI
|    |    |    +--- navigation.css <- nav bar, hamburger, dropdowns
|    |    +--- js/
|    |    +--- images/
|    +--- templates/               <- FLAT. No subfolders. Nav and footer inline in base.html.
|         +--- base.html           <- master template
|         +--- [all other templates, flat]
+--- migrations/
+--- venv/
+--- [projectname].py              <- entry point
+--- config.py
+--- requirements.txt              <- generated by pip freeze, NEVER created manually
+--- .flaskenv                     <- safe to commit
+--- .env                          <- NEVER commit
+--- .env.example
+--- .gitignore                    <- created FIRST
```

## 2.5 Ask Before Creating Sub-Folders

Sub-folders add navigational complexity. Claude must never create a new sub-folder without
proposing it first and receiving explicit owner approval.

## 2.6 The .gitignore File

**⚠ Create .gitignore before anything else.**

```
venv/
__pycache__/
*.pyc
*.pyo
.env
instance/
.idea/
*.egg-info/
dist/
build/
.DS_Store
_norton_/
```

## 2.7 The Two Environment Files

**.flaskenv — Flask CLI configuration. Safe to commit.**
```
FLASK_APP=greenfire.py
FLASK_DEBUG=1
FLASK_ENV=development
```

**.env — Runtime secrets. NEVER commit.**

**⚠ Both files must be created at the start of every project. Neither is optional.**

---

# 3.0 New Project Startup Order

- Step 1  — Present complete folder diagram and get confirmation
- Step 2  — Create `.gitignore` first
- Step 3  — Create folder structure
- Step 4  — Create `.flaskenv` and `.env.example`
- Step 5  — Create `config.py` and entry point
- Step 6  — Create `app/__init__.py`
- Step 7  — Create all CSS files in correct order (`variables.css` first)
- Step 8  — Create `base.html` with nav and footer inline
- Step 9  — Create route stub files and stub templates
- Step 10 — Create `models.py`
- Step 11 — Install dependencies, then `pip freeze > requirements.txt`
- Step 12 — Confirm `flask run` works before proceeding to features

**⚠ `requirements.txt` is generated by `pip freeze` after all packages are installed —
never created manually.**

---

# 4.0 CSS File Architecture

## 4.1 File Structure

All styling lives in CSS files. Inline styles permitted only in rare cases where genuinely
better — less than 1% of all styling decisions.

```
static/css/
+--- variables.css   <- COLOURS ONLY + --nav-height. Nothing else.
+--- base.css        <- reset, typography, global defaults + page-specific appended at bottom
+--- components.css  <- buttons, badges, cards, forms, chat bubble
+--- navigation.css  <- nav bar, hamburger, dropdowns
```

- `variables.css` is always imported first
- No font declarations in individual page stylesheets — all fonts in `base.css` only
- No colours hardcoded outside of `variables.css` — always reference a variable
- All other values (spacing, typography, shadows, transitions, z-index, border-radius)
  are hardcoded directly in their CSS class
- Page-specific CSS is appended to the bottom of `base.css` with a clearly labelled
  section header

## 4.2 CSS Variables Philosophy — Colours and Coupling Agents Only

CSS custom properties (variables) are used for two purposes only:

- **Colours** — all `--color-*` variables live in `variables.css`. Color changes are brand
  decisions that should propagate everywhere simultaneously.
- **`--nav-height`** — kept as a coupling agent. The mobile dropdown panel must always sit
  exactly at the bottom of the nav bar. Both rules reference `--nav-height` so they always
  agree.

Everything else — spacing, font sizes, font weights, line heights, letter spacing, shadows,
transitions, border radius, z-index, max-widths — is hardcoded directly as explicit values
in the CSS class that uses them.

**Why not spacing variables?**
Spacing is sensitive and page-by-page. A spacing variable used in 15 places becomes a
liability the moment one of those 15 places needs to be different. Explicit values give
maximum control with no hidden dependencies.

**Why not z-index variables?**
Z-index values are documented in a Z-index dictionary as a commented-out block in `base.html`
alongside the color dictionary. This provides a readable reference without making z-index
values into shared dependencies.

**⚠ Never create spacing, typography, shadow, transition, or z-index variables. If uncertain
whether a variable is justified, ask: is this a coupling relationship where two separate rules
must always agree? If yes, a variable may be warranted. If no, hardcode it.**

## 4.3 Colour System — Variables + Dictionary

All colour variables defined in `variables.css`. Every main colour must have a corresponding
hover variant. A human-readable colour dictionary lives as a comment at the bottom of
`base.html`. VS Code shows color swatches next to hex values in this dictionary.

**⚠ If a new colour is added anywhere in the project, it must be added to BOTH
`variables.css` AND the `base.html` colour dictionary simultaneously.**

**⚠ No semantic alias layer.** Do not create variables like `--color-btn-primary` that
point to another variable. Reference color variables directly: `var(--color-forest-green)`.
The double-indirection makes DevTools unreadable and debugging painful.

---

# 5.0 Mobile-First Development

## 5.1 Core Philosophy

- Design floor: 320px — test every layout at this width
- Base CSS targets small screens — scale up via min-width breakpoints
- Touch targets: all buttons and links must be at least 44x44px
- No horizontal scroll — test at 320px
- All dropdown options: left-aligned, never centred

## 5.2 Units — Priority Order

- `vw` / `vh` — highest preference
- `rem` — typography and component sizing
- `em` — spacing relative to current element font size
- `px` — only for borders and shadows

**⚠ Never use `px` for breakpoints — use `rem`.**

## 5.3 Standard Breakpoints

Custom breakpoints are permitted when a layout genuinely requires it. Always use rem,
never px.

```css
@media (min-width: 48rem) { ... }  /* Tablet 768px */
@media (min-width: 50rem) { ... }  /* Custom: e.g. nav hamburger breakpoint */
@media (min-width: 64rem) { ... }  /* Desktop 1024px */
@media (min-width: 90rem) { ... }  /* Wide 1440px */
```

## 5.4 Baseline Alignment for Grouped Labels

When nav tabs, footer columns, or any grouped headings have different line counts, all items
must align their first line to a common baseline.

The structural solution: give every single-line label a phantom second line using a
non-breaking space. This makes all containers structurally equal height.

```html
<!-- Two-line label: natural -->
<button class="nav-dropdown-trigger">Heady<br>Glass</button>

<!-- One-line label: add phantom second line -->
<button class="nav-dropdown-trigger">Account<br>&nbsp;</button>
```

NOTE: This is a design decision, not a hack. Apply universally to nav tabs, footer column
headings, and any grouped label set where line counts vary.

## 5.5 Media Query Override Safety Rule

When a wider breakpoint (64rem) overrides a narrower one (48rem), never use the CSS padding
shorthand. The shorthand resets ALL four sides, wiping out top padding set by the earlier
query.

```css
/* WRONG - wipes out padding-top */
padding: 0 1rem;

/* CORRECT - preserves padding-top */
padding-top: 1rem;
padding-left: 1rem;
padding-right: 1rem;
```

## 5.6 Scrollbar and Overflow Rules — Apply to Every Project

**⚠ Always add `overflow-y: scroll` to the `html` element. Never add `overflow-x: hidden`
to `body`. Always add `overflow-x: clip` to `.nav`.**

### overflow-y: scroll on html — always required

Without this, the vertical scrollbar appears and disappears based on content height. Each
time it appears it steals 15-17px from the content width, causing dark background sections
to appear not to reach the right edge of the screen at mid-range viewport widths (800px-1200px).

```css
html {
    overflow-y: scroll;
}
```

### overflow-x: hidden on body — never use

```css
/* WRONG - breaks sticky nav */
body { overflow-x: hidden; }
```

If horizontal overflow needs to be controlled, apply `overflow-x: hidden` to a specific
section or wrapper element, not to `body` or `html`.

### overflow-x: clip on .nav — always required

The mobile nav panel (.nav-links) uses `position: absolute`. `position: sticky` on `.nav`
does not establish a containing block for absolutely positioned children. Without
containment, `.nav-links` can extend beyond the viewport at certain widths, causing
horizontal overflow across the entire page — dark sections appear not to reach the right
edge, a horizontal scrollbar appears, and spacing irregularities occur at mid-range widths.

```css
.nav {
    position: sticky;
    top: 0;
    overflow-x: clip; /* contains absolutely positioned .nav-links */
}
```

Use `clip` not `hidden`. `overflow: hidden` creates a new scroll container which breaks
`position: sticky`. `overflow-x: clip` cuts off horizontal bleed without creating a scroll
container and without clipping dropdown menus which extend downward.

### How to recognise the scrollbar problem

- **Symptom** — dark background sections do not reach the right edge at certain viewport widths
- **Confusing detail** — DevTools shows the section width equals the viewport width
- **Confusing detail** — beige sections look fine because they match the body background
- **Confusing detail** — only appears at mid-range widths, not at very small or very large
- **Diagnosis** — the scrollbar is consuming 15-17px on the right edge
- **Fix** — add `overflow-y: scroll` to `html`

---

# 6.0 The clamp() Function

## 6.1 When TO Use clamp()

- Single property scaling smoothly across screen sizes
- Font sizes, container widths, padding, gap values

```css
font-size: clamp(1rem, 2.5vw, 2rem);
```

## 6.2 When NOT to Use clamp()

When already writing targeted per-side values at specific breakpoints — you already have
control. Adding `clamp()` creates unnecessary complexity.

**Default to `clamp()` for typography and generic sizing. Use explicit media queries for
surgical per-side precision.**

---

# 7.0 CSS Class Reuse — The Balancing Act

**Err toward creating new classes. The cost of a redundant class is low. The cost of a
cascading break is high.**

## 7.1 When to Reuse

- Same visual intent, same structural role
- Pages unlikely to diverge visually
- Reusing would not require overrides

## 7.2 When to Create a New Class

- Section will evolve differently over time
- Would require overrides to undo the existing class
- Page-specific with any chance of diverging
- Uncertain — always create new

## 7.3 Scoped Overrides

```css
.media-link-card .content-footer { flex-wrap: nowrap; }
```

Always document scoped overrides with a comment naming the page or context.

---

# 8.0 Typography

- All font declarations live in `base.css` only
- The browser must never supply a default font
- All text is left-aligned by default
- All sizing is `rem` or `em` — never `px` for font sizes

## 8.1 Fluid Typography with clamp()

```css
h1 { font-size: clamp(1.75rem, 5vw, 3rem); }
h2 { font-size: clamp(1.375rem, 4vw, 2.25rem); }
p  { font-size: clamp(1rem, 2vw, 1.125rem); }
```

---

# 9.0 Code Conventions

## 9.1 Inline Styling

**⚠ ALL styling goes in CSS files. Never put styling inline inside HTML.
Before violating this rule: always ask first.**

## 9.2 The TRouBLe Shorthand

Always use four-value shorthand for margin, padding, border-width, border-radius.
Order: Top, Right, Bottom, Left.

```css
margin: 0 0 0.5rem 0;
```

NOTE: Exception: at wider breakpoints that override narrower ones, use explicit per-side
properties to preserve previously set values. See Section 5.5.

## 9.3 No !important

**⚠ Never use `!important`. Resolve specificity conflicts at the source.**

## 9.4 CSS Section Headers

```css
/* ==============================================
   SECTION NAME --- Brief description
   ============================================== */
```

## 9.5 No HTML Comments

Do not add HTML comments to templates unless genuine complexity warrants it. Comments belong
in Python and CSS files.

## 9.6 Container Integrity

- Content must never break out of its container
- Always set `overflow-wrap: break-word` on user-generated content
- Always set `min-width: 0` on grid and flex children that contain text
- Test all containers at 320px before considering complete

## 9.7 Database & Data Integrity

- All queries use SQLAlchemy ORM — never raw SQL unless unavoidable
- Handle all edge cases: division by zero, empty results, null values
- Always ensure correct pluralisation

## 9.8 SEO — Applied to Every Page

- Every template must include: canonical tag, robots meta tag, meta description
- Meta descriptions written per page — never auto-generated
- All images must have descriptive alt text
- URL slugs clean and descriptive — never expose raw database IDs
- Schema.org structured data on product and content pages

## 9.9 HTML Line Length

Keep HTML within 80 characters per line. Write vertically, not horizontally.

---

# 10.0 HTML — Prefer Vertical Layout Over Horizontal

Users interact with Flask applications on narrow screens. Always design HTML structure to be
vertically aligned first. Horizontal layouts should be exceptions that are explicitly
justified, not defaults. Stack elements vertically in the source order — CSS can reorder
them for wider viewports using media queries, but the base structure should read cleanly
from top to bottom without any CSS applied.

In practice: avoid placing sibling elements side by side in raw HTML unless they are
genuinely equivalent in importance and always short in content. If either element could
ever be long, give each its own vertical block.

---

# 11.0 CSS Layout — Grid and Flexbox Conventions

## 11.1 Always Pair max-width with width: 100%

Any container element that uses `max-width` must always have `width: 100%` alongside it.

```css
.container {
    width: 100%;
    max-width: 75rem;
    margin: 0 auto;
}
```

## 11.2 Flexbox + space-between vs Grid

- `justify-content: space-between` creates inherent tension. If one side must never
  overtake the other → use Grid instead.
- **Grid = explicit intent.**

## 11.3 CSS Grid — Two-Column Key-Value Layout

Use case: key-value pairs on mobile, clean and readable at 320px.

```css
.card-grid {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 0.3rem 1rem;
    align-items: start;
}
.card-key   { font-weight: 600; font-size: 0.9rem; }
.card-value { font-size: 0.9rem; text-align: left; word-break: break-word; overflow-wrap: break-word; }
```

- Left column (`1fr`): Keys. Takes all remaining space.
- Right column (`auto`): Values. Sized by widest single line.
- `align-items: start` — prevents key from vertically centering against a multi-line value.
- Why `1fr auto` not `auto auto`: `auto auto` splits space unpredictably. Fixed widths break
  at edge cases. `1fr auto` gives the right column exactly what it needs.

## 11.4 CSS Grid — Right-Aligned Content in Far-Right Column

Use `justify-self: end` on the cell. Do NOT use `margin-left: auto` on a grid child.

```css
.grid-cell-right {
    justify-self: end;
    text-align: left;
    width: auto;
}
```

## 11.5 Flexbox — Never Use flex-shrink: 0

`flex-shrink: 0` pushes siblings out of the container. When user-defined string content is
involved it becomes a weapon against layout integrity. Use `min-width` with a specific value
instead, and let `flex-shrink` default to `1`.

```css
.protected-element {
    min-width: 10ch;
    /* flex-shrink: 1 is the default — do not override */
}
```

## 11.6 Flexbox — Fixed Elements

```css
flex: 0 0 auto;  /* do not grow, do not shrink, size to content */
```

## 11.7 Flexbox — Greedy Space-Filling Elements

```css
flex: 1 1 0;  /* grow to fill, shrink if needed, start from zero */
```

The `0` basis is important — element starts from zero and grows into available space rather
than starting from its content width.

## 11.8 Flexbox — justify-content: space-between Management Rules

- Every flex child must have `min-width: 0`
- Use `overflow-wrap: break-word` on any element with user-defined strings
- Protect fixed-width elements with `min-width` on a specific value, not `flex-shrink: 0`

## 11.9 Flexbox — Scope Rules with :nth-child

When a flex container has multiple rows needing different flex behaviour, use `:nth-child`
to scope rules rather than applying them globally.

```css
.header-row:nth-child(1) .left  { flex: 1 1 auto; }
.header-row:nth-child(2) .left  { flex: 0 0 auto; min-width: 10ch; }
.header-row:nth-child(2) .right { flex: 1 1 0; overflow-wrap: break-word; }
```

---

# 12.0 base.html Template Structure

Nav and footer are written inline inside `base.html` — not as separate partial files.

```html
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta name='description' content='{% block meta_description %}{% endblock %}'>
    <meta name='robots' content='{% block robots %}index, follow{% endblock %}'>
    <link rel='canonical' href='{% block canonical %}{% endblock %}'>
    <title>{% block title %}{% endblock %} — Site Name</title>
    <link rel='stylesheet' href="{{ url_for('static', filename='css/variables.css') }}">
    <link rel='stylesheet' href="{{ url_for('static', filename='css/base.css') }}">
    <link rel='stylesheet' href="{{ url_for('static', filename='css/components.css') }}">
    <link rel='stylesheet' href="{{ url_for('static', filename='css/navigation.css') }}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="nav">... nav inline here ...</nav>
    <main>{% block content %}{% endblock %}</main>
    <footer class="footer">... footer inline here ...</footer>
    {% block extra_js %}{% endblock %}
    <!-- COLOR DICTIONARY --- add all new colours here -->
    <!-- Z-INDEX DICTIONARY --- document all z-index values here -->
</body>
</html>
```

---

# 13.0 Quick Reference — Decision Rules

**Before starting any session**
- Read the entire relevant file before editing any part of it
- Confirm existing code before assuming a solution does not exist
- Ask for naming conventions before creating anything with business meaning

**New project startup — non-negotiable order**
- Folder diagram confirmed → `.gitignore` → structure → `.flaskenv` + `.env.example` →
  `config` → `__init__.py` → CSS (variables first) → `base.html` → routes → models →
  `pip freeze` → confirm `flask run`

**CSS variables — what goes in variables.css?**
- Colors → yes. `--nav-height` → yes. Everything else → hardcode in the CSS class.
- No semantic alias layer — reference color variables directly, never through an alias.

**Overflow and scrollbar — every project**
- `html` → `overflow-y: scroll`
- `body` → NEVER `overflow-x: hidden`
- `.nav` → `overflow-x: clip`

**Teaching or deferring?**
- Code quality, architecture, standards → teach proactively
- Personal workflow, naming, organisation → ask first. Unclear → ask first.

**clamp() or media queries?**
- Single property scaling smoothly → `clamp()`
- Per-side values at specific breakpoints → media queries

**Reuse a class or create new?**
- Same intent, same role, pages unlikely to diverge → reuse
- Would need overrides or uncertain → new class

**Where does styling go?**
- Colours → `variables.css`. `--nav-height` → `variables.css`. Fonts → `base.css`.
- Page-specific → appended to bottom of `base.css` with section header.
- Everything else → hardcoded in the CSS class that uses it.
- Inline styles → only when genuinely the better option, ask first.

**When stuck on a difficult problem**
- Read all relevant files completely first
- Search for the specific property causing the issue
- Reason from evidence to one specific diagnosis
- Propose that diagnosis — do not offer a series of guesses

---

# 14.0 Security Requirements

Security decisions affect the model, routes, auth, and session handling.
Retrofitting security after the fact is painful and error-prone. Every item
below must be considered at the start of a build, not after launch.

Requirements are ordered by severity. Critical items block deployment. High
items must be resolved before public launch. Medium items must be resolved in
the first iteration after launch.

---

## 14.1 Critical — Block Deployment Until Resolved

### Input Sanitisation

All user-supplied strings must be validated, sanitised, or parameterised before
use in database queries, shell commands, file paths, or rendered output.

- Use SQLAlchemy ORM or parameterised queries — never f-strings or string
  concatenation in SQL
- Validate structured data with marshmallow or pydantic
- Sanitise any user-supplied HTML with bleach.clean() using a strict allowlist

### Admin Route Protection

Admin and privileged routes must verify role, not just authentication. A valid
user session must never grant access to admin functionality. Assert role
server-side on every request — never rely on a route being hidden.

```python
@require_role('admin')
def admin_dashboard():
    ...
```

### Token Storage — httpOnly Cookies Only

Auth tokens must never be stored in localStorage. Use httpOnly, Secure, SameSite
cookies exclusively. Add these to Config on day one — before any auth is built:

```python
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'
PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
```

These four lines are not optional. A Flask app without them has insecure sessions
regardless of how well everything else is implemented.

### No Hardcoded Credentials

API keys, secrets, and passwords must never appear in source files, frontend code,
or build artifacts. Credentials extracted from version control history persist
even after removal.

- Use python-dotenv and a .env file locally
- Add .env to .gitignore immediately — on day one, before the first commit
- Use environment variables on the host (Render) in production

### XSS / Output Encoding

Jinja2 auto-escapes by default — this is good. The risk is when escaping is
deliberately disabled.

- Audit every use of `| safe` and `Markup()` — these disable escaping
- Any user HTML passed through these filters must first be cleaned with
  bleach.clean() using a strict allowlist
- If you cannot verify the input is safe, do not use `| safe`

### Password Hashing

Never store plaintext passwords. Always hash with Werkzeug's built-in functions.
Never implement a custom hashing scheme.

```python
from werkzeug.security import generate_password_hash, check_password_hash

# On registration
user.password_hash = generate_password_hash(password)

# On login
if check_password_hash(user.password_hash, submitted_password):
    ...
```

### Never Log or Store Payment Data

Stripe handles card processing — the application must never touch raw card data.

- Never log request bodies on payment or webhook endpoints
- Never store card numbers, CVVs, expiry dates, or raw Stripe tokens anywhere
  in the database or logs
- The only payment identifiers stored should be Stripe's own IDs
  (customer ID, payment intent ID) — not any card data

---

## 14.2 High — Resolve Before Public Launch

### CSRF Protection — Initialise on Day One

Flask-WTF's CSRFProtect enforces CSRF validation on every POST request sitewide —
not just FlaskForm forms. This affects every bare HTML `<form>` tag on the site.

**Critical lesson:** Initialise CSRFProtect in `__init__.py` on day one — before
any templates are written. This means csrf_token() is always available.

```python
# __init__.py
csrf = CSRFProtect()
csrf.init_app(app)
```

If bare `<form>` tags are added to templates after CSRFProtect is initialised, the
global `form {}` CSS rule will apply to them and alter their visual layout. Use a
scoped class to neutralise this:

```css
.form-inline-action {
    background: none;
    padding: 0;
    border-radius: 0;
    box-shadow: none;
    max-width: none;
    margin: 0;
    display: inline;
}
```

### Rate Limiting

Public and write endpoints must enforce per-IP request limits. Login endpoints are
especially critical.

```python
@limiter.limit("10 per minute")
@app.route('/login', methods=['POST'])
def login():
    ...
```

### Stripe Webhook Signature Verification

Unsigned webhooks can be forged to fake successful payment events. Verify the
Stripe signature on every webhook — reject on failure with a 400 response.

```python
try:
    event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
    )
except stripe.error.SignatureVerificationError:
    return '', 400
```

### Session and Token Expiry

Sessions must have a finite lifetime. Set in Config:

```python
PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
SESSION_REFRESH_EACH_REQUEST = False
```

### Password Reset Link Expiry

Reset tokens must expire within 15–60 minutes.

- Store reset tokens with a created_at timestamp in the database
- Enforce expiry at the point of redemption, not just generation
- Invalidate the token immediately after successful use

### Pagination on All List Queries

Never call .all() on a table that can grow without bound.

```python
products = Product.query.paginate(page=page, per_page=24)
```

### Structured Logging

- Replace print() with Python's logging module or structlog in production
- Emit logs with request ID, user ID, endpoint, and status

### Security Headers

HTTP security headers prevent clickjacking, content-type sniffing, and a class of
injection attacks. Flask-Talisman handles all of these in one initialisation.

```python
from flask_talisman import Talisman

Talisman(app, content_security_policy={
    'default-src': "'self'",
    'style-src': ["'self'", 'fonts.googleapis.com'],
    'font-src': ['fonts.gstatic.com'],
    'script-src': ["'self'", 'js.stripe.com'],
    'frame-src': ['js.stripe.com']
})
```

Key headers this sets automatically: `X-Frame-Options: DENY`,
`X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`.
Adjust the CSP allowlist as external services are added (Stripe, Google Fonts, etc.).

### Account Enumeration Prevention

Login and registration endpoints must never reveal whether an email address exists
in the database. This prevents attackers from harvesting valid accounts.

- Login failure: always return "Invalid email or password" — never "Email not found"
  or "Incorrect password" as separate messages
- Registration: if an email already exists, do not say so directly — send a
  "you already have an account" email to that address, or show a generic success message
- Password reset: always show "If that email exists, a reset link has been sent" —
  never confirm or deny whether the email is registered

---

## 14.3 Medium — Resolve in First Post-Launch Iteration

### CORS Policy

Never combine wildcard origins with session cookies.

```python
CORS(app, origins=['https://greenfireglass.com'], supports_credentials=True)
```

### Error Response Leakage

Stack traces must never appear in responses returned to clients.

```python
# config.py
DEBUG = False  # Never True in production

# __init__.py
@app.errorhandler(500)
def internal_error(e):
    return {'error': 'An unexpected error occurred'}, 500
```

### Environment Variables Validated at Startup

```python
required = ['SECRET_KEY', 'DATABASE_URL', 'STRIPE_SECRET_KEY', 'ANTHROPIC_API_KEY']
for var in required:
    assert os.getenv(var), f'{var} is not set'
```

### Database Indexing

Add index=True to columns used in filter(), order_by(), or join().

```python
slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), index=True)
```

### Connection Pooling

```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 5,
    'max_overflow': 10,
    'pool_pre_ping': True
}
```

### Image Upload Handling

- Upload to S3 or equivalent object storage — never serve uploads directly from Flask
- Validate file type using python-magic (checks actual bytes, not the extension)
- Enforce a maximum file size limit

### Async Email Dispatch

Use Celery with Redis or RQ. The request handler enqueues the task and returns
immediately — it does not wait for the email to send.

### Dependency Security

Known vulnerabilities in third-party packages are a common attack vector. Run
before every deployment:

```bash
pip audit
# or
safety check -r requirements.txt
```

If `pip audit` is not installed: `pip install pip-audit`. Fix any Critical or High
findings before deploying. Review Medium findings — not all require immediate action
but all require a conscious decision.

### Database User Least Privilege

The PostgreSQL user the application connects with should have only the permissions
the app actually needs — not superuser. On Render this is handled automatically,
but verify the user cannot create or drop databases. If setting up PostgreSQL
manually, grant only SELECT, INSERT, UPDATE, DELETE on the application's tables.

---

## 14.4 Low — Address When Convenient

### Health Check Endpoint

```python
@app.route('/health')
def health():
    return {'status': 'ok'}
```

Return only `{"status": "ok"}`. No version numbers, DB details, or internal paths.

---

## 14.5 Database Backup Protocol

Before any migration or deployment, run a manual backup. For Render PostgreSQL,
use pg_dump from a local machine:

```bat
:: backup_greenfire.bat
pg_dump -h [RENDER_HOST] -U [DB_USER] -d [DB_NAME] -F c -f backup_%DATE%.dump
```

Store backups in a dedicated local folder. Verify each file is greater than zero
bytes. Run backups before every git push, before every migration, and weekly.

Restore command (overwrites current DB — use with caution):
```bash
pg_restore -h [HOST] -U [USER] -d [DB_NAME] backup_file.dump
```

---

## 14.6 Security Quick Reference

| Item | Requirement |
|---|---|
| Session cookies | HTTPONLY, SECURE, SAMESITE=Lax — set on day one |
| CSRFProtect | Initialise in __init__.py on day one — before any templates |
| Admin routes | @require_role decorator on every privileged route |
| Credentials | Never in source. .env in .gitignore from first commit. |
| Passwords | Always hash with Werkzeug — never store plaintext |
| Payment data | Never log or store card data — Stripe IDs only |
| Stripe webhooks | Verify signature on every webhook — reject on failure |
| Security headers | Flask-Talisman on day one — adjust CSP as services are added |
| Account enumeration | Generic error messages on login, register, and password reset |
| List queries | Always paginate — never .all() on unbounded tables |
| Error responses | DEBUG=False in production. Custom 500 handler. |
| Env vars | Validate all required vars at startup |
| Dependencies | pip audit before every deployment |
| DB user | Least privilege — SELECT/INSERT/UPDATE/DELETE only |
| DB backup | Before every migration and deployment |

---

# PROJECT-SPECIFIC SECTION
# ============================================================

## Project: Green Fire

**Entry point:** `greenfire.py`
**Hosting:** Render (not yet live — setup in separate chat)
**Database:** PostgreSQL via Render (not yet live — setup in separate chat)
**Domain:** greenfireglass.com (registered at Namecheap, not yet pointed to Render)

## Colour Palette

```
GREENS
--color-forest-green:           #3A6B1A    Primary brand, buttons, links
--color-forest-green-hover:     #406932    Forest green hover state
--color-hillside-green:         #8F9783    Mid-tone earthy accent
--color-hillside-green-hover:   #A5AC9C    Hillside green hover state
--color-light-green:            #D8E6C8    Section backgrounds, subtle fills
--color-light-green-hover:      #C8DAB4    Light green hover state
--color-dark-section:           #3E473B    Hero, prodo sections, dark split sections
--color-nav-dark:               #2A302A    Nav bar, footer, dropdown panels

ORANGES
--color-burnt-orange:           #C4622D    Accent, CTA buttons, chat bubble
--color-burnt-orange-hover:     #D4743A    Burnt orange hover state

NAVY & BLUES
--color-navy:                   #2C3E50    Dark UI elements
--color-navy-hover:             #34495E    Navy hover state
--color-blue-dark:              #0047AB    Dark blue accent
--color-blue:                   #3498DB    Standard blue, links
--color-blue-hover:             #2980B9    Blue hover state
--color-blue-light:             #89C0E6    Light blue
--color-blue-light-hover:       #5DADE2    Light blue hover state

BEIGES
--color-beige:                  #F5F0E8    Primary light background
--color-beige-hover:            #EDE8DC    Beige hover state
--color-beige-deep:             #EAE3D2    Deeper beige variant

OTHER
--color-border:                 #D0CBBF    Light borders
--color-border-dark:            #4A5445    Dark borders
--color-error:                  #C0392B    Error states
--color-error-hover:            #A93226    Error hover state
```

## Fonts

- **Display / Headlines:** Cooper Black (Google Fonts)
- **Body / UI:** DM Sans (Google Fonts)

## Pages Built

- `base.html` — fully built. Nav inline, footer inline, age gate, chat bubble,
  color dictionary comment at bottom.
- `index.html` — fully built landing page. Hero, heady glass section, prodo section,
  location section. All green-background sections use --color-dark-section.
  Nav bar and footer use --color-nav-dark.
- All other templates are stubs.

## Current Task

Product catalogue pages — in this order:
1. `/headies` → heady_glass.html
2. `/prodos` → prodo_pieces.html (sectioned with anchors)
3. `/vapes-accessories` → vapes_accessories.html (sectioned with anchors)
4. `/product/<slug>` → product.html (universal detail page, heady + prodo)
5. `/archive` → archive.html

**Database must be live before building catalogue pages.**
DB setup is handled in a separate chat. Confirm DB is live before proceeding.

## Confirmed Architecture Decisions

- **Slug:** Single universal route `/product/<slug>` handles all products
- **Product type:** `product_type` field on Product model — values: 'heady' or 'prodo'
- **Routes:** Two files only — `routes.py` (public) and `admin.py` (admin)
- **Templates:** Flat, no subfolders
- **CSS variables:** Colors and --nav-height only. No semantic alias layer.

## Open Decisions (do not build blocked features until resolved)

- **Instagram embed approach** — blocks Featured Artist page
- **Analytics** — blocks deployment
- **AI chat agent name** — blocks chat feature
- **Shipping rates** — blocks Stripe checkout
- **Artist terms (consignment vs outright)** — blocks finalizing Product model

## Industry Terminology (use exactly as written)

- "Heady" — decorated, artistic, high-craft functional glass
- "Prodo" — production glass, regularly produced series
- "Rig" — oil/concentrate pipe
- "Bubbler" — water pipe with built-in water chamber
- "Uni Place Creative District" — the arts district (not "University Place Creative District")
- "University Place" — the neighborhood name

## Files That Must NOT Be Touched Without Explicit Confirmation

- `app/models.py` — database schema, any change affects migrations
- `app/__init__.py` — app factory, blueprint registration
- `config.py` — environment configuration

## Git Remote Naming Convention

The owner uses two remotes consistently across all projects:
- `local` — local backup (`C:\Users\rodkr\GreenFire-WebProject_Support\GreenFireSite_BackUp\greenfire-backup.git`)
- `origin` — GitHub (`https://github.com/RodDog420/GreenFire-WebProject.git`)

**⚠ Always use `local` (not `backup`) when referring to the local backup remote.**

Push commands:
- Save to local backup: `git push local main`
- Push to GitHub (deploy): `git push origin main`

## Known Issues / Notes

- Database tables do not exist yet — no migrations have been run
- `nav.html` in templates was an orphaned file — it has been deleted. Nav lives
  inline in `base.html` only.
- The owner uses Notepad++ for CSS and VS Code for HTML. VS Code shows color
  swatches next to hex values — this is why the color dictionary in `base.html`
  must always have accurate hex values.
- The owner makes direct edits to files and uploads updated versions. Always treat
  uploaded files as ground truth over your own copy.

# ============================================================
