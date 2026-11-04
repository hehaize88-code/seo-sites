const CANONICAL_HOST = 'cssbuys.pro';
const CACHE_VERSION = '20261104-buyer-guides-six-languages-v5';
const STORE_CATEGORIES = {
  "other-stuff": "https://cnfanshp.com/other-stuff/",
  "electronics": "https://cnfanshp.com/electronics/",
  "jersey": "https://cnfanshp.com/Jersey/",
  "accessories": "https://cnfanshp.com/accessories/",
  "headwear": "https://cnfanshp.com/headwear/",
  "pants-shorts": "https://cnfanshp.com/pants-shorts/",
  "jackets": "https://cnfanshp.com/jackets/",
  "t-shirts": "https://cnfanshp.com/t-shirts/",
  "hoodies-sweaters": "https://cnfanshp.com/hoodies-sweaters/",
  "shoes": "https://cnfanshp.com/shoes/",
  "short-sets": "https://cnfanshp.com/short-sets/"
};

function canonicalPath(pathname) {
  if (pathname.endsWith('/index.html')) return pathname.slice(0, -10);
  if (pathname === '/guides' || pathname === '/guides.html') return '/guides/';
  if (/^\/(de|fr|es|it|zh)$/.test(pathname)) return pathname + '/';
  if (/^\/(de|fr|es|it|zh)\/guides(?:\.html)?$/.test(pathname)) return pathname.replace(/\.html$/, '') + '/';
  if (pathname.endsWith('.html')) return pathname.slice(0, -5);
  return pathname;
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const finalPath = canonicalPath(url.pathname);

    if (url.protocol !== 'https:' || url.hostname !== CANONICAL_HOST || finalPath !== url.pathname) {
      url.protocol = 'https:';
      url.hostname = CANONICAL_HOST;
      url.port = '';
      url.pathname = finalPath;
      return Response.redirect(url.toString(), 308);
    }

    const category = /^\/categories\/([^/]+)\/?$/.exec(url.pathname);
    if (category && Object.hasOwn(STORE_CATEGORIES, category[1])) {
      return Response.redirect(STORE_CATEGORIES[category[1]], 301);
    }

    // Scope edge entries to this release so old destinations cannot survive a deployment.
    const cacheUrl = new URL(request.url);
    cacheUrl.searchParams.set('__site_revision', CACHE_VERSION);
    const cacheKey = new Request(cacheUrl.toString(), { method: 'GET' });

    if (request.method === 'GET') {
      const cached = await caches.default.match(cacheKey);
      if (cached) return cached;
    }

    const response = await env.ASSETS.fetch(request);
    const headers = new Headers(response.headers);
    headers.set('x-content-type-options', 'nosniff');
    headers.set('referrer-policy', 'strict-origin-when-cross-origin');
    headers.set('cache-control', response.status === 200 ? 'public, max-age=300, s-maxage=86400, stale-while-revalidate=604800' : 'no-store');
    if (response.status === 200 && url.pathname === '/sitemap.xml') headers.set('content-type', 'application/xml; charset=UTF-8');
    if (response.status === 200 && (url.pathname === '/robots.txt' || url.pathname === '/sitemap.txt')) headers.set('content-type', 'text/plain; charset=UTF-8');

    const finalResponse = new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers
    });

    if (request.method === 'GET' && finalResponse.status === 200) {
      ctx.waitUntil(caches.default.put(cacheKey, finalResponse.clone()));
    }

    return finalResponse;
  }
};
