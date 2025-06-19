import os
import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('init_db_direct')

def init_database_direct():
    """Initialize the database directly using SQLAlchemy instead of Flask-Migrate"""
    try:
        # Add the current directory to Python path
        current_dir = os.getcwd()
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Get database URI from environment or use default
        database_uri = os.environ.get('DATABASE_URL') or 'sqlite:///app/aksjeradar.db'
        logger.info(f"Using database URI: {database_uri}")
        
        # Create engine and connect to database
        engine = create_engine(database_uri)
        
        # Import all models to ensure they are registered
        from app.models.user import User
        from app.models.portfolio import Portfolio, PortfolioStock, StockTip
        from app.models.stock import Watchlist, WatchlistStock
        
        # Import SQLAlchemy database instance
        from app.extensions import db
        
        # Create all tables
        Base = db.Model.metadata
        Base.create_all(bind=engine)
        
        logger.info("Database tables created successfully!")
        return True
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        return False

if __name__ == "__main__":
    success = init_database_direct()
    if success:
        print("Database initialized successfully!")
    else:
        print("Database initialization failed! See logs for details.")
        sys.exit(1)
