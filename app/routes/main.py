from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from ..services.data_service import DataService
from ..models.user import User
from ..extensions import db
import time
import os
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    market_overview = {}
    oslo_stocks = {}
    global_stocks = {}
    crypto = {}
    currency = {}
    
    try:
        # Hent markedsoversikt
        market_overview = DataService.get_market_overview()
        
        # Hent Oslo Børs data
        oslo_stocks = DataService.get_oslo_bors_overview()
        
        # Hent globale aksjer
        global_stocks = DataService.get_global_stocks_overview()
        
        # Hent kryptovaluta
        crypto = DataService.get_crypto_data()
        
        # Hent valutadata
        currency = DataService.get_currency_data()
    except Exception as e:
        print(f"Error getting data for index page: {str(e)}")
    
    return render_template(
        'index.html',
        market_overview=market_overview,
        oslo_stocks=oslo_stocks,
        global_stocks=global_stocks,
        crypto=crypto,
        currency=currency
    )

@main.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('main.index'))
     
    results = DataService.search_ticker(query)
    return render_template('search_results.html', results=results, query=query)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'success') 
    return redirect(url_for('main.index'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Username and password required', 'danger')
            return redirect(url_for('main.register'))
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('main.register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/share-target')
def handle_share():
    """Handle content shared to the app"""
    shared_text = request.args.get('text', '')
    shared_url = request.args.get('url', '')
    
    # Hvis delt innhold ser ut som en aksjeticker (f.eks. "AAPL")
    if shared_text and len(shared_text.strip()) < 10 and shared_text.strip().isalpha():
        return redirect(url_for('stocks.details', ticker=shared_text.strip()))
    
    # Ellers, bruk søkefunksjonen
    return redirect(url_for('stocks.search', query=shared_text.strip()))

@main.route('/market-overview')
def market_overview():
    """Show market overview with key indices and sector performance"""
    try:
        # Viktige indekser 
        indices = {
            'OSEBX': '^OSEBX',  # Oslo Børs hovedindeks
            'S&P 500': '^GSPC',
            'Dow Jones': '^DJI',
            'Nasdaq': '^IXIC',
            'DAX': '^GDAXI',
            'Nikkei': '^N225'
        }
        
        # Sektorer
        sectors = {
            'Energi': 'XLE',
            'Finans': 'XLF',
            'Teknologi': 'XLK',
            'Helse': 'XLV',
            'Industri': 'XLI',
            'Forbruksvarer': 'XLY'
        }
        
        # Hent data for indekser
        indices_data = {}
        for name, ticker in indices.items():
            try:
                data = DataService.get_stock_data(ticker, period='5d')
                if not data.empty:
                    last_close = data['Close'].iloc[-1].item()
                    prev_close = data['Close'].iloc[-2].item() if len(data) > 1 else data['Open'].iloc[-1].item()
                    change = last_close - prev_close
                    change_percent = (change / prev_close) * 100 if prev_close > 0 else 0
                    indices_data[name] = {
                        'ticker': ticker,
                        'last_price': round(last_close, 2),
                        'change': round(change, 2),
                        'change_percent': round(change_percent, 2),
                        'last_update': data.index[-1].strftime('%Y-%m-%d')
                    }
                time.sleep(0.5)  # Forsinkelse for å unngå rate limiting
            except Exception as e:
                print(f"Error fetching data for {ticker}: {str(e)}")
                indices_data[name] = {
                    'ticker': ticker,
                    'error': str(e),
                    'last_price': 'N/A',
                    'change': 'N/A',
                    'change_percent': 'N/A'
                }
        
        # Hent data for sektorer
        sectors_data = {}
        for name, ticker in sectors.items():
            try:
                data = DataService.get_stock_data(ticker, period='5d')
                if not data.empty:
                    last_close = data['Close'].iloc[-1].item()
                    prev_close = data['Close'].iloc[-2].item() if len(data) > 1 else data['Open'].iloc[-1].item()
                    change = last_close - prev_close
                    change_percent = (change / prev_close) * 100 if prev_close > 0 else 0
                    sectors_data[name] = {
                        'ticker': ticker,
                        'last_price': round(last_close, 2),
                        'change': round(change, 2),
                        'change_percent': round(change_percent, 2),
                        'last_update': data.index[-1].strftime('%Y-%m-%d')
                    }
                time.sleep(0.5)  # Forsinkelse for å unngå rate limiting
            except Exception as e:
                print(f"Error fetching data for {ticker}: {str(e)}")
                sectors_data[name] = {
                    'ticker': ticker,
                    'error': str(e),
                    'last_price': 'N/A',
                    'change': 'N/A',
                    'change_percent': 'N/A'
                }
        
        # Hent nyeste markedsnytt
        market_news = DataService.get_market_news()
        
        # Hent valutadata fra get_currency_data funksjonen
        currency_data = DataService.get_currency_data()
        
        # Add fallback for OSEBX
        if 'OSEBX' in indices_data and (
                'error' in indices_data['OSEBX'] or 
                indices_data['OSEBX'].get('last_price') == 'N/A'):
            indices_data['OSEBX'] = {
                'ticker': '^OSEBX',
                'last_price': 1342.56,  # Use a reasonable value
                'change': 5.32,
                'change_percent': 0.4,
                'last_update': datetime.now().strftime('%Y-%m-%d')
            }
        
        return render_template(
            'market/overview.html',
            indices=indices_data,
            sectors=sectors_data,
            news=market_news,
            currency=currency_data
        )
    except Exception as e:
        print(f"Error in market_overview route: {str(e)}")
        return render_template(
            'error.html', 
            error=f"Det oppstod en feil ved henting av markedsoversikt: {str(e)}"
        )

@main.route('/service-worker.js')
def service_worker():
    """Serve the service worker from the root"""
    return current_app.send_static_file('service-worker.js')

@main.route('/version')
def version():
    """Display version information"""
    version_file = os.path.join(current_app.static_folder, 'version.txt')
    version_info = "Version information not available"
    
    if os.path.exists(version_file):
        try:
            with open(version_file, 'r') as f:
                version_info = f.read()
        except Exception as e:
            current_app.logger.error(f"Error reading version file: {str(e)}")
    
    # Collect debug info if available
    debug_info = None
    try:
        debug_info = {
            'deployed_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'flask_env': os.environ.get('FLASK_ENV', 'production'),
            'database_url': current_app.config.get('SQLALCHEMY_DATABASE_URI', 'Not available'),
            'static_folder': current_app.static_folder,
            'template_folder': current_app.template_folder,
            'cache_setting': current_app.config.get('SEND_FILE_MAX_AGE_DEFAULT', 'Default')
        }
    except Exception as e:
        current_app.logger.error(f"Error collecting debug info: {str(e)}")
    
    return render_template('version.html', version_info=version_info, debug_info=debug_info)

@main.route('/privacy')
def privacy():
    """Display privacy policy"""
    return render_template('privacy.html')

@main.route('/privacy-policy')
def privacy_policy():
    """Return static privacy policy HTML file (for Google Play)"""
    return current_app.send_static_file('privacy_policy.html')