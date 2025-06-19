document.addEventListener('DOMContentLoaded', function() {
    // Mode selector functionality
    const modeSelector = document.getElementById('mode-selector');
    if (modeSelector) {
        const modeLinks = modeSelector.querySelectorAll('.dropdown-item');
        const currentModeSpan = document.getElementById('current-mode');
        
        modeLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const mode = this.getAttribute('data-mode');
                
                // Send request to change mode
                fetch('/api/mode', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ mode: mode }),
                })
                .then(response => response.json())
                .then(data => {
                    // Update UI
                    currentModeSpan.textContent = mode.replace('_', '-');
                    document.body.setAttribute('data-mode', mode);
                    
                    // Show toast notification
                    const toast = document.createElement('div');
                    toast.className = 'position-fixed bottom-0 end-0 p-3';
                    toast.style.zIndex = '5';
                    toast.innerHTML = `
                        <div id="liveToast" class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
                            <div class="toast-header">
                                <strong class="me-auto">Smart Reminder</strong>
                                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                            </div>
                            <div class="toast-body">
                                Mode changed to ${mode.replace('_', '-')}
                            </div>
                        </div>
                    `;
                    document.body.appendChild(toast);
                    
                    // Remove toast after 3 seconds
                    setTimeout(() => {
                        toast.remove();
                    }, 3000);
                })
                .catch(error => {
                    console.error('Error changing mode:', error);
                });
            });
        });
    }
    
    // Format dates to be more user-friendly
    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString();
    }
    
    // Helper to check if a reminder is due soon (within 24 hours)
    function isDueSoon(dateString) {
        const now = new Date();
        const dueDate = new Date(dateString);
        const diff = dueDate - now;
        const hoursDiff = diff / (1000 * 60 * 60);
        return hoursDiff > 0 && hoursDiff <= 24;
    }
    
    // Helper to check if a reminder is overdue
    function isOverdue(dateString) {
        const now = new Date();
        const dueDate = new Date(dateString);
        return dueDate < now;
    }
    
    // Export utilities for other scripts
    window.appUtils = {
        formatDate: formatDate,
        isDueSoon: isDueSoon,
        isOverdue: isOverdue
    };
});

