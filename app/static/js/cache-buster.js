/* cache-buster.js - Add to main.js to help clear browser cache */

document.addEventListener('DOMContentLoaded', function() {
    // Check if the site version is different from the stored version
    fetch('/static/version.txt?' + Date.now())
        .then(response => response.text())
        .then(version => {
            const storedVersion = localStorage.getItem('aksjeradarVersion');
            
            if (storedVersion !== version) {
                console.log('New version detected, clearing cache...');
                
                // Clear caches if possible
                if ('caches' in window) {
                    caches.keys().then(cacheNames => {
                        return Promise.all(
                            cacheNames.map(cacheName => {
                                if (cacheName.startsWith('aksjeradar-cache')) {
                                    return caches.delete(cacheName);
                                }
                            })
                        );
                    }).then(() => {
                        console.log('Caches cleared successfully');
                    });
                }
                
                // Update stored version
                localStorage.setItem('aksjeradarVersion', version);
                
                // Show a message to the user
                const refreshMsg = document.createElement('div');
                refreshMsg.style.position = 'fixed';
                refreshMsg.style.top = '10px';
                refreshMsg.style.left = '50%';
                refreshMsg.style.transform = 'translateX(-50%)';
                refreshMsg.style.backgroundColor = '#343a40';
                refreshMsg.style.color = 'white';
                refreshMsg.style.padding = '10px 20px';
                refreshMsg.style.borderRadius = '5px';
                refreshMsg.style.zIndex = '9999';
                refreshMsg.textContent = 'Ny versjon av Aksjeradar er lastet. Trykk her for å oppdatere.';
                refreshMsg.style.cursor = 'pointer';
                
                refreshMsg.addEventListener('click', function() {
                    window.location.reload(true);
                });
                
                document.body.appendChild(refreshMsg);
                
                // Remove the message after 10 seconds if not clicked
                setTimeout(() => {
                    if (document.body.contains(refreshMsg)) {
                        document.body.removeChild(refreshMsg);
                    }
                }, 10000);
            }
        })
        .catch(err => console.log('Failed to check version:', err));
});
