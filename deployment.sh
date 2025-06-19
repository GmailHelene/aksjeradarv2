                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    #!/bin/bash
# deployment.sh - Script for preparing and deploying Aksjeradar to aksjeradar.trade

echo "===== Aksjeradar Deployment Script ====="
echo "This script will help prepare your application for deployment to aksjeradar.trade"
echo

# Check if we're in the right directory
if [ ! -f "config.py" ] || [ ! -d "app" ]; then
    echo "❌ Error: This script must be run from the root of the Aksjeradar project"
    exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Check if Railway CLI is installed
if ! command_exists railway; then
    echo "❌ Railway CLI not found. You'll need to deploy manually."
    echo "To install Railway CLI, run: npm i -g @railway/cli"
    echo "Or deploy through the Railway dashboard: https://railway.app"
fi

# Prepare database and static files
echo
echo "===== Preparing application ====="
echo "1. Creating version timestamp"
python create_version.py

echo "2. Updating static asset versions"
python update_static_versions.py

echo "3. Checking environment variables"
python check_env_vars.py

# Create a checklist of things to verify
echo
echo "===== Pre-deployment Checklist ====="
echo "Before deploying to aksjeradar.trade, please verify the following:"
echo
echo "1. Database:"
echo "   - [ ] All migrations have been created and tested"
echo "   - [ ] Database is properly backed up"
echo
echo "2. Stripe Integration:"
echo "   - [ ] Stripe webhook endpoint is configured on the Stripe dashboard"
echo "   - [ ] Stripe products and prices have been created"
echo "   - [ ] All required Stripe environment variables are set on Railway"
echo
echo "3. Security:"
echo "   - [ ] No API keys or secrets are hardcoded in the config"
echo "   - [ ] SECRET_KEY is set to a strong random value in production"
echo
echo "4. Routes and Templates:"
echo "   - [ ] Registration page includes email field"
echo "   - [ ] Subscription route is properly configured"
echo "   - [ ] Privacy policy has correct contact information"
echo
echo "5. PWA Features:"
echo "   - [ ] Service worker is properly configured"
echo "   - [ ] Manifest.json has correct information"
echo "   - [ ] Offline page is set up"
echo
echo "===== Deployment Instructions ====="
echo "To deploy to aksjeradar.trade, you can:"
echo
echo "1. Use Railway CLI (if installed):"
echo "   railway up"
echo
echo "2. Push to your GitHub repository connected to Railway:"
echo "   git add ."
echo "   git commit -m \"Deployment updates\""
echo "   git push origin main"
echo
echo "3. Deploy manually through Railway dashboard:"
echo "   https://railway.app"
echo
echo "After deployment, verify the following URLs work correctly:"
echo "- https://aksjeradar.trade/register (Registration)"
echo "- https://aksjeradar.trade/subscription (Subscription page)"
echo "- https://aksjeradar.trade/login (Login page)"
echo
echo "===== Deployment Complete ====="
echo "Thank you for using the Aksjeradar deployment script!"
