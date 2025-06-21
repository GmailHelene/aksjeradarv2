// Service Worker for Aksjeradar PWA
const CACHE_NAME = 'aksjeradar-cache-v1';
const OFFLINE_URL = '/offline';

// Resources to cache on install
const PRECACHE_RESOURCES = [
  '/',
  '/static/css/style.css',
  '/static/css/table-fixes.css',
  '/static/js/main.js',
  '/static/manifest.json',
  OFFLINE_URL,
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png'
];

// On Service Worker Install
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Caching app shell and static assets');
        return cache.addAll(PRECACHE_RESOURCES);
      })
      .catch(error => {
        console.error('Pre-caching failed:', error);
      })
  );
  // Force the waiting service worker to become the active service worker
  self.skipWaiting();
});

// On Service Worker Activate
self.addEventListener('activate', event => {
  event.waitUntil(
    Promise.all([
      // Clean up old caches
      caches.keys().then(cacheNames => {
        return Promise.all(
          cacheNames.filter(cacheName => {
            return cacheName !== CACHE_NAME;
          }).map(cacheName => {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          })
        );
      }),
      // Claims control for all clients in scope
      self.clients.claim()
    ])
  );
});

// On fetch - implement network-first strategy with offline fallback
self.addEventListener('fetch', event => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') return;
  
  // Skip cross-origin requests
  if (!event.request.url.startsWith(self.location.origin)) return;
  
  // Handle API requests differently (network-first)
  if (event.request.url.includes('/api/')) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          // Clone the response before using it
          const responseToCache = response.clone();
          
          // Cache the successful response
          caches.open(CACHE_NAME)
            .then(cache => {
              cache.put(event.request, responseToCache);
            });
            
          return response;
        })
        .catch(() => {
          // If network fails, try to return cached response
          return caches.match(event.request);
        })
    );
    return;
  }
  
  // For other requests, try cache first, then network
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          // Return cached response
          return response;
        }
        
        // If not in cache, fetch from network
        return fetch(event.request)
          .then(response => {
            // Clone the response before using it
            const responseToCache = response.clone();
            
            // Cache the successful response
            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });
              
            return response;
          })
          .catch(error => {
            // If both cache and network fail, show offline page
            console.error('Fetch failed:', error);
            return caches.match(OFFLINE_URL);
          });
      })
  );
});

// Handle push notifications
self.addEventListener('push', event => {
  const data = event.data.json();
  const options = {
    body: data.body,
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/icon-96x96.png',
    vibrate: [100, 50, 100],
    data: {
      url: data.url
    }
  };
  
  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

// Handle notification click
self.addEventListener('notificationclick', event => {
  event.notification.close();
  
  event.waitUntil(
    clients.openWindow(event.notification.data.url || '/')
  );
});
