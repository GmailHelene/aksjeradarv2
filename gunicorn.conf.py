import os
import multiprocessing

# Server socket
bind = "0.0.0.0:" + os.environ.get("PORT", "8080")

# Worker processes - optimized for Railway
workers = 2  # Reduced for Railway's memory limits
worker_class = 'sync'
worker_connections = 1000
timeout = 30  # Reduced timeout for better resource management
keepalive = 5  # Increased keepalive for better connection reuse
max_requests = 1000  # Restart workers after this many requests
max_requests_jitter = 50  # Add randomness to max_requests

# Logging
errorlog = '-'
loglevel = 'info'  # Changed from debug to info for production
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Server mechanics
daemon = False
preload_app = True
reload = False  # Disabled reload for production

# Process naming
proc_name = 'aksjeradar'

# Performance tuning
max_requests = 1000
max_requests_jitter = 50
graceful_timeout = 30
limit_request_line = 4094
limit_request_fields = 100

# SSL configuration for proxy support
forwarded_allow_ips = '*'  # Trust X-Forwarded-* headers from all IPs
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on'
}

# Server hooks
def on_starting(server):
    import sys
    import os
    # Ensure the app directory is in the Python path
    app_dir = os.getcwd()
    if app_dir not in sys.path:
        sys.path.insert(0, app_dir)
    server.log.info("Starting Aksjeradar application")
    
    # Log important paths and configurations
    server.log.info(f"Current directory: {app_dir}")
    server.log.info(f"Python path: {sys.path}")
    server.log.info(f"Number of workers: {workers}")
    server.log.info(f"Using worker class: {worker_class}")
    
    # Verify database configuration
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        server.log.info("Database URL is configured")
    else:
        server.log.error("No DATABASE_URL found in environment!")
        
    # Check if migrations directory exists
    migrations_dir = os.path.join(app_dir, 'migrations')
    if os.path.exists(migrations_dir):
        server.log.info(f"Migrations directory found at: {migrations_dir}")
        env_py = os.path.join(migrations_dir, 'env.py')
        if os.path.exists(env_py):
            server.log.info(f"env.py found at: {env_py}")
        else:
            server.log.error(f"env.py NOT found at: {env_py}")
    else:
        server.log.error(f"Migrations directory NOT found at: {migrations_dir}")

def post_fork(server, worker):
    """Log after a worker has been forked"""
    server.log.info(f"Worker {worker.pid} forked")
