# CLAUDE.md
# Flask Web Design Methodology Primer
# Universal Baseline — All Projects — All Sessions

---

# 1.0 CLAUDE.md Methodology and Tool Criteria
# ============================================================

## 1.1 Tool Selection — Claude Code vs Chat Interface
The key insight is that Claude Code's autonomy is an asset when the cost 
of mistakes is low, and a liability when it isn't.  
Claude Code through the startup sequence, chat interface once design is live.

The governing principle: Once the design is load-bearing — meaning other 
decisions depend on it — switch to the chat interface and its propose-then-confirm 
workflow. Claude Code moves fast and touches real files immediately. The chat 
interface keeps a human in the loop on every step. 
Use each for what it is suited for.

## 1.2 Naming Conventions

There are two CLAUDE.md documents in this system. Both are instances of
CLAUDE.md files — not instances of Claude itself.

**Master-Claude-Template** — the master CLAUDE.md document. Lives at:
C:\Users\rodkr\FlaskApp Instructions\CLAUDE.MDs\WebDev_Foundations\flask-web-dev-master.md
This is the global baseline all Project-Instance-Claude documents inherit from.
Never lives inside any codebase.

**Project-Instance-Claude** — the project-specific CLAUDE.md document. Lives
inside a specific project folder. Customized for that project to include project-specific configurations, variables, dictionaries, etc. Always listed
in .gitignore. Never committed. Never pushed to GitHub or any host.

***Project-specific Dictionaries*** - Project Color-Dictionary and complete Z-score Dictionary/Index is always recorded at bottom of project-instance of CLAUD.MD.
    COLOR DICTIONARY -add all new colours at bottom of project CLAUD.md
    Z-INDEX DICTIONARY -document all z-index values bottom of project CLAUDE.md>

## 1.3 Why Project-Instance-Claude Is Always Gitignored

CLAUDE.md is a large document. Committing it sends it to GitHub and then to any host (e.g. Render), which loads it on every deploy. Unnecessary overhead.

Add this to .gitignore on every project, as its own category at the bottom:

    # Claude Code
    CLAUDE.md

## 1.4 Two Types of Updates

**Project-specific** — applies only to the current Project-Instance-Claude.
**Global** — applies to all future projects and goes into the Master-Claude-Template.

## 1.5 Who Decides What Gets Written and Where

The owner makes all decisions about what gets written and where. Claude never
writes to the Project-Instance-Claude or the Master-Claude-Template unless the
owner has explicitly asked for it in that conversation.

Claude may identify an improvement and flag it — but it proposes, it does not
act. The owner pulls the trigger.

When the owner authorises an update, Claude reads the relevant document, makes
the change, and confirms what was written.

## 1.6 Any Claude Code Instance Can Reach the Master-Claude-Template

Claude Code is not sandboxed to the project folder it was activated in. Any
instance can read from and write to the Master-Claude-Template at the path
above — but only when the owner has explicitly authorised it for that session.

## 1.7 Browser QA — Playwright MCP

Playwright MCP is the standard browser QA tool across all projects.
Requires Node.js 18+ and is registered once per project:

    claude mcp add playwright npx @playwright/mcp@latest

When invoking Playwright inside a Claude Code session, always say
"Use Playwright MCP" explicitly — otherwise Claude may default to
Bash instead.

### Audit Protocol

When asked to audit a site, Claude visits every page accessible
from the navigation and reports:

- Broken or misaligned layouts
- Console errors
- Anything visually incomplete or unfinished

Claude documents only. It never fixes anything found during an
audit without explicit owner approval in a separate session.

### Port

Default Flask dev server is localhost:5000. Confirm the active
port at the start of each session if it differs.

# ============================================================

# 2.0 Cardinal Rules

**⚠ Before any work begins:** Confirm the correct file. Ask to see existing code before
assuming a solution does not exist. Read the ENTIRE file before editing any part of it.
Never make assumptions — always ask first. This applies every session without exception.

## 2.1 Before Building Anything Structural

Before building any new folder, file, or architectural element, Claude must state explicitly
what it intends to create, why it is needed, and wait for explicit confirmation before
touching anything.

**⚠ This applies to new folders, new files, new routes, new blueprints, and any change to
the project architecture. Claude proposes. The owner decides.**

