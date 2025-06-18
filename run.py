import os
from flask import Flask, render_template
import logging
from logging.handlers import RotatingFileHandler

# Sett opp logging først
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/aksjeradar.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(file_handler)
logging.getLogger().addHandler(console_handler)
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__,
            static_folder='app/static',
            template_folder='app/templates')

# Configure app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dette-er-en-hemmelighet'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///app/aksjeradar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['EXPORT_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/exports')

# Ensure export folder exists
os.makedirs(app.config['EXPORT_FOLDER'], exist_ok=True)

# Logging startup info
logger.info('Starting Aksjeradar application')
logger.info(f'Database URI: {app.config["SQLALCHEMY_DATABASE_URI"]}')

try:
    # Import extensions after app is created to avoid circular imports
    from app.extensions import db, login_manager, migrate

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    logger.info('Extensions initialized successfully')

    # Register Jinja2 filter
    @app.template_filter('now')
    def _jinja2_filter_now(format_string):
        from datetime import datetime
        return datetime.now().strftime(format_string)

    # Register error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        logger.error(f"404 error: {error}")
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"500 error: {error}")
        db.session.rollback()
        return render_template('500.html'), 500

    # Register blueprints in a with context to ensure proper app context
    with app.app_context():
        # Import models first to ensure they are registered with SQLAlchemy
        from app.models.user import User
        from app.models.portfolio import Portfolio, PortfolioStock, StockTip
        from app.models.stock import Watchlist, WatchlistStock
        logger.info('Models imported successfully')
        
        # Now import and register blueprints
        from app.routes.main import main
        from app.routes.stocks import stocks
        from app.routes.analysis import analysis
        from app.routes.portfolio import portfolio
        
        app.register_blueprint(main)
        app.register_blueprint(stocks, url_prefix='/stocks')
        app.register_blueprint(analysis, url_prefix='/analysis')
        app.register_blueprint(portfolio, url_prefix='/portfolio')
        logger.info('Blueprints registered successfully')

        # Initialize database if it doesn't exist
        try:
            db.create_all()
            logger.info('Database tables created successfully')
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")

except Exception as e:
    logger.error(f"Error during application setup: {e}")
    # Still provide a basic app with error information
    @app.route('/')
    def error_index():
        return f"""
        <html>
            <body>
                <h1>Aksjeradar - Application Error</h1>
                <p>An error occurred during application startup:</p>
                <pre>{str(e)}</pre>
                <p>Please check the logs for more information.</p>
            </body>
        </html>
        """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)