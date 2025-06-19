from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

# Endre denne importlinjen
from ..extensions import db, login_manager  # Bruk relative imports

class User(UserMixin, db.Model):
    __tablename__ = 'users'  # <-- Viktig!
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    portfolios = db.relationship('Portfolio', backref='user', lazy='dynamic')
    watchlists = db.relationship('Watchlist', backref='user', lazy='dynamic')
      # Subscription fields
    has_subscription = db.Column(db.Boolean, default=False)
    subscription_type = db.Column(db.String(20), default='free')  # 'free', 'monthly', 'yearly', 'lifetime'
    subscription_start = db.Column(db.DateTime, nullable=True)
    subscription_end = db.Column(db.DateTime, nullable=True)
    trial_used = db.Column(db.Boolean, default=False)
    trial_start = db.Column(db.DateTime, nullable=True)
    stripe_customer_id = db.Column(db.String(128), nullable=True)  # For å lagre Stripe Customer ID
    
    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def start_free_trial(self):
        """Start the free trial for this user"""
        if not self.trial_used:
            self.trial_used = True
            self.trial_start = datetime.utcnow()
            return True
        return False
    
    def is_in_trial_period(self):
        """Check if the user is in their free trial period (10 minutes)"""
        if not self.trial_used or not self.trial_start:
            return False
        
        # Trial period is 10 minutes
        trial_end = self.trial_start + timedelta(minutes=10)
        return datetime.utcnow() <= trial_end
    
    def is_trial_expired(self):
        """Check if the trial period has expired"""
        if not self.trial_used:
            return False
        
        # Trial period is 10 minutes
        trial_end = self.trial_start + timedelta(minutes=10)
        return datetime.utcnow() > trial_end
    
    def has_active_subscription(self):
        """Check if the user has an active subscription"""
        # If user has a subscription and it's not expired
        if self.has_subscription and self.subscription_end:
            return datetime.utcnow() <= self.subscription_end
        
        # Or if they have a lifetime subscription
        if self.has_subscription and self.subscription_type == 'lifetime':
            return True
        
        # Or if they're in trial period
        return self.is_in_trial_period()
    
    def can_access_content(self):
        """Check if the user can access premium content"""
        # If user has an active subscription
        if self.has_active_subscription():
            return True
        
        # If user hasn't started trial yet
        if not self.trial_used:
            return True
        
        # If user is in trial period
        return self.is_in_trial_period()
    
    def subscription_days_left(self):
        """Return the number of days left in the subscription"""
        if not self.has_subscription or not self.subscription_end:
            return 0
        
        delta = self.subscription_end - datetime.utcnow()
        return max(0, delta.days)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))