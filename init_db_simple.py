from flask import Flask
from app import create_app
from app.extensions import db
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('db_init')

def init_database():
    # Create app instance
    app = create_app()
    
    # Ensure instance directory exists
    if not os.path.exists('instance'):
        os.makedirs('instance')
        logger.info("Created instance directory")
    
    with app.app_context():
        # Create all tables
        db.create_all()
        logger.info("Database tables created")
        
        # Try to check if User table exists
        from app.models.user import User
        try:
            user_count = User.query.count()
            logger.info(f"User table exists with {user_count} users")
        except Exception as e:
            logger.error(f"Error checking User table: {str(e)}")
        
        # Log database URI (without sensitive info)
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if 'sqlite' in db_uri:
            logger.info(f"Using SQLite database at: {db_uri}")
        else:
            # Hide sensitive parts of the URI
            logger.info(f"Using database type: {db_uri.split(':')[0]}")

if __name__ == "__main__":
    init_database()
