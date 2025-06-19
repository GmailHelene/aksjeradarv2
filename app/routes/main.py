from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from ..services.data_service import DataService
from ..models.user import User
from ..extensions import db
from ..utils.subscription import subscription_required
import time
import os
import stripe
from datetime import datetime, timedelta

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

@main.route('/subscription')
def subscription():
    """Subscription page for premium features"""
    trial_remaining = None
    if current_user.is_authenticated:
        if current_user.is_in_trial_period():
            # Calculate remaining trial time in minutes
            now = datetime.utcnow()
            trial_end = current_user.trial_start + timedelta(minutes=10)
            trial_remaining = max(0, int((trial_end - now).total_seconds() / 60))
    
    return render_template('subscription.html', 
                          trial_remaining=trial_remaining,
                          subscription_active=current_user.is_authenticated and current_user.has_active_subscription() if current_user.is_authenticated else False)

@main.route('/start-trial', methods=['POST'])
@login_required
def start_trial():
    """Start free trial for the current user"""
    if not current_user.trial_used:
        current_user.start_free_trial()
        db.session.commit()
        flash('Din 10-minutters gratis prøveperiode har startet!', 'success')
    else:
        flash('Du har allerede brukt din gratis prøveperiode.', 'warning')
    
    return redirect(url_for('main.subscription'))