## 2.2 Agreed Implementation Approaches Are Binding

When an implementation approach has been explicitly agreed upon, it cannot be changed without
flagging the reason and getting explicit confirmation first. Not mid-build. Not silently.
Not ever.

Real example of a violation: the row-reversal class (.split-inner--reversed) was explicitly
agreed upon as the mechanism for alternating desktop layouts. Mid-build, Claude abandoned it
silently and introduced a dual-image approach without flagging the change. This caused hours
of rework.

## 2.3 Do Not Invent Industry-Specific Names or Assumptions

- Never guess at industry-specific terminology, naming conventions, or product categories
- Ask the owner for naming conventions before creating routes, templates, or database fields
  that carry business meaning
- Never argue that an invented name is correct or a best practice — it is an assumption

**⚠ If Claude is uncertain what something should be called: ask. Do not guess and then
defend the guess.**

## 2.4 Arbitrary Assumptions Are Not Best Practices

When the owner questions a decision, Claude must honestly assess whether it is a genuine
best practice or an assumption. If it is an assumption, Claude acknowledges it immediately
and defers. Claude never suggests the owner may have a memory problem as a way of defending
an arbitrary choice.

## 2.5 Session Sync Checklist — Required After Every Build Session

At the end of every build session, Claude must produce an explicit sync checklist containing
every file created or changed, its exact destination path, and confirmation that the owner
has placed it before proceeding.

**⚠ Never assume a file was placed. Never proceed to the next feature without confirming
sync.**

## 2.6 Teaching vs Deferring

- **Code quality, maintainability, standards** → Teach proactively
- **Personal workflow, naming, organisation** → Ask first
- **Unclear** → Ask first

## 2.7 When in Doubt, Dig Deep Before Responding

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


## 2.8 Automation Over Manual Entry

Default to automation wherever repetitive manual input would 
otherwise be required. Do not build manual workflows when a 
programmatic solution exists.

Examples:
- SEO blocks (meta description, canonical, robots, title) must 
  be driven by variables or template logic — never filled in 
  manually per page
- Any pattern that repeats across more than two pages is a 
  candidate for automation — flag it and propose the approach
  before building it manually

Claude must identify automation opportunities proactively and
propose them before building the manual version. The owner
decides whether to automate or not — but Claude must surface
the option.

## 2.9 Karpathy Guidelines — Invoke on Layout and CSS Work

Before making any CSS layout change, invoke the
andrej-karpathy-skills:karpathy-guidelines skill.
This is non-negotiable.

If the skill is not installed, run these commands once:

    /plugin marketplace add forrestchang/andrej-karpathy-skills
    /plugin install andrej-karpathy-skills@karpathy-skills
    /reload-plugins

---

# 3.0 Project Structure, File Naming & Organisation

## 3.1 The App Folder

**⚠ The Flask application package is always named `app`. Never anything else.**

## 3.2 The Entry Point File

**⚠ The Flask entry point is always named after the project (e.g. `greenfire.py`).
A `.flaskenv` file tells Flask where to find it.**

## 3.3 File Count Philosophy — Fewer Files, Longer Files

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

## 3.4 Standard Project Structure

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

## 3.5 Ask Before Creating Sub-Folders

Sub-folders add navigational complexity. Claude must never create a new sub-folder without
proposing it first and receiving explicit owner approval.

## 3.6 The .gitignore File

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

## 3.7 The Two Environment Files

**.flaskenv — Flask CLI configuration. Safe to commit.**
```
FLASK_APP=[projectname].py
FLASK_DEBUG=1
FLASK_ENV=development
```

**.env — Runtime secrets. NEVER commit.**

**⚠ Both files must be created at the start of every project. Neither is optional.**

---

# 4.0 New Project Startup Order

- Step 1  — Present complete folder diagram and get confirmation
- Step 2  — Create `.gitignore` first
- Step 3  — Create folder structure
- Step 4  — Create `.flaskenv` and `.env.example`
- Step 5  — Create `config.py` and entry point
- Step 6  — Create `app/__init__.py`
- Step 7  — Create all CSS files in correct order 
- Step 8  — Create `base.html` with nav and footer inline
- Step 9  — Create route stub files and stub templates
- Step 10 — Create `models.py`
- Step 11 — Install dependencies, then `pip freeze > requirements.txt`
- Step 12 — Confirm `flask run` works before proceeding to features

