from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

from config import Config

# Extensions — initialised here, bound to app in create_app()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Bind extensions to app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

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

    return app