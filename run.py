import os
from flask import Flask
from app.extensions import db, login_manager, migrate

app = Flask(__name__,
            static_folder='app/static',
            template_folder='app/templates')

# Configure app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dette-er-en-hemmelighet'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///app/aksjeradar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
migrate.init_app(app, db)

# Register blueprints
with app.app_context():
    from app.routes.main import main
    from app.routes.stocks import stocks
    from app.routes.analysis import analysis
    from app.routes.portfolio import portfolio
    
    app.register_blueprint(main)
    app.register_blueprint(stocks, url_prefix='/stocks')
    app.register_blueprint(analysis, url_prefix='/analysis')
    app.register_blueprint(portfolio, url_prefix='/portfolio')
    
    # Register models - needed for Flask-Migrate
    from app.models.user import User
    from app.models.portfolio import Portfolio, PortfolioStock, StockTip
    from app.models.stock import Watchlist, WatchlistStock

# Register Jinja2 filter
@app.template_filter('now')
def _jinja2_filter_now(format_string):
    from datetime import datetime
    return datetime.now().strftime(format_string)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)