**⚠ `requirements.txt` is generated by `pip freeze` after all packages are installed —
never created manually.**

---

# 5.0 CSS File Architecture

## 5.1 File Structure

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

## 5.2 CSS Variables Philosophy — Colours and Coupling Agents Only

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
Z-index values need to be aggregated into one single common area so that owner can visually inspect them altogether and compare them visually all at once. Without group them, comparing them is much more difficult. Therefore, class specific styling is affected inside he CSS files, but then ALL Z-scores are subsequently added into this large, project-specific Z-score Dictionary to best facilitate these internal comparisons.

**⚠ Never create spacing, typography, shadow, transition, or z-index variables. If uncertain whether a variable is justified, ask owner: is this a coupling relationship where two separate rules must always agree? If yes, a variable may be warranted. If no, hardcode it.**

## 5.3 Colour System — Variables + Dictionary

All colour variables defined in `variables.css`. Every main colour must have a corresponding hover variant. A human-readable colour dictionary lives as a comment at the bottom of the project-specific instance of the `CLAUDE.md` in the project's root folder. This is best because VS Code, which we use to access the file shows color swatches next to hex values in this dictionary.

**⚠ IMPORTANT - If a new colour is added anywhere in the project, it must be added to BOTH `variables.css` AND the `CLAUDE.md` colour dictionary simultaneously.**

**⚠ No semantic alias layer.** Do not create variables like `--color-btn-primary` that
point to another variable. Reference color variables directly: `var(--color-forest-green)`.
The double-indirection makes DevTools unreadable and debugging painful.

---

## 5.4 Dangerous Properties — Always Paired

Some CSS properties are destructive when used in isolation. They solve one problem while silently creating another. These properties are only permitted when their required safety net is explicitly present in the same rule or the same component.

### white-space: nowrap

Keeps content on a single line regardless of container width. Without a safety net, it will push content through the wall of its container and cause overflow or horizontal scroll.

Required — always pair with all three of the following, no exceptions:
- Ellipsis — text stays on one line and truncates cleanly:
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;

This is the only valid use of white-space: nowrap in this project. If the content cannot truncate with ellipsis, do not use white-space: nowrap. 
"The content is short" and "another element will absorb the overflow" are not safety nets — they are assumptions that will break at runtime.
---
### See also below: overflow-x: hidden on body — (Section 6.6 below)


# 6.0 Mobile-First Development


## 6.1 Core Philosophy

- Design floor: 320px — test every layout at this width
- Base CSS targets small screens — scale up via min-width breakpoints
- Touch targets: all buttons and links must be at least 44x44px
- No horizontal scroll — test at 320px
- All dropdown options: left-aligned, never centred

## 6.2 Units — Priority Order

- `vw` / `vh` — highest preference
- `rem` — typography and component sizing
- `em` — spacing relative to current element font size
- `px` — only for borders and shadows

**⚠ Never use `px` for breakpoints — use `rem`.**

## 6.3 Standard Breakpoints

Custom breakpoints are permitted when a layout genuinely requires it. Always use rem,
never px.

```css
@media (min-width: 48rem) { ... }  /* Tablet 768px */
@media (min-width: 50rem) { ... }  /* Custom: e.g. nav hamburger breakpoint */
@media (min-width: 64rem) { ... }  /* Desktop 1024px */
@media (min-width: 90rem) { ... }  /* Wide 1440px */
```

## 6.4 Baseline Alignment for Grouped Labels

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

## 6.5 Media Query Override Safety Rule

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

## 6.6 Scrollbar and Overflow Rules — Apply to Every Project

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

# 7.0 The clamp() Function

## 7.1 When TO Use clamp()

- Single property scaling smoothly across screen sizes
- Font sizes, container widths, padding, gap values

```css
font-size: clamp(1rem, 2.5vw, 2rem);
```

## 7.2 When NOT to Use clamp()

When already writing targeted per-side values at specific breakpoints — you already have
control. Adding `clamp()` creates unnecessary complexity.

