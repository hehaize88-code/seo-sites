const routes = new Set(__ROUTES__);
const aliases = __REDIRECTS__;
const languages = __LANGS__;
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    let pathname = url.pathname.replace(/\/{2,}/g, '/');
    if (pathname.endsWith('/index.html')) pathname = pathname.slice(0, -10);
    else if (pathname.endsWith('.html')) pathname = pathname.slice(0, -5);
    const prefix = pathname.split('/')[1];
    const locale = languages.includes(prefix) ? prefix : 'en';
    const base = locale !== 'en' ? '/' + locale : '';
    const inputBase = languages.includes(prefix) ? '/' + prefix : '';
    let rest = pathname.slice(inputBase.length) || '/';
    if (rest === '/index') rest = '/';
    if (rest === '/articles') rest = '/articles/';
    if (aliases[rest.replace(/\/$/, '')]) rest = aliases[rest.replace(/\/$/, '')];
    if (rest !== '/' && rest !== '/articles/' && rest.endsWith('/')) rest = rest.slice(0, -1);
    pathname = base + rest;
    if (url.hostname === 'www.lolobuychina.com' || url.protocol !== 'https:' || url.pathname !== pathname) {
      url.hostname = url.hostname === 'www.lolobuychina.com' ? 'lolobuychina.com' : url.hostname;
      url.protocol = 'https:';url.pathname = pathname;
      return Response.redirect(url.toString(), 301);
    }
    const isStatic = /\.(?:js|css|svg|png|jpe?g|webp|ico|txt|xml|woff2?)$/i.test(pathname);
    let response;
    if (!routes.has(pathname) && !isStatic) {
      const notFound = new URL(base + '/404.html', url);
      const asset = await env.ASSETS.fetch(new Request(notFound, {method:'GET'}));
      response = new Response(request.method === 'HEAD' ? null : asset.body, {status:404,headers:{'Content-Type':'text/html; charset=utf-8','X-Robots-Tag':'noindex'}});
    } else response = await env.ASSETS.fetch(request);
    const headers = new Headers(response.headers);
    if ((headers.get('content-type') || '').includes('text/html')) {
      headers.set('Cache-Control','no-cache, max-age=0, must-revalidate');
      headers.set('Cloudflare-CDN-Cache-Control','no-store');
      if (response.status === 200) headers.set('Content-Language', locale);
    }
    headers.set('X-Content-Type-Options','nosniff');
    return new Response(response.body,{status:response.status,statusText:response.statusText,headers});
  }
};
