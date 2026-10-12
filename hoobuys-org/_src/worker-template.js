const PAGES = __PAGES__;
const LANGS = ['zh-CN', 'de', 'fr', 'es', 'it', 'pl', 'nl', 'pt'];
const REVISION = '2026-10-12-org-multilingual';
function route(path) {
  const parts = path.split('/').filter(Boolean);
  const lang = LANGS.includes(parts[0]) ? parts.shift() : '';
  const slug = parts.join('/') || 'index';
  return { lang, slug, valid: PAGES.includes(slug) };
}
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (!['GET', 'HEAD'].includes(request.method)) return new Response('Method not allowed', { status: 405, headers: { Allow: 'GET, HEAD' } });
    const original = url.pathname;
    let path = original.replace(/\.html$/, '').replace(/\/index$/, '/');
    if (path === '/index') path = '/';
    if (/^\/(zh-CN|de|fr|es|it|pl|nl|pt)$/.test(path)) path += '/';
    const home = path === '/' || /^\/(zh-CN|de|fr|es|it|pl|nl|pt)\/$/.test(path);
    if (!home) path = path.replace(/\/$/, '');
    const info = route(path);
    const asset = /^\/assets\/[a-zA-Z0-9_.-]+$/.test(path) || ['/robots.txt', '/sitemap.xml', '/sitemap.txt'].includes(path);
    if (url.hostname === 'www.hoobuys.org' || (info.valid && path !== original)) {
      url.hostname = url.hostname === 'www.hoobuys.org' ? 'hoobuys.org' : url.hostname;
      url.pathname = info.valid ? path : original;
      return Response.redirect(url.toString(), 301);
    }
    if (!info.valid && !asset) {
      const missing = new URL(request.url); missing.pathname = (info.lang ? '/' + info.lang : '') + '/404'; missing.search = '';
      const page = await env.ASSETS.fetch(new Request(missing, request));
      return new Response(request.method === 'HEAD' ? null : page.body, { status: 404, headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store', 'X-Robots-Tag': 'noindex', 'X-Site-Revision': REVISION } });
    }
    const response = await env.ASSETS.fetch(request);
    const headers = new Headers(response.headers);
    headers.set('X-Site-Revision', REVISION);
    headers.set('X-Content-Type-Options', 'nosniff');
    if ((headers.get('content-type') || '').includes('text/html')) headers.set('Cache-Control', 'public, max-age=0, s-maxage=300');
    else if (/\.[a-f0-9]{12}\.(css|js)$/.test(path)) headers.set('Cache-Control', 'public, max-age=31536000, immutable');
    return new Response(request.method === 'HEAD' ? null : response.body, { status: response.status, headers });
  }
};
