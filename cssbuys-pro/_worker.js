const CANONICAL_HOST = 'cssbuys.pro';

function canonicalPath(pathname) {
  if (pathname === '/index.html') return '/';
  if (pathname === '/guides' || pathname === '/guides.html' || pathname === '/guides/index.html') return '/guides/';
  if (/\/(de|fr|es)\/index\.html$/.test(pathname)) return pathname.replace(/index\.html$/, '');
  if (pathname.endsWith('.html')) return pathname.slice(0, -5);
  return pathname;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const finalPath = canonicalPath(url.pathname);

    if (url.protocol !== 'https:' || url.hostname !== CANONICAL_HOST || finalPath !== url.pathname) {
      url.protocol = 'https:';
      url.hostname = CANONICAL_HOST;
      url.port = '';
      url.pathname = finalPath;
      return Response.redirect(url.toString(), 301);
    }

    const response = await env.ASSETS.fetch(request);
    const headers = new Headers(response.headers);
    headers.set('x-content-type-options', 'nosniff');
    headers.set('referrer-policy', 'strict-origin-when-cross-origin');
    if (url.pathname === '/sitemap.xml') headers.set('content-type', 'application/xml; charset=UTF-8');
    if (url.pathname === '/robots.txt' || url.pathname === '/sitemap.txt') headers.set('content-type', 'text/plain; charset=UTF-8');

    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers
    });
  }
};
