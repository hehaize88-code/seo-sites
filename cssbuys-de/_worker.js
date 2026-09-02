export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === 'www.cssbuys.de') { url.hostname = 'cssbuys.de'; return Response.redirect(url.toString(), 301); }
    if (url.pathname === '/guides' || url.pathname === '/guides.html') { url.pathname = '/guides/'; return Response.redirect(url.toString(), 301); }
    if (url.pathname.endsWith('/index.html')) { url.pathname = url.pathname.slice(0, -10); return Response.redirect(url.toString(), 301); }
    if (url.pathname.endsWith('.html') && url.pathname !== '/404.html') { url.pathname = url.pathname.slice(0, -5) || '/'; return Response.redirect(url.toString(), 301); }
    const response = await env.ASSETS.fetch(request);
    const headers = new Headers(response.headers);
    headers.set('X-Content-Type-Options', 'nosniff');
    headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
    headers.set('X-Frame-Options', 'SAMEORIGIN');
    if ((headers.get('content-type') || '').includes('text/html')) headers.set('Cache-Control', 'public, max-age=0, must-revalidate');
    return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
  }
};