**Default to `clamp()` for typography and generic sizing. Use explicit media queries for
surgical per-side precision.**

---

# 8.0 CSS Class Reuse — The Balancing Act

**Err toward creating new classes. The cost of a redundant class is low. The cost of a
cascading break is high.**

## 8.1 When to Reuse

- Same visual intent, same structural role
- Pages unlikely to diverge visually
- Reusing would not require overrides

## 8.2 When to Create a New Class

- Section will evolve differently over time
- Would require overrides to undo the existing class
- Page-specific with any chance of diverging
- Uncertain — always create new

## 8.3 Scoped Overrides

```css
.media-link-card .content-footer { flex-wrap: nowrap; }
```

Always document scoped overrides with a comment naming the page or context.

---

# 9.0 Typography

- All font declarations live in `base.css` only
- The browser must never supply a default font
- All text is left-aligned by default
- All sizing is `rem` or `em` — never `px` for font sizes

## 9.1 Fluid Typography with clamp()

```css
h1 { font-size: clamp(1.75rem, 5vw, 3rem); }
h2 { font-size: clamp(1.375rem, 4vw, 2.25rem); }
p  { font-size: clamp(1rem, 2vw, 1.125rem); }
```

---

# 10.0 Code Conventions

## 10.1 Inline Styling

**⚠ ALL styling goes in CSS files. Never put styling inline inside HTML.
Before violating this rule: always ask first.**

## 10.2 The TRouBLe Shorthand

Always use four-value shorthand for margin, padding, border-width, border-radius.
Order: Top, Right, Bottom, Left.

```css
margin: 0 0 0.5rem 0;
```

NOTE: Exception: at wider breakpoints that override narrower ones, use explicit per-side
properties to preserve previously set values. See Section 6.5.

## 10.3 No !important

**⚠ Never use `!important`. Resolve specificity conflicts at the source.**

## 10.4 CSS Section Headers

```css
/* ==============================================
   SECTION NAME --- Brief description
   ============================================== */
```

## 10.5 No HTML Comments

Do not add HTML comments to templates unless genuine complexity warrants it. Comments belong
in Python and CSS files.

## 10.6 Container Integrity

- Content must never break out of its container
- Always set `overflow-wrap: break-word` on user-generated content
- Always set `min-width: 0` on grid and flex children that contain text
- Test all containers at 320px before considering complete

## 10.7 Database & Data Integrity

- All queries use SQLAlchemy ORM — never raw SQL unless unavoidable
- Handle all edge cases: division by zero, empty results, null values
- Always ensure correct pluralisation

## 10.8 SEO — Applied to Every Page

- Every template must include: canonical tag, robots meta tag, meta description
- Meta descriptions written per page — never auto-generated
- All images must have descriptive alt text
- URL slugs clean and descriptive — never expose raw database IDs
- Schema.org structured data on product and content pages

## 10.9 HTML Line Length

Keep HTML within 80 characters per line. Write vertically, not horizontally.

---

# 11.0 HTML — Prefer Vertical Layout Over Horizontal

Users interact with Flask applications on narrow screens. Always design HTML structure to be
vertically aligned first. Horizontal layouts should be exceptions that are explicitly
justified, not defaults. Stack elements vertically in the source order — CSS can reorder
them for wider viewports using media queries, but the base structure should read cleanly
from top to bottom without any CSS applied.

In practice: avoid placing sibling elements side by side in raw HTML unless they are
genuinely equivalent in importance and always short in content. If either element could
ever be long, give each its own vertical block.

---

# 12.0 CSS Layout — Grid and Flexbox Conventions

## 12.1 Always Pair max-width with width: 100%

Any container element that uses `max-width` must always have `width: 100%` alongside it.

```css
.container {
    width: 100%;
    max-width: 75rem;
    margin: 0 auto;
}
```

## 12.2 Flexbox + space-between vs Grid

- `justify-content: space-between` creates inherent tension. If one side must never
  overtake the other → use Grid instead.
- **Grid = explicit intent.**

## 12.3 CSS Grid — Two-Column Key-Value Layout

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

## 12.4 CSS Grid — Right-Aligned Content in Far-Right Column

Use `justify-self: end` on the cell. Do NOT use `margin-left: auto` on a grid child.

