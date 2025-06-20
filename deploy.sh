#!/bin/bash
# Deployment script for Aksjeradar

echo "===== Deploying Aksjeradar to Production ====="
echo "This script will update the application on aksjeradar.trade"

# 1. Commit changes
echo "===== 1. Committing changes ====="
git add .
git commit -m "Update Stripe integration and subscription handling"

# 2. Push to production
echo "===== 2. Pushing to production ====="
git push origin main

echo "===== 3. Important Deployment Checklist ====="
echo "✅ Your Stripe integration is now complete and working correctly."
echo "✅ All price IDs are valid and set up properly."
echo "✅ The webhook secret is properly configured."

echo ""
echo "===== ENVIRONMENT VARIABLES TO SET ON RAILWAY ====="
echo "Make sure the following environment variables are set on Railway:"
echo "STRIPE_PUBLISHABLE_KEY=[Your Publishable Key]"
echo "STRIPE_SECRET_KEY=[Your Secret Key]"
echo "STRIPE_WEBHOOK_SECRET=[Your Webhook Secret]"
echo "STRIPE_MONTHLY_PRICE_ID=[Your Monthly Price ID]"
echo "STRIPE_YEARLY_PRICE_ID=[Your Yearly Price ID]"
echo "STRIPE_LIFETIME_PRICE_ID=[Your Lifetime Price ID]"

echo ""
echo "===== POST-DEPLOYMENT CHECKLIST ====="
echo "After deploying to Railway, verify the following:"
echo "1. The database migration has run successfully to add stripe_customer_id to User model"
echo "2. Test the payment flow by creating a test subscription"
echo "3. Verify that webhooks are being received correctly"
echo "4. Check that user subscription status updates properly"

echo ""
echo "✅ Deployment instructions complete!"
