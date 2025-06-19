import os
import multiprocessing

# Server socket
bind = "0.0.0.0:" + os.environ.get("PORT", "8080")

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 2

# Logging
errorlog = '-'
loglevel = 'debug'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Server mechanics
daemon = False
preload_app = True
reload = True

# Process naming
proc_name = 'aksjeradar'

# Server hooks
def on_starting(server):
    server.log.info("Starting Aksjeradar application")

def post_fork(server, worker):
    server.log.info(f"Worker spawned (pid: {worker.pid})")

def pre_fork(server, worker):
    pass

def pre_exec(server):
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")

def worker_exit(server, worker):
    # Create version file on worker exit to ensure it's updated
    try:
        from create_version import create_timestamp
        timestamp = create_timestamp()
        server.log.info(f"Worker exiting, updated version timestamp: {timestamp}")
    except Exception as e:
        server.log.error(f"Error creating version timestamp: {e}")
