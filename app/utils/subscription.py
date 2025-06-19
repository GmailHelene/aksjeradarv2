from functools import wraps
from flask import redirect, url_for, flash, request, session
from flask_login import current_user
from datetime import datetime

def subscription_required(f):
    """
    Decorator to require an active subscription for certain routes.
    Will redirect to subscription page if user is not subscribed.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip this check for public pages and endpoints
        allowed_routes = [
            'main.index', 'main.login', 'main.register', 'main.subscription', 
            'main.privacy', 'main.privacy_policy', 'main.start_trial', 
            'main.service_worker', 'main.logout', 'main.search', 'main.version',
            'main.market_overview', 'static', 'stocks.index', 'stocks.search',
            'stocks.details'
        ]
        
        # Check if current endpoint is in allowed routes
        if request.endpoint:
            for allowed_route in allowed_routes:
                if request.endpoint.endswith(allowed_route):
                    return f(*args, **kwargs)
            
        # If user is not logged in, store the requested URL and redirect to login
        if not current_user.is_authenticated:
            session['next'] = request.url
            flash('Logg inn for å få tilgang til denne funksjonen.', 'info')
            return redirect(url_for('main.login'))
        
        # Check if user has an active subscription or is in trial
        if current_user.has_active_subscription():
            return f(*args, **kwargs)
        
        # If user has used their trial but it has expired
        if current_user.trial_used and not current_user.is_in_trial_period():
            flash('Din gratis prøveperiode er utløpt. Vennligst abonner for å fortsette.', 'warning')
            return redirect(url_for('main.subscription'))
        
        # If user hasn't used their trial yet, redirect to start trial
        if not current_user.trial_used:
            flash('Start din gratis prøveperiode for å få tilgang til alle funksjoner.', 'info')
            return redirect(url_for('main.subscription'))
        
        # Redirect to subscription page
        flash('Du trenger et aktivt abonnement for å få tilgang til denne funksjonen.', 'warning')
        return redirect(url_for('main.subscription'))
    
    return decorated_function
