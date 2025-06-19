from functools import wraps
from flask import redirect, url_for, session
from datetime import datetime, timedelta
from flask_login import current_user

def trial_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If user is not logged in
        if not current_user.is_authenticated:
            # Check session for trial start
            trial_start = session.get('anonymous_trial_start')
            if trial_start:
                # Convert string to datetime if needed
                if isinstance(trial_start, str):
                    trial_start = datetime.fromisoformat(trial_start)
                
                # Check if trial has expired
                trial_end = trial_start + timedelta(minutes=10)
                if datetime.utcnow() > trial_end:
                    return redirect(url_for('main.trial_expired'))
            else:
                # Start anonymous trial
                session['anonymous_trial_start'] = datetime.utcnow().isoformat()
        else:
            # For logged in users
            if not current_user.can_access_content():
                return redirect(url_for('main.trial_expired'))
        
        return f(*args, **kwargs)
    return decorated_function
