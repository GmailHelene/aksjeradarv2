import os
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("init_db_direct")

# Set development environment
os.environ['FLASK_ENV'] = 'development'

def init_db():
    """Initialize the database directly"""
    logger.info("Starting direct database initialization")
    
    # Create app and register SQLAlchemy properly
    from app import create_app
    app = create_app()
    
    # Use app context for database operations
    with app.app_context():
        from app.extensions import db
        
        # Create all tables
        try:
            db.create_all()
            logger.info("Successfully created all database tables")
            
            # Check number of users
            from app.models.user import User
            users_count = User.query.count()
            logger.info(f"Current user count: {users_count}")
            
            return True
        except Exception as e:
            logger.error(f"Error creating database tables: {str(e)}")
            return False

if __name__ == "__main__":
    success = init_db()
    sys.exit(0 if success else 1)