```css
.grid-cell-right {
    justify-self: end;
    text-align: left;
    width: auto;
}
```

## 12.5 Flexbox — flex-shrink and Content Protection --   Two distinct scenarios. 

Unbounded strings — user-defined content with no character ceiling: review text, names, URLs, headlines. flex-shrink: 0 on these is a layout weapon. Never use it. Instead:

```css
.unbounded-content {
    min-width: 0;              /* unlocks shrinking — required or overflow-wrap won't fire */
    overflow-wrap: break-word; /* breaks long strings cleanly */
    max-width: 100%;
}
```

Bounded strings — predictable maximum length: dates, ratings, status labels, currency. A date can never exceed "September 28, 2026". flex-shrink: 0 is correct and safe here — it hardens the element against compression from a sibling.

```css
.bounded-content {
    flex-shrink: 0; /* safe — string has a known maximum width */
}
```

Mixed row pattern — one bounded element, one unbounded in the same flex row:

```css
.row > .bounded   { flex-shrink: 0; }
.row > .unbounded { min-width: 0; overflow-wrap: break-word; }
```

The bounded element holds. The unbounded element yields and wraps.
overflow-wrap: break-word alone does nothing in a flex container. Flex items default to min-width: auto, which prevents shrinking below content width. Always pair with min-width: 0.


## 12.6 Flexbox — Fixed Elements

```css
flex: 0 0 auto;  /* do not grow, do not shrink, size to content */
```

## 12.7 Flexbox — Greedy Space-Filling Elements

```css
flex: 1 1 0;  /* grow to fill, shrink if needed, start from zero */
```
    In practice, flex: 1 1 0 is frequently used to create equal-width columns. Because the flex-basis is 0, every item starts with the same "zero" size and grows at the same rate to fill the container, resulting in perfectly equal distribution regardless of content length. This prevents long content from assuming it deserves more space than what remains after fixed elements are placed.

## 12.8 Flexbox — justify-content: space-between Management Rules

- Every flex child must have `min-width: 0`
- Use `overflow-wrap: break-word` on any element with user-defined strings
- Protect fixed-width elements with `min-width` on a specific value, not `flex-shrink: 0`

## 12.9 Flexbox — Scope Rules with :nth-child

When a flex container has multiple rows needing different flex behaviour, use `:nth-child`
to scope rules rather than applying them globally.

```css
.header-row:nth-child(1) .left  { flex: 1 1 auto; }
.header-row:nth-child(2) .left  { flex: 0 0 auto; min-width: 10ch; }
.header-row:nth-child(2) .right { flex: 1 1 0; overflow-wrap: break-word; }
```

---

# 13.0 base.html Template Structure

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

# 14.0 Quick Reference — Decision Rules

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

# 15.0 Mobile Card Design Blueprint for Converting Desktop Data Tables

## 15.1 The Fork — Why Two Roadmaps

The single most important question when designing any card component is:
does this card contain user-submitted strings of unknown length?

This question drives every subsequent layout decision. Fixed-length
content — badges, prices, dates, status labels — has a known maximum
width and can be laid out with certainty. User-submitted strings —
names, descriptions, addresses, review text — have no ceiling and will
break any layout that assumes known widths. These two card types require
different rules and are documented separately below.

Row layout tool selection — the right column content decides:
  Variable or unknown-length content on the right (user strings, names, 
  descriptions) → Grid.
  Fixed, bounded content on the right (dates, prices, status labels, 
  counts) → Flexbox is fine.


## 15.2 Shared Foundations — All Cards

Card container is always Grid. Grid does everything a block container
does and more. Since all cards use two columns, always start with Grid.

Two columns always. Maximize space on every card by using both columns.
Use them as key-value pairs (label left, value right) or as content
left with a functional element right. Two columns is the baseline for
all breakpoints unless content type dictates otherwise.

Row-level tool selection. The card container establishes the grid.
Each row inside the card independently chooses Grid or Flexbox based
on what its right column contains. The container has no opinion on
this. See 15.3 and 15.4.

Full-width rows. Any content important enough to span the full card
width uses grid-column: 1 / -1. This steps outside the two-column
track without requiring special markup or a wrapper element.

