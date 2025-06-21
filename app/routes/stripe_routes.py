from flask import Blueprint, current_app, request, jsonify, session, redirect, url_for, flash
from flask_login import current_user, login_required
from ..models.user import User
from ..extensions import db
from datetime import datetime, timedelta
import stripe

stripe_routes = Blueprint('stripe', __name__)

@stripe_routes.record_once
def on_register(state):
    try:
        # Set Stripe API key
        stripe.api_key = state.app.config['STRIPE_SECRET_KEY']
        
        # Only test the connection in production
        if state.app.config['IS_REAL_PRODUCTION']:
            # Test the connection by making a simple API call
            stripe.Price.list(limit=1)
            state.app.logger.info('Stripe initialized successfully')
        else:
            state.app.logger.info('Stripe initialized with dummy keys for development')
    except Exception as e:
        state.app.logger.error(f'Failed to initialize Stripe during blueprint registration: {str(e)}')
        # Only raise in production
        if state.app.config['IS_REAL_PRODUCTION']:
            raise

@stripe_routes.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    """Create a Stripe checkout session for subscription purchase"""
    subscription_type = request.form.get('subscription_type')
    if not subscription_type:
        return jsonify({'error': 'No subscription type provided'}), 400

    price_id = None
    mode = 'subscription'
    if subscription_type == 'monthly':
        price_id = current_app.config['STRIPE_MONTHLY_PRICE_ID']
    elif subscription_type == 'yearly':
        price_id = current_app.config['STRIPE_YEARLY_PRICE_ID']
    elif subscription_type == 'lifetime':
        price_id = current_app.config['STRIPE_LIFETIME_PRICE_ID']
        mode = 'payment'
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
                'quantity': 1
            }],
            mode=mode,
            success_url=request.host_url.rstrip('/') + url_for('stripe.payment_success') + '?session_id={CHECKOUT_SESSION_ID}',
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

@stripe_routes.route('/payment/success')
@login_required
def payment_success():
    """Handle successful payment"""
    session_id = request.args.get('session_id')
    if not session_id:
        return redirect(url_for('main.subscription'))
    
    try:
        # Retrieve Checkout session to confirm payment
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        
        # Update user's subscription status based on subscription type
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
        flash(f'Det oppstod en feil ved bekreftelse av betalingen: {str(e)}', 'danger')
        return redirect(url_for('main.subscription'))

@stripe_routes.route('/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook events"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = current_app.config['STRIPE_WEBHOOK_SECRET']
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
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