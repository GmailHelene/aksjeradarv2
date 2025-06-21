from dotenv import load_dotenv
load_dotenv()  # Legg til dette kallet for å laste miljøvariabler
import os
from datetime import timedelta

class Config:    # Security settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        if os.environ.get('FLASK_ENV') == 'production':
            raise ValueError('SECRET_KEY must be set in production environment')
        else:
            SECRET_KEY = 'dev-dette-er-en-hemmelighet-ikke-bruk-i-produksjon'
            print('Warning: Using development SECRET_KEY')
      # Database settings
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL:
        if os.environ.get('FLASK_ENV') == 'production':
            raise ValueError('DATABASE_URL must be set in production environment')
        else:
            # Make sure we use the full path for SQLite
            base_dir = os.path.abspath(os.path.dirname(__file__))
            instance_dir = os.path.join(base_dir, 'instance')
            if not os.path.exists(instance_dir):
                os.makedirs(instance_dir)
            
            DATABASE_URL = f'sqlite:///{os.path.join(instance_dir, "aksjeradar.db")}'
            print(f'Warning: Using SQLite database at {DATABASE_URL} for development')
    
    # Fix potential Railway.app PostgreSQL URL format
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Session settings
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flask_session')
    SESSION_FILE_THRESHOLD = 500  # Maximum number of files stored
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_PARTITIONED = True # Support for Chrome's CHIPS (Cookie Having Independent Partitioned State)
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    # Ensure proper session handling for APIs
    SESSION_REFRESH_EACH_REQUEST = True
    SESSION_COOKIE_NAME = 'aksjeradar_session'

    # Pagination
    STOCKS_PER_PAGE = 20

    # API-nøkler
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or 'your-openai-api-key'  # Legg til denne
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY') or 'your-news-api-key'  # Legg til denne

    # Email configurations
    EMAIL_SERVER = os.environ.get('EMAIL_SERVER') or 'smtp.gmail.com'
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT') or 465)
    EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME') or 'your-email@gmail.com'
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD') or 'your-email-password'
    EMAIL_SENDER = os.environ.get('EMAIL_SENDER') or 'Aksjeradar <noreply@aksjeradar.no>'    # Export configurations
    EXPORT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/exports')
    # Ensure export folder exists
    os.makedirs(EXPORT_FOLDER, exist_ok=True)    # Stripe settings
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
    if not STRIPE_PUBLISHABLE_KEY:
        if os.environ.get('FLASK_ENV') == 'production':
            raise ValueError('STRIPE_PUBLISHABLE_KEY must be set in production environment')
        else:
            STRIPE_PUBLISHABLE_KEY = 'pk_test_dummy_key_for_development'
            print('Warning: Using dummy Stripe publishable key for development')
    
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    if not STRIPE_SECRET_KEY:
        if os.environ.get('FLASK_ENV') == 'production':
            raise ValueError('STRIPE_SECRET_KEY must be set in production environment')
        else:
            STRIPE_SECRET_KEY = 'sk_test_dummy_key_for_development'
            print('Warning: Using dummy Stripe secret key for development')
    
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
    if not STRIPE_WEBHOOK_SECRET:
        if os.environ.get('FLASK_ENV') == 'production':
            raise ValueError('STRIPE_WEBHOOK_SECRET must be set in production environment')
        else:
            STRIPE_WEBHOOK_SECRET = 'whsec_dummy_webhook_secret_for_development'
            print('Warning: Using dummy Stripe webhook secret for development')

    # Stripe Product IDs
    STRIPE_MONTHLY_PRICE_ID = os.environ.get('STRIPE_MONTHLY_PRICE_ID')
    if not STRIPE_MONTHLY_PRICE_ID:
        if os.environ.get('FLASK_ENV') == 'production':
            raise ValueError('STRIPE_MONTHLY_PRICE_ID must be set in production environment')
        else:
            STRIPE_MONTHLY_PRICE_ID = 'price_dummy_monthly'
            print('Warning: Using dummy Stripe monthly price ID for development')
    
    STRIPE_YEARLY_PRICE_ID = os.environ.get('STRIPE_YEARLY_PRICE_ID')
    if not STRIPE_YEARLY_PRICE_ID:
        if os.environ.get('FLASK_ENV') == 'production':
            raise ValueError('STRIPE_YEARLY_PRICE_ID must be set in production environment')
        else:
            STRIPE_YEARLY_PRICE_ID = 'price_dummy_yearly'
            print('Warning: Using dummy Stripe yearly price ID for development')
    
    STRIPE_LIFETIME_PRICE_ID = os.environ.get('STRIPE_LIFETIME_PRICE_ID')
    if not STRIPE_LIFETIME_PRICE_ID:
        if os.environ.get('FLASK_ENV') == 'production':
            raise ValueError('STRIPE_LIFETIME_PRICE_ID must be set in production environment')
        else:
            STRIPE_LIFETIME_PRICE_ID = 'price_dummy_lifetime'
            print('Warning: Using dummy Stripe lifetime price ID for development')