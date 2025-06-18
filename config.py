from dotenv import load_dotenv
load_dotenv()  # Legg til dette kallet for å laste miljøvariabler
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dette-er-en-hemmelighet'  # Legg til SECRET_KEY
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///aksjeradar.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Brukersesjoner
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
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
    EMAIL_SENDER = os.environ.get('EMAIL_SENDER') or 'Aksjeradar <noreply@aksjeradar.no>'
    
    # Export configurations
    EXPORT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/exports')
    
    # Ensure export folder exists
    os.makedirs(EXPORT_FOLDER, exist_ok=True)