from run import app
from app.extensions import db
from flask_migrate import Migrate, init, migrate, upgrade

# Initialize database
with app.app_context():
    db.create_all()
    
    # Setup Flask-Migrate
    migrate_instance = Migrate(app, db)
    
    # Try to run migrations
    try:
        upgrade()
    except:
        # If no migrations exist, create them
        init()
        migrate()
        upgrade()
    
    print("Database initialized successfully!")
