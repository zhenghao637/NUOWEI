const OFFLINE_SCRIPT = String.raw`
'use strict';
const CACHE = 'norway-uk-manual';
const HOME = '/index.html';
self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const response = await fetch(HOME, {cache: 'reload'});
    if (!response.ok) throw new Error('Unable to cache the travel manual');
    const cache = await caches.open(CACHE);
    await cache.put(HOME, response);
    await self.skipWaiting();
  })());
});
self.addEventListener('activate', event => {
  event.waitUntil(self.clients.claim());
});
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (event.request.method !== 'GET' || url.origin !== self.location.origin || event.request.mode !== 'navigate') return;
  if (url.pathname !== '/' && url.pathname !== '/index.html') return;
  const network = (async () => {
    const response = await fetch(event.request, {cache: 'no-cache'});
    if (!response.ok) throw new Error('Manual is temporarily unavailable');
    const cache = await caches.open(CACHE);
    await cache.put(HOME, response.clone());
    return response;
  })();
  event.waitUntil(network.then(() => {}, () => {}));
  event.respondWith((async () => {
    const cached = await (await caches.open(CACHE)).match(HOME);
    if (!cached) return network;
    return Promise.race([
      network.catch(() => cached),
      new Promise(resolve => setTimeout(() => resolve(cached), 3500))
    ]);
  })());
});
`;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/sw.js') {
      return new Response(OFFLINE_SCRIPT, {
        headers: {
          'Content-Type': 'text/javascript; charset=utf-8',
          'Cache-Control': 'no-cache',
          'Service-Worker-Allowed': '/',
          'X-Content-Type-Options': 'nosniff'
        }
      });
    }
    const asset = await env.ASSETS.fetch(request);
    const response = new Response(asset.body, asset);
    response.headers.set('Cache-Control', 'no-cache');
    response.headers.set('X-Content-Type-Options', 'nosniff');
    response.headers.set('Referrer-Policy', 'no-referrer');
    response.headers.set('X-Robots-Tag', 'noindex, nofollow');
    response.headers.set('Content-Security-Policy', "default-src 'self' data: blob:; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'");
    return response;
  }
};
