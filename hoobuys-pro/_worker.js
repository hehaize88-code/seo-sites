const ORIGIN = 'https://hoobuys.pro';
const LOCALES = ['de', 'es', 'fr', 'it'];
const LEGACY = 'hoobuy-pro-europe-parcel-ledger-w2c-qc-2026-07-14';
const HEADERS = {
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
  'X-Frame-Options': 'SAMEORIGIN',
  'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
  'Content-Security-Policy': "default-src 'self'; img-src 'self' https://cnfanssp.com https://www.cnfanssp.com https://*.google-analytics.com data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com; connect-src 'self' https://www.google-analytics.com https://*.google-analytics.com https://*.analytics.google.com; form-action 'self' https://cnfanssp.com; base-uri 'self'; frame-ancestors 'self'"
};
export function canonicalPath(pathname) {
  let p = pathname.replace(/\/{2,}/g, '/');
  if (p === '/en' || p.startsWith('/en/')) p = p.slice(3) || '/';
  p = p.replace(/\/index(?:\.html)?\/?$/, '/');
  p = p.replace(/\.html\/?$/, '');
  const parts = p.split('/').filter(Boolean);
  const lang = LOCALES.includes(parts[0]) ? parts.shift() : '';
  let slug = parts.join('/');
  if (slug === 'languages') slug = '';
  if (slug === LEGACY) slug = 'shipping-guide';
  return (lang ? '/' + lang + '/' : '/') + slug;
}
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/_src' || url.pathname.startsWith('/_src/')) return new Response('Not found', {status: 404, headers: HEADERS});
    // Assets with real extensions retain their path. HTML aliases normalize once.
    const isPage = !/\.[a-z0-9]+\/?$/i.test(url.pathname) || /\.html\/?$/i.test(url.pathname);
    const destination = isPage ? canonicalPath(url.pathname) : url.pathname;
    if (url.hostname === 'www.hoobuys.pro' || destination !== url.pathname || url.protocol !== 'https:') {
      url.hostname = 'hoobuys.pro'; url.protocol = 'https:'; url.pathname = destination;
      return new Response(null, {status: 301, headers: {...HEADERS, Location: url.toString(), 'Cache-Control': 'public, max-age=3600'}});
    }
    // Let Pages resolve extensionless HTML and locale index files directly.
    // Never fetch the .html alias internally: that can create a redirect cycle.
    const response = await env.ASSETS.fetch(request);
    const headers = new Headers(response.headers);
    for (const [k,v] of Object.entries(HEADERS)) headers.set(k,v);
    if (response.status === 404) {
      headers.set('X-Robots-Tag', 'noindex');
      headers.set('Cache-Control', 'public, max-age=60');
    } else if ((headers.get('Content-Type') || '').includes('text/html')) {
      headers.set('Cache-Control', 'public, max-age=0, must-revalidate');
    }
    return new Response(response.body, {status:response.status,statusText:response.statusText,headers});
  }
};
