from datetime import datetime
import os

# Create timestamp file
def create_timestamp():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create the file in the static folder
    timestamp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/version.txt')
    
    with open(timestamp_path, 'w') as f:
        f.write(f"Aksjeradar version timestamp: {timestamp}")
    
    print(f"Created version timestamp: {timestamp}")
    return timestamp

if __name__ == "__main__":
    create_timestamp()
