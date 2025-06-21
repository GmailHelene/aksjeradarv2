#!/usr/bin/env python3
import requests
import logging
import sys
from urllib.parse import urljoin

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://aksjeradar.trade"

def check_endpoint(path, expected_status=200):
    """Check if an endpoint returns expected status"""
    url = urljoin(BASE_URL, path)
    try:
        response = requests.get(url, timeout=10)
        status = response.status_code
        if status == expected_status:
            logger.info(f"✅ {path}: OK ({status})")
            return True
        else:
            logger.error(f"❌ {path}: Failed (Status {status})")
            return False
    except requests.RequestException as e:
        logger.error(f"❌ {path}: Error - {str(e)}")
        return False

def check_all_endpoints():
    """Check all important endpoints"""
    endpoints = [
        "/",
        "/stocks",
        "/stocks/list/oslo",
        "/stocks/list/global",
        "/stocks/list/crypto",
        "/stocks/list/currency",
        "/stocks/search",
        "/analysis/technical/EQNR.OL",
        "/portfolio/overview",
        "/portfolio/transactions",
        "/version",
        "/manifest.json"
    ]
    
    results = []
    for endpoint in endpoints:
        success = check_endpoint(endpoint)
        results.append((endpoint, success))
    
    # Print summary
    logger.info("\nEndpoint Check Summary:")
    logger.info("=" * 50)
    working = [ep for ep, success in results if success]
    failing = [ep for ep, success in results if not success]
    
    if working:
        logger.info(f"\n✅ Working endpoints ({len(working)}):")
        for ep in working:
            logger.info(f"  {ep}")
    
    if failing:
        logger.error(f"\n❌ Failing endpoints ({len(failing)}):")
        for ep in failing:
            logger.error(f"  {ep}")
    
    return len(failing) == 0

if __name__ == "__main__":
    sys.exit(0 if check_all_endpoints() else 1)
