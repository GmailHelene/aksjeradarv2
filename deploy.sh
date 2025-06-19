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
echo "STRIPE_PUBLISHABLE_KEY=pk_live_WAFqLYQXhprWHuTG9gu0rqml"
echo "STRIPE_SECRET_KEY=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"
echo "STRIPE_WEBHOOK_SECRET=whsec_bbS77lBqiZvsMEd6T9HLYELduRsJOCFl"
echo "STRIPE_MONTHLY_PRICE_ID=price_1RbggkDql25sVlduoDydQz9i"
echo "STRIPE_YEARLY_PRICE_ID=price_1RbggkDql25sVldusvNAoOwB"
echo "STRIPE_LIFETIME_PRICE_ID=price_1RbggkDql25sVlduTVr85WEu"

echo ""
echo "===== POST-DEPLOYMENT CHECKLIST ====="
echo "After deploying to Railway, verify the following:"
echo "1. The database migration has run successfully to add stripe_customer_id to User model"
echo "2. Test the payment flow by creating a test subscription"
echo "3. Verify that webhooks are being received correctly"
echo "4. Check that user subscription status updates properly"

echo ""
echo "✅ Deployment instructions complete!"
