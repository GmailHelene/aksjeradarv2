#!/usr/bin/env python3
"""
Dette scriptet sjekker at alle viktige endepunkter i appen er tilgjengelige
og returnerer riktige responser når den kjøres lokalt.
"""

import requests
import logging
import sys
from urllib.parse import urljoin

# Sett opp logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# For lokal testing
BASE_URL = "http://localhost:5001"

def check_endpoint(path, expected_status=200):
    """Sjekk om et endepunkt returnerer forventet status"""
    url = urljoin(BASE_URL, path)
    try:
        response = requests.get(url, timeout=10)
        status = response.status_code
        if status == expected_status:
            logger.info(f"✅ {path}: OK ({status})")
            return True
        else:
            logger.error(f"❌ {path}: Feil (Status {status})")
            return False
    except requests.RequestException as e:
        logger.error(f"❌ {path}: Error - {str(e)}")
        return False

def check_data_endpoints():
    """Sjekk spesifikt endepunkter som leverer data"""
    data_endpoints = [
        "/stocks/list/oslo",  # Oslo Børs
        "/stocks/list/global",  # Globale markeder
        "/stocks/list/crypto",  # Kryptovaluta
        "/stocks/list/currency",  # Valutakurser
    ]
    
    failures = []
    for endpoint in data_endpoints:
        if not check_endpoint(endpoint):
            failures.append(endpoint)
    
    return failures

def main():
    """Hovedfunksjon for å sjekke alle endepunkter"""
    # Sjekk først grunnleggende endepunkter
    basic_endpoints = [
        "/",
        "/version",
        "/manifest.json"
    ]
    
    basic_failures = []
    for endpoint in basic_endpoints:
        if not check_endpoint(endpoint):
            basic_failures.append(endpoint)
    
    # Sjekk deretter data-endepunkter
    data_failures = check_data_endpoints()
    
    # Til slutt, sjekk funksjonsendepunkter
    feature_endpoints = [
        "/portfolio/overview",
        "/portfolio/transactions",
        "/analysis/technical/EQNR.OL"
    ]
    
    feature_failures = []
    for endpoint in feature_endpoints:
        if not check_endpoint(endpoint):
            feature_failures.append(endpoint)
    
    # Skriv ut oppsummering
    if not (basic_failures or data_failures or feature_failures):
        logger.info("\n✅ Alle endepunkter fungerer!")
        return 0
    else:
        if basic_failures:
            logger.error("\n❌ Feilet grunnleggende endepunkter:")
            for ep in basic_failures:
                logger.error(f"  {ep}")
        
        if data_failures:
            logger.error("\n❌ Feilet data-endepunkter:")
            for ep in data_failures:
                logger.error(f"  {ep}")
        
        if feature_failures:
            logger.error("\n❌ Feilet funksjonsendepunkter:")
            for ep in feature_failures:
                logger.error(f"  {ep}")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
