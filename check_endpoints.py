#!/usr/bin/env python3
"""
Dette scriptet sjekker at alle viktige endepunkter i appen er tilgjengelige
og returnerer riktige responser.
"""

import requests
import sys
from urllib.parse import urljoin
import logging

# Sett opp logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://aksjeradar.trade"  # For produksjon
# BASE_URL = "http://localhost:5000"  # For lokal testing

def check_endpoint(path, expected_status=200):
    """Sjekk om et endepunkt returnerer forventet status"""
    url = urljoin(BASE_URL, path)
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == expected_status:
            logger.info(f"✅ {path}: OK (status {response.status_code})")
            return True
        else:
            logger.error(f"❌ {path}: Feil status {response.status_code}, forventet {expected_status}")
            return False
    except Exception as e:
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
        url = urljoin(BASE_URL, endpoint)
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # Sjekk at responsen inneholder data
                if len(response.text) > 1000:  # Enkel sjekk for å se om vi får meningsfylt innhold
                    logger.info(f"✅ {endpoint}: OK (inneholder data)")
                else:
                    logger.warning(f"⚠️ {endpoint}: Respons ser tom ut")
                    failures.append(endpoint)
            else:
                logger.error(f"❌ {endpoint}: Feil status {response.status_code}")
                failures.append(endpoint)
        except Exception as e:
            logger.error(f"❌ {endpoint}: Error - {str(e)}")
            failures.append(endpoint)
    
    return failures

def main():
    """Hovedfunksjon for å sjekke alle endepunkter"""
    endpoints = [
        # Hovedsider
        ("/", 200),  # Hovedside
        ("/login", 200),  # Logg inn
        ("/register", 200),  # Registrer
        ("/privacy", 200),  # Personvern
        ("/contact", 200),  # Kontakt
        ("/subscription", 200),  # Abonnement
        
        # Aksjer og markeder
        ("/stocks", 200),  # Aksjeoversikt
        ("/stocks/list/oslo", 200),  # Oslo Børs
        ("/stocks/list/global", 200),  # Globale markeder
        ("/stocks/list/crypto", 200),  # Kryptovaluta
        ("/stocks/list/currency", 200),  # Valutakurser
        ("/stocks/details/EQNR.OL", 200),  # Eksempel aksjedetaljer
        ("/stocks/details/AAPL", 200),  # Eksempel global aksje
        ("/stocks/search", 200),  # Søk
        ("/stocks/compare", 200),  # Sammenlign aksjer
        
        # Analyse og portefølje
        ("/analysis", 200),  # Analyse hovedside
        ("/analysis/ai", 200),  # AI-analyse
        ("/analysis/technical/EQNR.OL", 200),  # Teknisk analyse
        ("/portfolio", 200),  # Portefølje hovedside
        ("/portfolio/overview", 200),  # Porteføljeoversikt
        ("/portfolio/transactions", 200),  # Transaksjoner
        ("/portfolio/tips", 200),  # Porteføljetips
        
        # Statiske filer og PWA
        ("/static/manifest.json", 200),  # PWA manifest
        ("/static/service-worker.js", 200),  # Service worker
        ("/static/css/style.css", 200),  # Hovedstilark
        
        # Feilsider
        ("/nonexistent", 404),  # Skal gi 404
    ]

    logger.info("\n=== Sjekker alle endepunkter ===\n")
    
    failures = []
    for path, expected_status in endpoints:
        if not check_endpoint(path, expected_status):
            failures.append(path)
    
    logger.info("\n=== Sjekker data-endepunkter ===\n")
    data_failures = check_data_endpoints()
    failures.extend(data_failures)
    
    logger.info("\n=== Oppsummering av endepunktsjekk ===")
    if failures:
        logger.error(f"\n❌ {len(failures)} endepunkter feilet:")
        for path in failures:
            logger.error(f"  - {path}")
        sys.exit(1)
    else:
        logger.info("\n✅ Alle endepunkter fungerer som forventet!")
        sys.exit(0)

if __name__ == "__main__":
    main()
