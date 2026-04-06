import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError('SECRET_KEY environment variable is not set.')

    SESSION_COOKIE_SECURE        = True
    SESSION_COOKIE_HTTPONLY      = True
    SESSION_COOKIE_SAMESITE      = 'Lax'
    PERMANENT_SESSION_LIFETIME   = timedelta(hours=2)
    SESSION_REFRESH_EACH_REQUEST = False
    TALISMAN_FORCE_HTTPS         = True

    # Database — PostgreSQL on Render
    # SQLite is NOT used — Render has an ephemeral filesystem
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'max_overflow': 10,
        'pool_pre_ping': True
    }

    # Stripe
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')

    # Email — Gmail SMTP via Flask-Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    # Anthropic — AI chat agent
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')

    # App settings
    ITEMS_PER_PAGE = 12
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB upload limit


class DevConfig(Config):
    # Local development overrides
    # SESSION_COOKIE_SECURE must be False — local Flask runs on HTTP, not HTTPS
    SESSION_COOKIE_SECURE = False
    TALISMAN_FORCE_HTTPS  = False
