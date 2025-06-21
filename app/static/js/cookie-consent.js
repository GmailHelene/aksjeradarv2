// Cookie Consent Management
document.addEventListener('DOMContentLoaded', function() {
    const cookieConsentBanner = document.getElementById('cookieConsentBanner');
    const acceptCookiesBtn = document.getElementById('acceptCookies');
    const essentialCookiesBtn = document.getElementById('essentialCookies');
    
    // Check if user has already consented
    if (!localStorage.getItem('cookieConsent')) {
        // Show cookie consent banner after a slight delay
        setTimeout(() => {
            cookieConsentBanner.style.display = 'block';
        }, 1000);
    }
    
    // Handle accept all cookies button
    if (acceptCookiesBtn) {
        acceptCookiesBtn.addEventListener('click', function() {
            localStorage.setItem('cookieConsent', 'all');
            cookieConsentBanner.style.display = 'none';
            enableAllCookies();
        });
    }
    
    // Handle essential only cookies button
    if (essentialCookiesBtn) {
        essentialCookiesBtn.addEventListener('click', function() {
            localStorage.setItem('cookieConsent', 'essential');
            cookieConsentBanner.style.display = 'none';
            disableNonEssentialCookies();
        });
    }
    
    // Apply cookie settings based on saved preference
    applyCookiePreferences();
});

// Function to enable all cookies
function enableAllCookies() {
    // This would typically initialize analytics, advertising cookies, etc.
    console.log('All cookies enabled');
    
    // Initialize analytics (example)
    if (typeof initializeAnalytics === 'function') {
        initializeAnalytics();
    }
}

// Function to disable non-essential cookies
function disableNonEssentialCookies() {
    // This would disable analytics, advertising cookies, etc.
    console.log('Only essential cookies enabled');
}

// Apply cookie preferences from localStorage
function applyCookiePreferences() {
    const preference = localStorage.getItem('cookieConsent');
    
    if (preference === 'all') {
        enableAllCookies();
    } else if (preference === 'essential') {
        disableNonEssentialCookies();
    }
}
