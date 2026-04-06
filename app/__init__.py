from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import Config

# Extensions — initialised here, bound to app in create_app()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
talisman = Talisman()
limiter = Limiter(key_func=get_remote_address)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Bind extensions to app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    talisman.init_app(
        app,
        force_https=app.config.get('TALISMAN_FORCE_HTTPS', True),
        content_security_policy={
            'default-src': "'self'",
            'style-src': ["'self'", 'fonts.googleapis.com'],
            'font-src':   ['fonts.gstatic.com'],
            'script-src': ["'self'", 'js.stripe.com'],
            'frame-src':  ['js.stripe.com']
        }
    )

    # Flask-Login settings
    login_manager.login_view = 'routes.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.routes.routes import routes_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(routes_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Inject current datetime into all templates (used in footer copyright year)
    from datetime import datetime
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({'error': 'An unexpected error occurred'}), 500

    return app