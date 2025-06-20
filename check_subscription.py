import requests
import sys
import os
from urllib.parse import urljoin
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = 'https://aksjeradar.trade'

def check_subscription_endpoints():
    """Test subscription-related endpoints"""
    endpoints = [
        ('/subscription', 'GET', 'Subscription page'),
        ('/create-checkout-session', 'POST', 'Create Stripe checkout session'),
        ('/payment/success', 'GET', 'Payment success page'),
        ('/webhook', 'POST', 'Stripe webhook endpoint')
    ]

    all_ok = True
    for endpoint, method, description in endpoints:
        url = urljoin(BASE_URL, endpoint)
        try:
            if method == 'GET':
                response = requests.get(url, timeout=10)
            else:  # POST
                response = requests.post(url, timeout=10)
            
            status = response.status_code
            if status in [200, 302]:  # 302 is ok for redirects
                logger.info(f"✅ {description} ({url}) - OK ({status})")
            else:
                logger.error(f"❌ {description} ({url}) - Error ({status})")
                all_ok = False
        except requests.RequestException as e:
            logger.error(f"❌ {description} ({url}) - Failed to connect: {str(e)}")
            all_ok = False

    return all_ok

if __name__ == "__main__":
    logger.info("Testing subscription endpoints...")
    success = check_subscription_endpoints()
    if success:
        logger.info("All subscription endpoints are working! ✅")
        sys.exit(0)
    else:
        logger.error("Some subscription endpoints failed! ❌")
        sys.exit(1)
