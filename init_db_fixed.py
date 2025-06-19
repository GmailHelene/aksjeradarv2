import os
import sys
from flask_migrate import Migrate, init, migrate, upgrade
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('init_db')

def init_database(app, db):
    """Initialize the database with proper path handling"""
    try:
        # Add the current directory to Python path
        current_dir = os.getcwd()
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Ensure the migrations directory exists with the correct structure
        migrations_dir = os.path.join(current_dir, 'migrations')
        if not os.path.exists(migrations_dir):
            os.makedirs(migrations_dir, exist_ok=True)
            logger.info(f"Created migrations directory at {migrations_dir}")
        
        logger.info(f"Current working directory: {current_dir}")
        logger.info(f"Python path: {sys.path}")
        
        # Check if migrations directory exists
        migrations_dir = os.path.join(current_dir, 'migrations')
        if os.path.exists(migrations_dir):
            logger.info(f"Migrations directory found at: {migrations_dir}")
            env_py = os.path.join(migrations_dir, 'env.py')
            if os.path.exists(env_py):
                logger.info(f"env.py found at: {env_py}")
            else:
                logger.error(f"env.py NOT found at: {env_py}")
        else:
            logger.error(f"Migrations directory NOT found at: {migrations_dir}")
        
        with app.app_context():
            # Create database tables
            db.create_all()
            logger.info("Database tables created")
            
            # Setup Flask-Migrate
            migrations_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'migrations')
            migrate_instance = Migrate(app, db, directory=migrations_dir)
            
            # Try to run migrations
            try:
                logger.info("Attempting to run migrations...")
                upgrade()
                logger.info("Migrations applied successfully")
            except Exception as e:
                logger.error(f"Error running migrations: {e}")
                logger.info("Attempting to initialize migrations")
                try:
                    # If no migrations exist, create them
                    init(directory=migrations_dir)
                    migrate(directory=migrations_dir)
                    upgrade(directory=migrations_dir)
                    logger.info("Migrations initialized and applied successfully")
                except Exception as e:
                    logger.error(f"Error initializing migrations: {e}")
                    # Continue without migrations - just use db.create_all()
                    logger.info("Continuing with basic database creation")
        
        logger.info("Database initialization completed")
        return True
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        return False

if __name__ == "__main__":
    # Import the app and db here to avoid circular imports
    from run import app
    from app.extensions import db
    
    success = init_database(app, db)
    if success:
        print("Database initialized successfully!")
    else:
        print("Database initialization failed! See logs for details.")
        sys.exit(1)
