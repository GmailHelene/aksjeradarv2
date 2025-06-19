import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    """Set up logging configuration for the Flask application"""
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Set up file handler
    file_handler = RotatingFileHandler(
        'logs/aksjeradar.log',
        maxBytes=1024 * 1024,  # 1 MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    
    # Set up stream handler for console output
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s'
    ))
    stream_handler.setLevel(logging.INFO)
    
    # Add handlers to app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    
    # Initial log message
    app.logger.info('Aksjeradar startup')
