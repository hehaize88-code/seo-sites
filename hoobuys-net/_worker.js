// Static editions contain their complete content, language links and metadata.
const RELEASE = 'multilingual-guides-20261012-logo-v2';
const LANGS = new Set(['zh-cn', 'de', 'fr', 'es', 'it', 'pl', 'nl', 'pt']);
const LEGACY = new Map([
  ['/hoobuy-net-w2c-qc-shipping-workflow-2026', '/hoobuy-order-status-purchase-dispatch-qc-storage-2026'],
  ['/hoobuy-net-shipping-cost-parcel-route-2026', '/shipping-guide'],
  ['/hoobuy-qc-request-sheet-w2c-shipping-decision-2026-07-16', '/hoobuy-order-status-purchase-dispatch-qc-storage-2026#qc-and-storage'],
]);

function redirect(url) {
  return new Response(null, {status: 301, headers: {Location: url.toString(), 'Cache-Control': 'public, max-age=86400'}});
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    let decoded;
    try { decoded = decodeURIComponent(url.pathname); }
    catch { return new Response('Bad request', {status: 400}); }
    // Build inputs never belong to the public document surface.
    if (decoded.split('/').includes('_src') || decoded.split('/').some(p => p.startsWith('.'))) {
      return new Response('Not found', {status: 404, headers: {'Cache-Control': 'no-store', 'X-Robots-Tag': 'noindex'}});
    }
    const original = url.toString();
    if (url.hostname.toLowerCase() === 'www.hoobuys.net') url.hostname = 'hoobuys.net';
    if (['hoobuys.net', 'www.hoobuys.net'].includes(url.hostname) && url.protocol !== 'https:') url.protocol = 'https:';
    let path = url.pathname.replace(/\/{2,}/g, '/');
    path = path.replace(/^\/zh-CN(?=\/|$)/i, '/zh-cn');
    if (path.endsWith('/index.html')) path = path.slice(0, -10);
    else if (path.toLowerCase().endsWith('.html')) path = path.slice(0, -5);
    if (path === '') path = '/';
    const bits = path.split('/').filter(Boolean);
    if (bits.length === 1 && LANGS.has(bits[0])) path = '/' + bits[0] + '/';
    else if (path.length > 1) path = path.replace(/\/+$/, '');
    url.pathname = path;
    const prefix = bits.length > 1 && LANGS.has(bits[0]) ? '/' + bits[0] : '';
    const legacyPath = prefix ? path.slice(prefix.length) : path;
    if (LEGACY.has(legacyPath)) {
      const target = new URL(prefix + LEGACY.get(legacyPath), url.origin);
      target.search = url.search;
      return redirect(target);
    }
    if (url.toString() !== original) return redirect(url);
    // Do not reuse cache entries from the previous HTML rewriter.
    let response = await env.ASSETS.fetch(request);
    if (response.status === 404 && bits.length > 0 && LANGS.has(bits[0])) {
      const localizedUrl = new URL('/' + bits[0] + '/404', url.origin);
      const localized = await env.ASSETS.fetch(new Request(localizedUrl, request));
      if (localized.ok && (localized.headers.get('content-type') || '').includes('text/html')) {
        response = new Response(localized.body, {status: 404, headers: localized.headers});
      }
    }
    const headers = new Headers(response.headers);
    headers.set('X-Content-Type-Options', 'nosniff');
    headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
    headers.set('X-Frame-Options', 'SAMEORIGIN');
    headers.set('X-Hoobuys-Release', RELEASE);
    if ((headers.get('content-type') || '').includes('text/html')) {
      if (response.ok) headers.set('Link', `<https://hoobuys.net${url.pathname}>; rel="canonical"`);
      headers.set('Cache-Control', response.status === 404 ? 'no-store' : 'public, max-age=60, s-maxage=300, stale-while-revalidate=60');
    }
    return new Response(response.body, {status: response.status, statusText: response.statusText, headers});
  },
};
