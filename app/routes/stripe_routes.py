import stripe
from flask import current_app, request, jsonify, session, redirect, url_for
from flask_login import current_user, login_required

# Sett opp Stripe API-nøkkel
stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

@main.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    """Oppretter en Stripe Checkout-sesjon for abonnement"""
    subscription_type = request.form.get('subscription_type')
    
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
        return jsonify(error='Ugyldig abonnementstype'), 400
    
    # Opprett Checkout-sesjon
    try:
        checkout_session = stripe.checkout.Session.create(
            customer_email=current_user.email,
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
        return jsonify(error=str(e)), 500

@main.route('/payment/success')
@login_required
def payment_success():
    """Håndterer vellykket betaling"""
    session_id = request.args.get('session_id')
    if not session_id:
        return redirect(url_for('main.subscription'))
    
    try:
        # Hent Checkout-sesjonen for å bekrefte betaling
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        
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
        flash(f'Det oppstod en feil ved bekreftelse av betalingen: {str(e)}', 'danger')
        return redirect(url_for('main.subscription'))

@main.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    """Håndterer Stripe webhook-hendelser"""
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = current_app.config['STRIPE_WEBHOOK_SECRET']
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        # Ugyldig payload
        return jsonify(success=False), 400
    except stripe.error.SignatureVerificationError as e:
        # Ugyldig signatur
        return jsonify(success=False), 400
    
    # Håndter hendelsen
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_session(session)
    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        handle_subscription_updated(subscription)
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_deleted(subscription)
    
    return jsonify(success=True)

def handle_checkout_session(session):
    """Håndterer fullført checkout-sesjon"""
    user_id = session.get('client_reference_id')
    if not user_id:
        return
    
    user = User.query.get(int(user_id))
    if not user:
        return
    
    # Oppdater brukerens abonnementsstatus basert på betalingen
    # (Dette blir også håndtert i success-ruten, men webhooks gir en ekstra sikkerhet)
    
def handle_subscription_updated(subscription):
    """Håndterer oppdatert abonnement"""
    # Finn brukeren basert på Stripe-kunde-ID og oppdater abonnementsstatus
    
def handle_subscription_deleted(subscription):
    """Håndterer kansellert abonnement"""
    # Finn brukeren basert på Stripe-kunde-ID og oppdater abonnementsstatus