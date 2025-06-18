from flask import Flask
import os

# Import extensions from extensions.py instead of redefining
from .extensions import db, login_manager, migrate

def create_app():
    app = Flask(__name__)
    
    # Konfigurer app
    try:
        from config import Config
        app.config.from_object(Config)
    except ImportError:
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dette-er-en-hemmelighet'
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///aksjeradar.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialiser utvidelser
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Registrer blueprints
    with app.app_context():
        from .routes.main import main
        from .routes.stocks import stocks
        from .routes.analysis import analysis
        from .routes.portfolio import portfolio
        
        app.register_blueprint(main)
        app.register_blueprint(stocks, url_prefix='/stocks')
        app.register_blueprint(analysis, url_prefix='/analysis')
        app.register_blueprint(portfolio, url_prefix='/portfolio')
        
        # Registrer modellene
        from .models.user import User
        from .models.portfolio import Portfolio, PortfolioStock, StockTip
        from .models.stock import Watchlist, WatchlistStock
    
    # Legg til Jinja2 filter
    @app.template_filter('now')
    def _jinja2_filter_now(format_string):
        from datetime import datetime
        return datetime.now().strftime(format_string)
    
    return app