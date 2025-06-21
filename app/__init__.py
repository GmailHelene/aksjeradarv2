from flask import Flask, render_template, request
import os
import logging
from logging.handlers import RotatingFileHandler

# Import extensions from extensions.py
from .extensions import db, migrate, login_manager, csrf

def create_app():
    app = Flask(__name__)
    
    # Configure app
    try:
        from config import Config
        app.config.from_object(Config)
    except ImportError:
        app.config.update(
            SECRET_KEY=os.environ.get('SECRET_KEY', 'dette-er-en-hemmelighet'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///aksjeradar.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            STRIPE_SECRET_KEY=os.environ.get('STRIPE_SECRET_KEY'),
            EXPORT_FOLDER=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/exports'),
            WTF_CSRF_TIME_LIMIT=3600  # CSRF token validity period in seconds
        )
    
    # Set up logging
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configure logging
    file_handler = RotatingFileHandler('logs/aksjeradar.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Aksjeradar startup')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)  # Initialize CSRF protection
    
    # Register blueprints
    from .routes.main import main
    from .routes.stocks import stocks
    from .routes.analysis import analysis
    from .routes.portfolio import portfolio
    from .routes.stripe_routes import stripe_routes
    
    app.register_blueprint(main)
    app.register_blueprint(stocks, url_prefix='/stocks')
    app.register_blueprint(analysis, url_prefix='/analysis')
    app.register_blueprint(portfolio, url_prefix='/portfolio')
    app.register_blueprint(stripe_routes, url_prefix='/stripe')
    
    # Create required directories
    try:
        os.makedirs(app.config['EXPORT_FOLDER'], exist_ok=True)
    except Exception as e:
        app.logger.error(f'Failed to create export folder: {str(e)}')
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        app.logger.error(f'500 Error: {str(error)}')
        return render_template('500.html'), 500
    
    # Add Jinja2 filter for datetime
    @app.template_filter('now')
    def _jinja2_filter_now(format_string):
        from datetime import datetime
        return datetime.now().strftime(format_string)
    
    return app
