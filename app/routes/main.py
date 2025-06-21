from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, jsonify, session, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from ..services.data_service import DataService
from ..models.user import User
from ..extensions import db
from ..utils.subscription import subscription_required
from ..utils.trial import trial_required
from ..forms import LoginForm, RegistrationForm  # Import the forms
from urllib.parse import urlparse, urljoin
from datetime import datetime, timedelta
import time
import os
import stripe

main = Blueprint('main', __name__)

def url_is_safe(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def init_stripe():
    """Initialize Stripe with error handling"""
    try:
        stripe.api_key = current_app.config['STRIPE_SECRET_KEY']
        # Test the connection by making a simple API call
        stripe.Price.list(limit=1)
        current_app.logger.info('Stripe initialized successfully')
    except stripe.error.AuthenticationError as e:
        current_app.logger.error(f'Stripe authentication failed: {str(e)}')
        raise
    except Exception as e:
        current_app.logger.error(f'Stripe initialization failed: {str(e)}')
        raise

# Initialize Stripe when the blueprint is registered
@main.record_once
def on_register(state):
    try:
        # Set Stripe API key
        stripe.api_key = state.app.config['STRIPE_SECRET_KEY']
        
        # Test the connection by making a simple API call
        stripe.Price.list(limit=1)
        state.app.logger.info('Stripe initialized successfully')
        else:
            state.app.logger.info('Stripe initialized in development mode (no API calls)')
    except Exception as e:
        state.app.logger.error(f'Failed to initialize Stripe during blueprint registration: {str(e)}')

@main.route('/')
def index():
    """Home page"""
    try:
        # Get market data for the homepage
        oslo_stocks = DataService.get_oslo_bors_overview(limit=5)
        global_stocks = DataService.get_global_stocks_overview(limit=5)
        crypto = DataService.get_crypto_overview(limit=5)
        currency = DataService.get_currency_overview()
        
        # Check if user needs to be prompted about trial/subscription
        show_trial_prompt = False
        if current_user.is_authenticated:
            if not current_user.is_premium and not current_user.trial_used:
                show_trial_prompt = True
        
        return render_template(
            'index.html',
            oslo_stocks=oslo_stocks,
            global_stocks=global_stocks,
            crypto=crypto,
            currency=currency
        )
    except Exception as e:
        current_app.logger.error(f"Error in index route: {str(e)}")
        flash("En feil oppstod ved henting av markedsdata. Vennligst prøv igjen senere.", "error")
        return render_template('index.html')

@main.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('main.index'))
     
    results = DataService.search_ticker(query)
    return render_template('search_results.html', results=results, query=query)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Du er nå logget inn!', 'success')
            next_page = request.args.get('next')
            if next_page and url_is_safe(next_page):
                return redirect(next_page)
            return redirect(url_for('main.index'))
        else:
            flash('Ugyldig brukernavn eller passord', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Du er nå logget ut', 'success') 
    return redirect(url_for('main.index'))

def unauthorized_handler():
    flash('Du må logge inn for å få tilgang til denne siden.', 'warning')
    return redirect(url_for('main.login', next=request.url))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Log registration attempt
        current_app.logger.info(f'Registration attempt for username: {form.username.data}')
        
        try:
            # Create user
            user = User(
                username=form.username.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            
            # Start free trial
            user.start_free_trial()
            
            # Save to database
            db.session.add(user)
            db.session.commit()
            
            # Log success
            current_app.logger.info(f'New user registered: {username}')
            
            # Login the user
            login_user(user)
            flash('Registrering vellykket! Velkommen til Aksjeradar.', 'success')
            
            return redirect(url_for('main.index'))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Registration failed for {username}: {str(e)}')
            flash('Beklager, det oppstod en feil under registreringen. Prøv igjen.', 'danger')
            return redirect(url_for('main.register'))
            
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

@main.route('/manifest.json')
def manifest():
    """Serve the manifest.json file for PWA support"""
    try:
        return send_from_directory('static', 'manifest.json')
    except Exception as e:
        current_app.logger.error(f"Error serving manifest.json: {str(e)}")
        return jsonify({'error': 'Manifest not found'}), 404

@main.route('/version')
def version():
    """Return the current version of the application"""
    try:
        with open('static/version.txt', 'r') as f:
            version = f.read().strip()
        return jsonify({'version': version})
    except Exception as e:
        current_app.logger.error(f"Error reading version: {str(e)}")
        return jsonify({'version': 'unknown'})

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
    """Show subscription options"""
    show_trial = request.args.get('trial', False)
    is_expired = request.args.get('expired', False)
    
    # If trial is expired, show the subscription template with expired message
    if is_expired:
        return render_template('subscription.html', 
                             show_trial=False,
                             is_expired=True,
                             title="Prøveperioden er utløpt")
    
    # If trial is available, show trial option
    if show_trial:
        return render_template('subscription.html', 
                             show_trial=True,
                             is_expired=False,
                             title="Start din prøveperiode")
    
    # Default view shows all subscription options
    return render_template('subscription.html', 
                         show_trial=False,
                         is_expired=False,
                         title="Velg abonnement")

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
    """Create a Stripe checkout session for subscription purchase"""
    subscription_type = request.form.get('subscription_type')
    if not subscription_type:
        return jsonify({'error': 'No subscription type provided'}), 400

    price_id = None
    if subscription_type == 'monthly':
        price_id = current_app.config['STRIPE_MONTHLY_PRICE_ID']
    elif subscription_type == 'yearly':
        price_id = current_app.config['STRIPE_YEARLY_PRICE_ID']
    elif subscription_type == 'lifetime':
        price_id = current_app.config['STRIPE_LIFETIME_PRICE_ID']
    else:
        return jsonify({'error': 'Invalid subscription type'}), 400

    try:
        # Create or retrieve Stripe customer
        if not current_user.stripe_customer_id:
            customer = stripe.Customer.create(
                email=current_user.email,
                metadata={'user_id': current_user.id}
            )
            current_user.stripe_customer_id = customer.id
            db.session.commit()
        
        # Create checkout session
        session = stripe.checkout.Session.create(
            customer=current_user.stripe_customer_id,
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=request.host_url.rstrip('/') + url_for('main.payment_success'),
            cancel_url=request.host_url.rstrip('/') + url_for('main.subscription'),
            metadata={
                'user_id': current_user.id,
                'subscription_type': subscription_type
            }
        )
        
        return jsonify({'sessionId': session.id})
    except Exception as e:
        current_app.logger.error(f'Failed to create checkout session: {str(e)}')
        return jsonify({'error': 'Failed to create checkout session'}), 500

@main.route('/payment/success')
@login_required
def payment_success():
    """Handle successful payment and subscription activation"""
    flash('Takk for kjøpet! Ditt abonnement er nå aktivert.', 'success')
    return redirect(url_for('main.subscription'))

@main.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, current_app.config['STRIPE_WEBHOOK_SECRET']
        )
    except ValueError as e:
        current_app.logger.error(f'Invalid payload: {str(e)}')
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError as e:
        current_app.logger.error(f'Invalid signature: {str(e)}')
        return 'Invalid signature', 400

    try:
        if event.type == 'checkout.session.completed':
            handle_checkout_session(event.data.object)
        elif event.type == 'customer.subscription.updated':
            handle_subscription_update(event.data.object)
        elif event.type == 'customer.subscription.deleted':
            handle_subscription_deleted(event.data.object)
    except Exception as e:
        current_app.logger.error(f'Error handling webhook {event.type}: {str(e)}')
        return jsonify({'error': str(e)}), 500

    return jsonify({'status': 'success'})

def handle_checkout_session(session):
    """Handle completed checkout session"""
    user_id = int(session.metadata.get('user_id'))
    subscription_type = session.metadata.get('subscription_type')
    
    user = User.query.get(user_id)
    if not user:
        current_app.logger.error(f'User not found: {user_id}')
        return
    
    try:
        # Update user subscription
        user.has_subscription = True
        user.subscription_type = subscription_type
        user.subscription_start = datetime.utcnow()
        
        if subscription_type == 'monthly':
            user.subscription_end = datetime.utcnow() + timedelta(days=30)
        elif subscription_type == 'yearly':
            user.subscription_end = datetime.utcnow() + timedelta(days=365)
        elif subscription_type == 'lifetime':
            user.subscription_end = None
        
        db.session.commit()
        current_app.logger.info(f'Subscription activated for user {user_id}')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Failed to update subscription for user {user_id}: {str(e)}')
        raise

def handle_subscription_update(subscription):
    """Handle subscription updates"""
    try:
        customer_id = subscription.customer
        user = User.query.filter_by(stripe_customer_id=customer_id).first()
        
        if not user:
            current_app.logger.error(f'User not found for Stripe customer: {customer_id}')
            return
        
        # Update subscription status
        user.has_subscription = subscription.status == 'active'
        if subscription.status == 'active':
            if subscription.cancel_at:
                user.subscription_end = datetime.fromtimestamp(subscription.cancel_at)
            elif subscription.current_period_end:
                user.subscription_end = datetime.fromtimestamp(subscription.current_period_end)
        
        db.session.commit()
        current_app.logger.info(f'Subscription updated for user {user.id}')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Failed to update subscription: {str(e)}')
        raise

def handle_subscription_deleted(subscription):
    """Handle subscription cancellation"""
    try:
        customer_id = subscription.customer
        user = User.query.filter_by(stripe_customer_id=customer_id).first()
        
        if not user:
            current_app.logger.error(f'User not found for Stripe customer: {customer_id}')
            return
        
        # Update user subscription status
        user.has_subscription = False
        user.subscription_end = datetime.utcnow()
        
        db.session.commit()
        current_app.logger.info(f'Subscription cancelled for user {user.id}')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Failed to cancel subscription: {str(e)}')
        raise

@main.route('/trial-expired')
def trial_expired():
    """Show the trial expired page with subscription options"""
    # If user is already subscribed, redirect to home
    if current_user.is_authenticated and current_user.has_active_subscription():
        return redirect(url_for('main.index'))
        
    return render_template(
        'trial-expired.html',
        monthly_price=99,
        yearly_price=799,
        yearly_savings=33,  # Savings percentage for yearly plan
        stripe_public_key=current_app.config['STRIPE_PUBLIC_KEY']
    )

@main.route('/contact')
def contact():
    """Show contact page"""
    return render_template('contact.html')

@main.route('/contact/submit', methods=['POST'])
def contact_submit():
    """Handle contact form submission"""
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Log the contact form submission
        current_app.logger.info(f"Contact form submission from {name} ({email}): {subject}")
        
        # Here you would typically send an email or store in database
        # For now, we'll just show a success message
        
        flash('Takk for din henvendelse! Vi vil svare deg så snart som mulig.', 'success')
        return redirect(url_for('main.contact'))
    except Exception as e:
        current_app.logger.error(f"Error processing contact form: {str(e)}")
        flash('Det oppstod en feil ved sending av skjemaet. Vennligst prøv igjen.', 'danger')
        return redirect(url_for('main.contact'))

@main.route('/api/oslo_stocks')
@trial_required
def get_oslo_stocks():
    try:
        data = DataService.get_oslo_bors_overview()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/global_stocks')
@trial_required
def get_global_stocks():
    try:
        data = DataService.get_global_stocks_overview()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/crypto')
@trial_required
def get_crypto():
    try:
        data = DataService.get_crypto_list()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/currency')
@trial_required
def get_currency():
    try:
        data = DataService.get_currency_list()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/offline')
def offline():
    """Show offline page"""
    return render_template('offline.html')