Spacing between rows. Use gap on the grid container. Gap is set per
component — never prescribed globally. When a specific row needs
different spacing from its neighbors, use margin-top on that row to
override the gap for that row only.

Actions row. Always last in source order. Layout depends on context:
- Public-facing card: full-width stacked buttons. Maximum touch
  target, easy for the public to press.
- Admin-facing card: buttons side by side, equal width AND equal height.
  The flex container must use ALL THREE of these together — no exceptions:

      .actions-inner {
          display: flex;
          flex-wrap: wrap;
          align-items: stretch;   /* equal height — every button matches the tallest */
          gap: 0.5rem;
      }
      .actions-inner .btn {
          flex: 1 1 0;            /* equal width — buttons share the row in equal parts */
          white-space: normal;    /* text wraps within the button rather than expanding it */
          text-align: center;
      }

  `flex: 1 1 0` — zero basis means all buttons start from nothing and grow equally.
  Never use `flex: 1 1 auto` — auto basis causes a lone wrapped button to fill the
  full row width.

  `align-items: stretch` — every button in the row matches the tallest one's height.
  Never use `align-items: flex-start` in an admin action button group — it lets each
  button size independently, producing uneven heights when any button's text wraps.

  `white-space: normal` — allows text to wrap within a constrained button width.
  This only triggers because `flex: 1 1 0` constrains the width. Without the flex
  rule, `white-space: normal` alone does nothing — the button just expands.

  Forms wrapping a button must use `display: contents` so the button participates
  directly in the flex container as if the form element were not there.

## 15.3 Roadmap A — Fixed-Length Card

Use when all content is predictable and bounded: badges, prices,
dates, statuses, short labels. Content width is known so layout
can be rigid.

Column collapse: two columns hold at all breakpoints. Content is
known to fit.

Row layout: Flexbox is appropriate for individual rows since right-
column content width is known and bounded.

    .row {
        display: flex;
        align-items: flex-start;
        gap: [context-dependent];
    }
    .row-left  { flex: 1 1 auto; min-width: 0; }
    .row-right { flex: 0 0 auto; }

Word-break rules: not required. Fixed strings do not need overflow
protection.

## 15.4 Roadmap B — User-Submitted String Card

Use when any field accepts user input: names, descriptions, addresses,
review text, or any string without a known maximum length.

Column collapse: may collapse to a single column at narrow breakpoints
depending on string length risk. Evaluate per component.

Row layout: use Grid for rows containing user-submitted strings.
The right column sizes to its content; the left column takes the rest.

    .row {
        display: grid;
        grid-template-columns: 1fr auto;
        gap: [context-dependent];
    }

Word-break — apply as a set from the start, never retrofit. These
three properties must be applied together on every user-submitted
string container when the component is first built. Do not wait for
a layout break to discover the need for them.

    .user-string {
        overflow-wrap: break-word;
        min-width: 0;
        max-width: 100%;
    }

## 15.5 Responsive Table-to-Card Pattern

Data tables cannot fit on narrow screens. Collapse them to stacked
cards at a defined breakpoint using CSS only. Semantic HTML stays
intact — no duplicate markup is needed. The table is visually
transformed via display: block on the table elements.

Before writing any CSS — every <td> must have a class name. When a
table collapses to cards, each cell becomes a block-level element and
loses its column context. Without a class name there is no way to
target individual cells for different treatment — for example, giving
the actions cell a top border and full-width buttons while leaving the
name cell unstyled. Add class names to all <td> elements before
writing collapse CSS.

    @media (max-width: 40rem) {

        .your-table thead { display: none; }

        .your-table,
        .your-table tbody,
        .your-table tr {
            display: block;
            width: 100%;
        }

        .your-table tr {
            border: 0.0625rem solid [border-color];
            border-radius: 0.5rem;
            margin-top: 1rem;
            padding: 1rem;
        }

        .your-table tbody tr td {
            display: block;
            padding: 0.25rem 0;
            border-bottom: none;
        }

        .your-table__actions {
            margin-top: 0.75rem;
            padding-top: 0.75rem;
            border-top: 0.0625rem solid [border-color];
        }

        .your-table__actions-inner {
            flex-direction: column;
            align-items: stretch;
        }

        .your-table__actions-inner .btn,
        .your-table__actions-inner form {
            display: block;
            width: 100%;
        }

        .your-table__actions-inner form button {
            width: 100%;
        }

    }

