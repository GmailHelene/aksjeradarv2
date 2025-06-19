def check_db_connection(db):
    """Check if the database connection is working"""
    try:
        with db.engine.connect() as connection:
            connection.execute(db.text('SELECT 1'))
        return True
    except Exception as e:
        print(f'Database connection failed: {str(e)}')
        return False
