const CANONICAL_HOST = 'cssbuys.pro';

function canonicalPath(pathname) {
  if (pathname === '/index.html') return '/';
  if (pathname === '/guides' || pathname === '/guides.html' || pathname === '/guides/index.html') return '/guides/';
  if (/\/(de|fr|es)\/index\.html$/.test(pathname)) return pathname.replace(/index\.html$/, '');
  if (pathname.endsWith('.html')) return pathname.slice(0, -5);
  return pathname;
}

const ANALYTICS_SCRIPT = `<script>
document.addEventListener('click',function(event){
  if(!event.target.closest)return;
  var link=event.target.closest('a[href]');
  if(!link)return;
  try{
    var target=new URL(link.href,location.href);
    if((target.hostname==='www.cssbuy.com'||target.hostname==='m.cssbuy.com')&&typeof gtag==='function'){
      gtag('event','cssbuy_outbound_click',{
        link_url:target.href,
        link_text:(link.textContent||'').trim().slice(0,100),
        page_location:location.href,
        transport_type:'beacon'
      });
    }
  }catch(_error){}
});
</script>`;

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const finalPath = canonicalPath(url.pathname);

    if (url.protocol !== 'https:' || url.hostname !== CANONICAL_HOST || finalPath !== url.pathname) {
      url.protocol = 'https:';
      url.hostname = CANONICAL_HOST;
      url.port = '';
      url.pathname = finalPath;
      return Response.redirect(url.toString(), 301);
    }

    if (url.pathname.startsWith('/categories/')) {
      return Response.redirect('https://www.cssbuy.com/', 301);
    }

    if (request.method === 'GET') {
      const cached = await caches.default.match(request);
      if (cached) return cached;
    }

    const response = await env.ASSETS.fetch(request);
    const headers = new Headers(response.headers);
    headers.set('x-content-type-options', 'nosniff');
    headers.set('referrer-policy', 'strict-origin-when-cross-origin');
    headers.set('cache-control', 'public, max-age=300, s-maxage=86400, stale-while-revalidate=604800');
    if (url.pathname === '/sitemap.xml') headers.set('content-type', 'application/xml; charset=UTF-8');
    if (url.pathname === '/robots.txt' || url.pathname === '/sitemap.txt') headers.set('content-type', 'text/plain; charset=UTF-8');

    let finalResponse = new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers
    });

    if (headers.get('content-type')?.includes('text/html')) {
      finalResponse.headers.delete('content-length');
      finalResponse = new HTMLRewriter()
        .on('body', {
          element(element) {
            element.append(ANALYTICS_SCRIPT, { html: true });
          }
        })
        .transform(finalResponse);
    }

    if (request.method === 'GET' && finalResponse.status === 200) {
      ctx.waitUntil(caches.default.put(request, finalResponse.clone()));
    }

    return finalResponse;
  }
};
