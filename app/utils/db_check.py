from sqlalchemy import text
from flask import current_app

def check_db_connection(db):
    """Check if the database connection is working"""
    try:
        # Try to execute a simple query
        with db.engine.connect() as connection:
            connection.execute(text('SELECT 1'))
        current_app.logger.info('Database connection successful')
        return True
    except Exception as e:
        current_app.logger.error(f'Database connection failed: {str(e)}')
        return False
