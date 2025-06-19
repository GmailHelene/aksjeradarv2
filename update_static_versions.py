from datetime import datetime
import os
import re

def add_version_to_static_files():
    """Add version timestamps to all CSS and JS files to force browser cache invalidation"""
    timestamp = int(datetime.now().timestamp())
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static')
    
    # Create the version.txt file
    with open(os.path.join(static_dir, 'version.txt'), 'w') as f:
        f.write(f"Aksjeradar version timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Build: {timestamp}")
    
    print(f"Created version file with timestamp: {timestamp}")
    
    # Update service-worker.js to include the timestamp
    service_worker_path = os.path.join(static_dir, 'service-worker.js')
    if os.path.exists(service_worker_path):
        with open(service_worker_path, 'r') as f:
            content = f.read()
        
        # Update the cache name with the timestamp
        content = re.sub(
            r"const CACHE_NAME = ['\"]aksjeradar-cache-v\d+['\"];", 
            f"const CACHE_NAME = 'aksjeradar-cache-v{timestamp}';", 
            content
        )
        
        with open(service_worker_path, 'w') as f:
            f.write(content)
        
        print(f"Updated service worker cache version to: {timestamp}")
    
    return timestamp

if __name__ == "__main__":
    add_version_to_static_files()