@main.route('/purchase-subscription', methods=['POST'])
@login_required
def purchase_subscription():
    """Handle subscription purchase (dummy implementation)"""
    subscription_type = request.form.get('subscription_type')
    
    # In a real implementation, you would:
    # 1. Process payment with a payment provider (Stripe, PayPal, etc.)
    # 2. Verify payment was successful
    # 3. Then update user's subscription status
    
    # For demo purposes, we'll just update the subscription directly
    if subscription_type == 'monthly':
        current_user.has_subscription = True
        current_user.subscription_type = 'monthly'
        current_user.subscription_start = datetime.utcnow()
        current_user.subscription_end = datetime.utcnow() + timedelta(days=30)
        flash('Takk for kjøpet! Du har nå et månedsabonnement.', 'success')
    
    elif subscription_type == 'yearly':
        current_user.has_subscription = True
        current_user.subscription_type = 'yearly'
        current_user.subscription_start = datetime.utcnow()
        current_user.subscription_end = datetime.utcnow() + timedelta(days=365)
        flash('Takk for kjøpet! Du har nå et årsabonnement.', 'success')
    
    elif subscription_type == 'lifetime':
        current_user.has_subscription = True
        current_user.subscription_type = 'lifetime'
        current_user.subscription_start = datetime.utcnow()
        current_user.subscription_end = None
        flash('Takk for kjøpet! Du har nå et livsvarig abonnement.', 'success')
    
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    """Oppretter en Stripe Checkout-sesjon for abonnement"""
    subscription_type = request.form.get('subscription_type')
    
    # Initialiser Stripe API-nøkkel
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    
    # Velg riktig pris-ID basert på abonnementstype
    if subscription_type == 'monthly':
        price_id = current_app.config['STRIPE_MONTHLY_PRICE_ID']
        mode = 'subscription'
    elif subscription_type == 'yearly':
        price_id = current_app.config['STRIPE_YEARLY_PRICE_ID']
        mode = 'subscription'
    elif subscription_type == 'lifetime':
        price_id = current_app.config['STRIPE_LIFETIME_PRICE_ID']
        mode = 'payment'
    else:
        flash('Ugyldig abonnementstype', 'danger')
        return redirect(url_for('main.subscription'))        # Opprett Checkout-sesjon
    try:
        # Check if user already has a Stripe customer ID
        if current_user.stripe_customer_id:
            customer_id = current_user.stripe_customer_id
        elif current_user.email:
            # Create a new customer
            customer = stripe.Customer.create(
                email=current_user.email,
                name=current_user.username,
                metadata={
                    'user_id': str(current_user.id)
                }
            )
            customer_id = customer.id
            # Save the customer ID to the user
            current_user.stripe_customer_id = customer_id
            db.session.commit()
        else:
            customer_id = None
            
        checkout_session = stripe.checkout.Session.create(
            customer=customer_id,
            customer_email=None if customer_id else current_user.email,
            client_reference_id=str(current_user.id),
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode=mode,
            success_url=request.host_url + 'payment/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.host_url + 'subscription',
            metadata={
                'user_id': current_user.id,
                'subscription_type': subscription_type
            }
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        current_app.logger.error(f"Stripe error: {str(e)}")
        flash(f'Det oppstod en feil: {str(e)}', 'danger')
        return redirect(url_for('main.subscription'))

@main.route('/payment/success')
@login_required
def payment_success():
    """Håndterer vellykket betaling"""
    session_id = request.args.get('session_id')
    if not session_id:
        return redirect(url_for('main.subscription'))
    
    try:
        # Initialiser Stripe API-nøkkel
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
          # Hent Checkout-sesjonen for å bekrefte betaling
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        
        # Verifiser at bruker-ID matcher
        if str(current_user.id) != checkout_session.client_reference_id:
            flash('Ugyldig betalingssesjon', 'danger')
            return redirect(url_for('main.subscription'))
        
        # Lagre Stripe Customer ID hvis tilgjengelig
        if hasattr(checkout_session, 'customer') and checkout_session.customer and not current_user.stripe_customer_id:
            current_user.stripe_customer_id = checkout_session.customer
        
        # Oppdater brukerens abonnementsstatus
        subscription_type = checkout_session.metadata.get('subscription_type')
        if subscription_type == 'monthly':
            current_user.has_subscription = True
            current_user.subscription_type = 'monthly'
            current_user.subscription_start = datetime.utcnow()
            current_user.subscription_end = datetime.utcnow() + timedelta(days=30)
        elif subscription_type == 'yearly':
            current_user.has_subscription = True
            current_user.subscription_type = 'yearly'
            current_user.subscription_start = datetime.utcnow()
            current_user.subscription_end = datetime.utcnow() + timedelta(days=365)
        elif subscription_type == 'lifetime':
            current_user.has_subscription = True
            current_user.subscription_type = 'lifetime'
            current_user.subscription_start = datetime.utcnow()
            current_user.subscription_end = None
        
        db.session.commit()
        flash('Takk for kjøpet! Du har nå et aktivt abonnement.', 'success')
        return redirect(url_for('main.index'))
    except Exception as e:
        current_app.logger.error(f"Stripe payment success error: {str(e)}")
        flash(f'Det oppstod en feil ved bekreftelse av betalingen: {str(e)}', 'danger')
        return redirect(url_for('main.subscription'))

@main.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    """Håndterer Stripe webhook-hendelser"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = current_app.config['STRIPE_WEBHOOK_SECRET']
    
    # Initialiser Stripe API-nøkkel
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        # Ugyldig payload
        current_app.logger.error(f"Stripe webhook error (Invalid payload): {str(e)}")
        return jsonify(success=False), 400
    except stripe.error.SignatureVerificationError as e:
        # Ugyldig signatur
        current_app.logger.error(f"Stripe webhook error (Invalid signature): {str(e)}")
        return jsonify(success=False), 400
    
    # Håndter hendelsen
    try:
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            _handle_checkout_session(session)
        elif event['type'] == 'customer.subscription.updated':
            subscription = event['data']['object']
            _handle_subscription_updated(subscription)
        elif event['type'] == 'customer.subscription.deleted':
            subscription = event['data']['object']
            _handle_subscription_deleted(subscription)
    except Exception as e:
        current_app.logger.error(f"Stripe webhook processing error: {str(e)}")
        return jsonify(success=False, error=str(e)), 500
    
    return jsonify(success=True)

def _handle_checkout_session(session):
    """Håndterer fullført checkout-sesjon"""
    user_id = session.get('client_reference_id')
    if not user_id:
        return
    
    user = User.query.get(int(user_id))
    if not user:
        return
    
    # Oppdater brukerens abonnementsstatus basert på betalingen
    subscription_type = session.metadata.get('subscription_type')
    if subscription_type == 'monthly':
        user.has_subscription = True
        user.subscription_type = 'monthly'
        user.subscription_start = datetime.utcnow()
        user.subscription_end = datetime.utcnow() + timedelta(days=30)
    elif subscription_type == 'yearly':
        user.has_subscription = True
        user.subscription_type = 'yearly'
        user.subscription_start = datetime.utcnow()
        user.subscription_end = datetime.utcnow() + timedelta(days=365)
    elif subscription_type == 'lifetime':
        user.has_subscription = True
        user.subscription_type = 'lifetime'
        user.subscription_start = datetime.utcnow()
        user.subscription_end = None
    
    db.session.commit()

def _handle_subscription_updated(subscription):
    """Håndterer oppdatert abonnement"""
    customer_id = subscription.get('customer')
    if not customer_id:
        return
    
    user = User.query.filter_by(stripe_customer_id=customer_id).first()
    if not user:
        return
    
    status = subscription.get('status')
    
    if status == 'active':
        # Abonnement er aktivt
        user.has_subscription = True
        
        # Sjekk abonnement type basert på pris
        price_id = subscription.get('items', {}).get('data', [{}])[0].get('price', {}).get('id', '')
        
        if price_id == current_app.config['STRIPE_MONTHLY_PRICE_ID']:
            user.subscription_type = 'monthly'
            # Sett utløpsdato til neste fakturadato
            user.subscription_end = datetime.fromtimestamp(subscription.get('current_period_end', 0))
        elif price_id == current_app.config['STRIPE_YEARLY_PRICE_ID']:
            user.subscription_type = 'yearly'
            # Sett utløpsdato til neste fakturadato
            user.subscription_end = datetime.fromtimestamp(subscription.get('current_period_end', 0))
    elif status in ['canceled', 'unpaid', 'past_due']:
        # Abonnement er kansellert eller ikke betalt
        if user.subscription_type in ['monthly', 'yearly']:
            user.has_subscription = False
    
    db.session.commit()
    
def _handle_subscription_deleted(subscription):
    """Håndterer kansellert abonnement"""
    customer_id = subscription.get('customer')
    if not customer_id:
        return
    
    user = User.query.filter_by(stripe_customer_id=customer_id).first()
    if not user:
        return
    
    # Hvis brukeren har et abonnement som ikke er livstid, deaktiver det
    if user.subscription_type in ['monthly', 'yearly']:
        user.has_subscription = False
        # La utløpsdatoen være uendret for referanse
    
    db.session.commit()