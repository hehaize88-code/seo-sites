// Verified main-catalog destinations for existing product detail URLs.
const productDestinations = {
  "/products/multi-brand-running-shoes": "https://cnfanshp.com/AllProducts/4029.html",
  "/products/leather-loafers": "https://cnfanshp.com/AllProducts/1969.html",
  "/products/boss-polo": "https://cnfanshp.com/AllProducts/5555.html",
  "/products/classic-watch": "https://cnfanshp.com/AllProducts/4827.html",
  "/products/paint-splatter-jeans": "https://cnfanshp.com/AllProducts/5839.html",
  "/products/guess-jeans": "https://cnfanshp.com/AllProducts/1922.html",
  "/products/down-jacket": "https://cnfanshp.com/AllProducts/5919.html",
  "/products/varsity-jacket": "https://cnfanshp.com/AllProducts/5910.html",
  "/products/stussy-jacket": "https://cnfanshp.com/AllProducts/4586.html",
  "/products/mertra-hoodie": "https://cnfanshp.com/AllProducts/4699.html"
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === 'www.cssbuys.de') { url.hostname = 'cssbuys.de'; return Response.redirect(url.toString(), 301); }
    const productPath = url.pathname.replace(/\/$/, '').replace(/\.html$/, '');
    if (Object.hasOwn(productDestinations, productPath)) {
      return Response.redirect(productDestinations[productPath], 302);
    }
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
