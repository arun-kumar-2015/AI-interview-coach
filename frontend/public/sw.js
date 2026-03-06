// Enhanced Service Worker for AI Coach
const CACHE_NAME = 'ai-coach-v2'; // Incremented version
const urlsToCache = [
    '/',
    '/manifest.json',
    '/icons/icon-192.png',
    '/icons/icon-512.png'
];

// Install event: cache initial assets
self.addEventListener('install', (event) => {
    self.skipWaiting(); // Force the waiting service worker to become active
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(urlsToCache))
    );
});

// Activate event: clean up old caches and claim clients
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (cache !== CACHE_NAME) {
                        console.log('SW: Clearing Old Cache', cache);
                        return caches.delete(cache);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch event: Network-First strategy for HTML and manifest, Cache-First for others
self.addEventListener('fetch', (event) => {
    const isHtml = event.request.mode === 'navigate' ||
        (event.request.method === 'GET' && event.request.headers.get('accept').includes('text/html'));

    const isManifest = event.request.url.includes('manifest.json');

    if (isHtml || isManifest) {
        // Network-First: Always try network first, fallback to cache
        event.respondWith(
            fetch(event.request)
                .then((response) => {
                    const copy = response.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
                    return response;
                })
                .catch(() => caches.match(event.request))
        );
    } else {
        // Cache-First: Standard for images and assets
        event.respondWith(
            caches.match(event.request)
                .then((response) => response || fetch(event.request))
        );
    }
});
