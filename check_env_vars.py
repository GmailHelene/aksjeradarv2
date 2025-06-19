import os

# Required environment variables
required_vars = [
    'STRIPE_SECRET_KEY',
    'STRIPE_PUBLISHABLE_KEY', 
    'STRIPE_WEBHOOK_SECRET',
    'STRIPE_MONTHLY_PRICE_ID',
    'STRIPE_YEARLY_PRICE_ID',
    'STRIPE_LIFETIME_PRICE_ID',
    'SECRET_KEY',
    'DATABASE_URL'
]

# Optional but recommended
optional_vars = [
    'FLASK_ENV',
    'FLASK_DEBUG',
    'OPENAI_API_KEY',
    'NEWS_API_KEY',
    'EMAIL_SERVER',
    'EMAIL_PORT',
    'EMAIL_USERNAME',
    'EMAIL_PASSWORD'
]

def check_env_vars():
    """Check for required environment variables"""
    print("\n=== Environment Variable Check ===\n")
    
    # Track missing required variables
    missing_required = []
    
    # Check required variables
    print("Required Variables:")
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            # Mask sensitive values
            if 'KEY' in var or 'SECRET' in var:
                masked_value = value[:4] + '****' + value[-4:] if len(value) > 8 else '****'
                print(f"✅ {var}: {masked_value}")
            else:
                print(f"✅ {var}: Set")
        else:
            print(f"❌ {var}: MISSING")
            missing_required.append(var)
    
    # Check optional variables
    print("\nOptional Variables:")
    for var in optional_vars:
        value = os.environ.get(var)
        if value:
            if 'KEY' in var or 'SECRET' in var or 'PASSWORD' in var:
                print(f"✅ {var}: Set (value masked)")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"⚠️ {var}: Not set")
    
    # Summary
    print("\n=== Summary ===")
    if missing_required:
        print(f"❌ Missing {len(missing_required)} required variables: {', '.join(missing_required)}")
        print("These must be set for the application to function properly in production.")
    else:
        print("✅ All required environment variables are set!")
    
    print("\nDone checking environment variables.")

if __name__ == "__main__":
    check_env_vars()
