#!/usr/bin/env python3
"""
Dette scriptet sjekker status på Railway-deploymentet.
"""

import requests
import sys
import time
import logging

# Sett opp logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://aksjeradar.trade"  # For produksjon

def check_deployment_status():
    """Sjekk om nettsiden er oppe og kjører etter deployment"""
    max_attempts = 10
    attempt = 0
    
    logger.info(f"Sjekker status på {BASE_URL}...")
    
    while attempt < max_attempts:
        attempt += 1
        try:
            response = requests.get(BASE_URL, timeout=10)
            if response.status_code == 200:
                logger.info(f"✅ Deployment vellykket! Serveren er oppe og kjører (status {response.status_code})")
                return True
            else:
                logger.warning(f"⚠️ Forsøk {attempt}/{max_attempts}: Serveren svarer, men med status {response.status_code}")
        except Exception as e:
            logger.warning(f"⚠️ Forsøk {attempt}/{max_attempts}: Kan ikke koble til serveren - {str(e)}")
        
        if attempt < max_attempts:
            wait_time = 30  # Sekunder mellom hver sjekk
            logger.info(f"Venter {wait_time} sekunder før neste forsøk...")
            time.sleep(wait_time)
    
    logger.error(f"❌ Deployment feilet eller er ikke ferdig etter {max_attempts} forsøk")
    return False

if __name__ == "__main__":
    sys.exit(0 if check_deployment_status() else 1)
