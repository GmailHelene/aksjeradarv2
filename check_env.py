#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv

def check_env_variables():
    """Check if all required environment variables are set"""
    load_dotenv()  # Load .env file if it exists
    
    required_vars = {
        'STRIPE_SECRET_KEY': 'Your Stripe Secret Key (starts with sk_live_)',
        'STRIPE_PUBLISHABLE_KEY': 'Your Stripe Publishable Key (starts with pk_live_)',
        'STRIPE_WEBHOOK_SECRET': 'Your Stripe Webhook Secret (starts with whsec_)',
        'STRIPE_MONTHLY_PRICE_ID': 'Your Stripe Monthly Price ID (starts with price_)',
        'STRIPE_YEARLY_PRICE_ID': 'Your Stripe Yearly Price ID (starts with price_)',
        'STRIPE_LIFETIME_PRICE_ID': 'Your Stripe Lifetime Price ID (starts with price_)',
        'SECRET_KEY': 'A secure random string for Flask sessions',
        'DATABASE_URL': 'Your database connection URL'
    }
    
    missing_vars = []
    insecure_vars = []
    
    print("\nChecking environment variables for Aksjeradar...\n")
    
    for var, description in required_vars.items():
        value = os.environ.get(var)
        if not value:
            missing_vars.append(f"❌ {var}: {description}")
            continue
            
        # Check for specific patterns
        if var == 'STRIPE_SECRET_KEY' and not value.startswith('sk_'):
            insecure_vars.append(f"⚠️ {var}: Does not start with 'sk_'")
        elif var == 'STRIPE_PUBLISHABLE_KEY' and not value.startswith('pk_'):
            insecure_vars.append(f"⚠️ {var}: Does not start with 'pk_'")
        elif var == 'STRIPE_WEBHOOK_SECRET' and not value.startswith('whsec_'):
            insecure_vars.append(f"⚠️ {var}: Does not start with 'whsec_'")
        elif var == 'STRIPE_MONTHLY_PRICE_ID' and not value.startswith('price_'):
            insecure_vars.append(f"⚠️ {var}: Does not start with 'price_'")
        elif var == 'STRIPE_YEARLY_PRICE_ID' and not value.startswith('price_'):
            insecure_vars.append(f"⚠️ {var}: Does not start with 'price_'")
        elif var == 'STRIPE_LIFETIME_PRICE_ID' and not value.startswith('price_'):
            insecure_vars.append(f"⚠️ {var}: Does not start with 'price_'")
        elif var == 'SECRET_KEY' and len(value) < 32:
            insecure_vars.append(f"⚠️ {var}: Value might not be secure (too short)")
        else:
            print(f"✅ {var}: Set correctly")
    
    if missing_vars:
        print("\n🚨 Missing Required Variables:")
        for var in missing_vars:
            print(var)
    
    if insecure_vars:
        print("\n⚠️ Security Warnings:")
        for var in insecure_vars:
            print(var)
    
    if not missing_vars and not insecure_vars:
        print("\n✅ All environment variables are set correctly!")
        return True
    
    if missing_vars:
        print("\n❌ Some required environment variables are missing!")
        return False
    
    print("\n⚠️ All variables are set but some security warnings exist.")
    return True

if __name__ == "__main__":
    sys.exit(0 if check_env_variables() else 1)
