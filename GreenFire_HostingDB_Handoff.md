# Green Fire — Hosting & Database Setup Handoff
## Separate from the build session — handle in this chat only

---

## PURPOSE OF THIS CHAT

This chat handles one thing only: getting the hosting and database live so the
build session can connect to a real database. Do not build application features
here. Do not edit CSS or HTML here. This is infrastructure only.

---

## WHAT NEEDS TO BE DONE

1. Provision a PostgreSQL database
2. Deploy the Flask app to Render
3. Set all required environment variables on Render
4. Run database migrations
5. Point greenfireglass.com DNS to Render

---

## PROJECT DETAILS

- **Entry point:** `greenfire.py`
- **App factory:** `app/__init__.py` → `create_app()`
- **Domain:** `greenfireglass.com` (registered at Namecheap)
- **Target host:** Render (render.com)
- **Database:** PostgreSQL (Render managed PostgreSQL)
- **SSL:** Render provisions free Let's Encrypt certificate automatically —
  no certificate purchase needed

---

## STEP 1 — Create Render Account and Connect GitHub

1. Create account at render.com if not already done
2. Push the project to GitHub:
   ```
   git remote add origin https://github.com/[username]/greenfire.git
   git push -u origin main
   ```
3. In Render dashboard: New → Web Service → Connect GitHub repo

---

## STEP 2 — Render Web Service Configuration

- **Environment:** Python 3
- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn greenfire:app`
- **Region:** Choose closest to Nebraska (US Central if available, else US East)

Note: `gunicorn` must be in `requirements.txt`. If not present:
```
pip install gunicorn
pip freeze > requirements.txt
```
Then commit and push before connecting to Render.

---

## STEP 3 — Provision PostgreSQL on Render

1. In Render dashboard: New → PostgreSQL
2. Choose the free tier for development, paid tier for production
3. After creation, copy the **Internal Database URL** (use this, not the external URL,
   for apps hosted on Render — it's faster and doesn't count against egress)

---

## STEP 4 — Set Environment Variables on Render

In Render Web Service → Environment, add all of these:

| Variable | Value |
|---|---|
| `SECRET_KEY` | Generate a strong random string |
| `DATABASE_URL` | Internal Database URL from Step 3 |
| `STRIPE_PUBLIC_KEY` | From Stripe dashboard |
| `STRIPE_SECRET_KEY` | From Stripe dashboard |
| `STRIPE_WEBHOOK_SECRET` | From Stripe dashboard (set up webhook first) |
| `MAIL_USERNAME` | Email address for outbound mail |
| `MAIL_PASSWORD` | Email password or app password |
| `ANTHROPIC_API_KEY` | From console.anthropic.com |

**IMPORTANT:** The `DATABASE_URL` from Render starts with `postgres://` but
SQLAlchemy requires `postgresql://`. Either fix this in `config.py`:
```python
uri = os.environ.get('DATABASE_URL')
if uri and uri.startswith('postgres://'):
    uri = uri.replace('postgres://', 'postgresql://', 1)
```
Or set the env var manually with `postgresql://` prefix.

---

## STEP 5 — Run Database Migrations

After the app is deployed and environment variables are set:

**Option A — Via Render Shell (easiest):**
In Render dashboard → Web Service → Shell:
```
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

**Option B — Locally against the remote DB:**
Set `DATABASE_URL` in your local `.env` to the External Database URL from Render,
then run the same commands locally.

After migrations run, verify by checking the Render PostgreSQL dashboard —
all tables should be visible.

---

## STEP 6 — Point DNS at Render

In Render Web Service → Settings → Custom Domain: add `greenfireglass.com`
and `www.greenfireglass.com`. Render will show you two values:

- An A record (IP address) for the apex domain (`greenfireglass.com`)
- A CNAME record for `www`

In Namecheap DNS settings for `greenfireglass.com`:
1. Set A record → Render's IP address
2. Set CNAME for `www` → Render's CNAME value
3. Delete any conflicting default records Namecheap added

DNS propagation takes 15 minutes to 48 hours. Render provisions SSL automatically
once DNS propagates — no action needed.

---

## STEP 7 — Verify Deployment

Once live, confirm:
- [ ] `https://greenfireglass.com` loads the landing page
- [ ] SSL certificate is active (padlock in browser)
- [ ] Age gate appears
- [ ] Nav bar is sticky and dropdowns work
- [ ] No 500 errors in Render logs

---

## AFTER THIS CHAT IS COMPLETE

Tell the build session chat that the database is live and provide:
- The `DATABASE_URL` format (postgresql:// prefix confirmed working)
- Confirmation that migrations ran successfully
- The Render service URL (e.g. greenfire.onrender.com)

The build session can then proceed with database-dependent features.
