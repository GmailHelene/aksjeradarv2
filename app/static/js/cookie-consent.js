(function() {
    // Cookie utility functions
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    function setCookie(name, value, days) {
        let expires = "";
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "") + expires + "; path=/; secure; SameSite=Lax";
    }

    function createConsentBanner() {
        const banner = document.createElement('div');
        banner.id = 'cookie-consent';
        banner.innerHTML = `
            <div class="cookie-consent-container">
                <div class="cookie-text">
                    <p>Vi bruker informasjonskapsler (cookies) for å gi deg en bedre brukeropplevelse. 
                       Ved å fortsette å bruke nettsiden aksepterer du vår bruk av cookies. 
                       <a href="/privacy#cookie-policy">Les mer om hvordan vi bruker cookies</a>.</p>
                </div>
                <div class="cookie-buttons">
                    <button id="cookie-accept-all" class="btn btn-primary">Godta alle</button>
                    <button id="cookie-accept-necessary" class="btn btn-outline-secondary">Kun nødvendige</button>
                    <button id="cookie-settings" class="btn btn-link">Innstillinger</button>
                </div>
            </div>
        `;

        const style = document.createElement('style');
        style.textContent = `
            #cookie-consent {
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                background: rgba(33, 37, 41, 0.95);
                color: white;
                padding: 1rem;
                z-index: 9999;
                box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
            }
            
            .cookie-consent-container {
                max-width: 1200px;
                margin: 0 auto;
                display: flex;
                align-items: center;
                justify-content: space-between;
                flex-wrap: wrap;
                gap: 1rem;
            }
            
            .cookie-text {
                flex: 1;
                min-width: 300px;
            }
            
            .cookie-text a {
                color: #8ab4f8;
                text-decoration: none;
            }
            
            .cookie-text a:hover {
                text-decoration: underline;
            }
            
            .cookie-buttons {
                display: flex;
                gap: 0.5rem;
                flex-wrap: wrap;
            }
            
            @media (max-width: 768px) {
                .cookie-consent-container {
                    flex-direction: column;
                    text-align: center;
                }
                
                .cookie-buttons {
                    width: 100%;
                    justify-content: center;
                }
            }
        `;

        document.head.appendChild(style);
        document.body.appendChild(banner);

        // Event listeners
        document.getElementById('cookie-accept-all').addEventListener('click', function() {
            setCookie('cookieConsent', 'all', 365);
            setCookie('analyticsConsent', 'true', 365);
            setCookie('marketingConsent', 'true', 365);
            banner.remove();
            initializeTracking();
        });

        document.getElementById('cookie-accept-necessary').addEventListener('click', function() {
            setCookie('cookieConsent', 'necessary', 365);
            setCookie('analyticsConsent', 'false', 365);
            setCookie('marketingConsent', 'false', 365);
            banner.remove();
        });

        document.getElementById('cookie-settings').addEventListener('click', function() {
            showCookieSettings();
        });
    }

    function showCookieSettings() {
        const modal = document.createElement('div');
        modal.className = 'cookie-settings-modal';
        modal.innerHTML = `
            <div class="cookie-settings-content">
                <h3>Innstillinger for cookies</h3>
                <div class="cookie-settings-section">
                    <div class="cookie-setting-item">
                        <label>
                            <input type="checkbox" id="necessary-cookies" checked disabled>
                            Nødvendige cookies
                        </label>
                        <p>Disse er påkrevd for at nettsiden skal fungere og kan ikke deaktiveres.</p>
                    </div>
                    <div class="cookie-setting-item">
                        <label>
                            <input type="checkbox" id="analytics-cookies">
                            Analysecookies
                        </label>
                        <p>Hjelper oss å forstå hvordan besøkende bruker nettsiden.</p>
                    </div>
                    <div class="cookie-setting-item">
                        <label>
                            <input type="checkbox" id="marketing-cookies">
                            Markedsføringscookies
                        </label>
                        <p>Brukes til å vise relevante annonser og måle effektiviteten av markedsføring.</p>
                    </div>
                </div>
                <div class="cookie-settings-buttons">
                    <button id="save-cookie-settings" class="btn btn-primary">Lagre innstillinger</button>
                    <button id="close-cookie-settings" class="btn btn-outline-secondary">Lukk</button>
                </div>
            </div>
        `;

        const style = document.createElement('style');
        style.textContent = `
            .cookie-settings-modal {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.5);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
            }
            
            .cookie-settings-content {
                background: white;
                padding: 2rem;
                border-radius: 8px;
                max-width: 600px;
                width: 90%;
                max-height: 90vh;
                overflow-y: auto;
            }
            
            .cookie-settings-section {
                margin: 1.5rem 0;
            }
            
            .cookie-setting-item {
                margin-bottom: 1.5rem;
            }
            
            .cookie-setting-item label {
                font-weight: bold;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            .cookie-setting-item p {
                margin: 0.5rem 0 0 1.75rem;
                color: #666;
                font-size: 0.9rem;
            }
            
            .cookie-settings-buttons {
                display: flex;
                gap: 1rem;
                justify-content: flex-end;
                margin-top: 1.5rem;
            }
        `;

        document.head.appendChild(style);
        document.body.appendChild(modal);

        const analyticsCookies = document.getElementById('analytics-cookies');
        const marketingCookies = document.getElementById('marketing-cookies');

        // Set initial state based on existing cookies
        analyticsCookies.checked = getCookie('analyticsConsent') === 'true';
        marketingCookies.checked = getCookie('marketingConsent') === 'true';

        document.getElementById('save-cookie-settings').addEventListener('click', function() {
            setCookie('cookieConsent', 'custom', 365);
            setCookie('analyticsConsent', analyticsCookies.checked, 365);
            setCookie('marketingConsent', marketingCookies.checked, 365);
            modal.remove();
            document.getElementById('cookie-consent')?.remove();
            if (analyticsCookies.checked) {
                initializeTracking();
            }
        });

        document.getElementById('close-cookie-settings').addEventListener('click', function() {
            modal.remove();
        });
    }

    function initializeTracking() {
        // Initialize Google Analytics or other tracking tools here
        if (window.gtag && getCookie('analyticsConsent') === 'true') {
            gtag('consent', 'update', {
                'analytics_storage': 'granted'
            });
        }
    }

    // Show banner if consent is not already given
    if (!getCookie('cookieConsent')) {
        createConsentBanner();
    } else if (getCookie('analyticsConsent') === 'true') {
        initializeTracking();
    }
})();