Spacing: apply margin-top to the table wrapper — not margin-bottom
to whatever precedes it. See Spacing Ownership rule.



# 16.0 Security Requirements

Security decisions affect the model, routes, auth, and session handling.
Retrofitting security after the fact is painful and error-prone. Every item
below must be considered at the start of a build, not after launch.

Requirements are ordered by severity. Critical items block deployment. High
items must be resolved before public launch. Medium items must be resolved in
the first iteration after launch.

---

## 16.1 Critical — Block Deployment Until Resolved

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

## 16.2 High — Resolve Before Public Launch

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


### Talisman-Ready Development — Build Standards

Every Flask project is built Talisman-ready from day one. This means CSP compliance is a design
constraint, not an afterthought.

JavaScript

  All JavaScript lives in external .js files in static/js/ from the first line of code written.
  Inline <script> blocks are never used under any circumstances. No exceptions. If a script requires
  server-side data from Jinja2, that data is passed via data- attributes on HTML elements. The
  external JS file reads from those attributes. The {% block extra_js %}{% endblock %} block must be
  present in base.html from the start of every project.

CSS

  All styling lives in external CSS files from the first line of code written. Inline style=
  attributes are never used under any circumstances. No exceptions. If a widget requires complex
  positioning — such as an overlay button on an input field — the classes are written in the
  appropriate CSS file first, and those class names are applied in the HTML.

Jinja2

  Every use of | safe and Markup() must be justified in a code comment at the point of use. If
  user-supplied content touches either, it must pass through bleach.clean() with a strict allowlist
  before rendering.

Talisman

  Flask-Talisman is installed and initialized in __init__.py at project start — before any templates
  are written. The initial CSP is strict: script-src: 'self', style-src: 'self', no
  'unsafe-inline'. It is never relaxed without explicit owner approval.


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

## 16.3 Medium — Resolve in First Post-Launch Iteration

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

## 16.4 Low — Address When Convenient

### Health Check Endpoint

```python
@app.route('/health')
def health():
    return {'status': 'ok'}
```

Return only `{"status": "ok"}`. No version numbers, DB details, or internal paths.

---

## 16.5 Database Backup Protocol

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

## 16.6 Security Quick Reference

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
  swatches next to hex values — this is why the color dictionary in CLAUDE.md
  must always have accurate hex values.
- The owner makes direct edits to files and uploads updated versions. Always treat
  uploaded files as ground truth over your own copy.

# ============================================================

## Color Dictionary

Add all new colours here AND in variables.css simultaneously.
This is the sole reference — removed from base.html to keep deployed HTML clean.
VS Code shows color swatches next to hex values below.

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
--color-burnt-orange:           #C4622D    Primary button, CTAs, chat bubble
--color-burnt-orange-hover:     #D4743A    Burnt orange hover state

BROWNS
--color-brown:                  #5C5828    Secondary button, destructive actions
--color-brown-hover:            #424018    Earthy olive-brown hover state

NAVY & BLUES
--color-navy:                   #2C3E50    Dark UI, info elements
--color-navy-hover:             #34495E    Navy hover state
--color-blue-dark:              #0047AB    Dark blue accent
--color-blue:                   #3498D8    Tertiary button (edit, view, informational)
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

MAROON
--color-maroon:                 #800000    Turn off / destructive stop action
--color-maroon-hover:           #3C0008    Maroon hover state
```

## Z-Index Dictionary

Document all z-index values here when adding or changing them.
Gaps between values are intentional — room to insert layers if needed.

```
100   .product-zoom-panel          base.css       Zoom panel beside product image
100   .nav-dropdown-panel          navigation.css Desktop nav dropdown (64rem+)
300   .nav                         navigation.css Sticky nav bar
300   .nav-links                   navigation.css Mobile nav panel (absolute)
400   .chat-bubble-trigger         components.css Floating chat button
400   .chat-panel                  components.css Chat message panel
500   .modal-overlay               components.css Generic modal backdrop
800   .lightbox                    base.css       Full-screen product image viewer
900   .age-gate                    components.css Full-screen age gate overlay
```

# ============================================================
