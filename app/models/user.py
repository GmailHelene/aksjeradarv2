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
    
    # Stripe fields
    stripe_customer_id = db.Column(db.String(255), nullable=True)
    subscription_id = db.Column(db.String(255), nullable=True)
    subscription_status = db.Column(db.String(50), nullable=True)
    
    # Admin field
    is_admin = db.Column(db.Boolean, default=False)
    
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
        """Check if the user is in their trial period"""
        if self.is_admin or self.email == 'helene721@gmail.com':
            return True
            
        if not self.trial_start:
            return False
            
        trial_end = self.trial_start + timedelta(days=14)
        return datetime.utcnow() <= trial_end
    
    def has_active_subscription(self):
        """Check if the user has an active subscription"""
        if self.is_admin or self.email == 'helene721@gmail.com':
            return True
            
        if self.subscription_type in ['monthly', 'yearly', 'lifetime'] and self.subscription_end:
            return datetime.utcnow() <= self.subscription_end
            
        return self.is_in_trial_period()
    
    @property
    def is_premium(self):
        """Check if user has premium access (either admin, specific email, or active subscription)"""
        return self.is_admin or self.email == 'helene721@gmail.com' or self.has_active_subscription()
    
    def subscription_days_left(self):
        """Return the number of days left in the subscription"""
        if not self.has_subscription or not self.subscription_end:
            return 0
        
        delta = self.subscription_end - datetime.utcnow()
        return max(0, delta.days)

    def has_active_subscription(self):
        if self.is_admin or self.email == 'helene721@gmail.com':
            return True
        if self.subscription_type and self.subscription_end and self.subscription_end > datetime.utcnow():
            return True
        return False
    
    def is_in_trial(self):
        if self.is_admin or self.email == 'helene721@gmail.com':
            return True
        if not self.trial_end:
            return False
        return datetime.utcnow() <= self.trial_end

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))