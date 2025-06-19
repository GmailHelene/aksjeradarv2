#!/bin/bash
# prepare_deploy.sh - Script to prepare Aksjeradar for deployment

echo "Preparing Aksjeradar for deployment..."

# Update static asset versions
echo "Updating static asset versions..."
python update_static_versions.py

# Create version timestamp
echo "Creating version timestamp..."
python create_version.py

# Check if database exists, if not initialize it
if [ ! -f "app/aksjeradar.db" ]; then
    echo "Database not found, initializing..."
    python init_db_direct.py
fi

# Verify privacy policy files
echo "Verifying privacy policy files..."
if [ -f "app/templates/privacy.html" ] && [ -f "app/static/privacy_policy.html" ]; then
    echo "Privacy policy files found."
else
    echo "WARNING: Privacy policy files are missing! Required for app stores."
fi

# Test the application
echo "Testing the application..."
echo "Run: FLASK_APP=run.py FLASK_DEBUG=1 python -m flask run"

echo "Deployment preparation complete."
echo "Push your changes to your repository for Railway to deploy automatically."
echo "git add ."
echo "git commit -m \"your commit message\""
echo "git push"

echo "After deployment, remember to clear your browser cache if changes aren't visible."
