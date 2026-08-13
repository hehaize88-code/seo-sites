const STYLE = `<style>
.lang-switch{height:40px;border:1px solid #1e5269;border-radius:999px;background:#061827;color:#eaffff;font-weight:850;padding:0 11px;outline:0;min-width:108px;color-scheme:dark}.lang-switch option{background:#fff!important;color:#061226!important}.mobile-lang-wrap{position:fixed;right:12px;bottom:12px;z-index:39;display:none}.mobile-lang-wrap .lang-switch{box-shadow:0 12px 30px rgba(0,0,0,.28);background:#08283b}.goog-te-banner-frame.skiptranslate{display:none!important}body{top:0!important}@media(max-width:760px){nav#nav .lang-switch{display:none}.mobile-lang-wrap{display:block}.mobile-lang-wrap .lang-switch{width:112px;height:36px;font-size:12px}}
</style>`;

const SELECT = `<select class="lang-switch" aria-label="Translate page" onchange="setPageLang(this.value)"><option value="">Translate</option><option value="en">EN</option><option value="zh-CN">中文</option><option value="de">DE</option><option value="fr">FR</option><option value="es">ES</option><option value="it">IT</option><option value="pl">PL</option><option value="nl">NL</option><option value="pt">PT</option></select>`;

const PAGE_END = `<div class="trust-links"><a href="/about">About</a><a href="/editorial-policy">Editorial policy</a><a href="/privacy">Privacy</a><a href="/terms">Terms</a><a href="/sitemap.xml">Sitemap</a></div><div class="mobile-lang-wrap">${SELECT}</div><div id="google_translate_element" hidden></div><script>function googleTranslateElementInit(){new google.translate.TranslateElement({pageLanguage:'en',includedLanguages:'en,zh-CN,de,fr,es,it,pl,nl,pt',autoDisplay:false},'google_translate_element')}function setPageLang(v){if(!v)return;document.cookie='googtrans=/en/'+v+';path=/;SameSite=Lax';document.cookie='googtrans=/en/'+v+';domain=.'+location.hostname+';path=/;SameSite=Lax';location.reload()}</script><script defer src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>`;

const LEGACY_REDIRECTS = new Map([
  ['/hoobuy-net-w2c-qc-shipping-workflow-2026', '/hoobuy-order-status-purchase-dispatch-qc-storage-2026'],
  ['/hoobuy-net-shipping-cost-parcel-route-2026', '/shipping-guide'],
  ['/hoobuy-qc-request-sheet-w2c-shipping-decision-2026-07-16', '/hoobuy-order-status-purchase-dispatch-qc-storage-2026#qc-and-storage']
]);

function permanentRedirect(url) {
  return new Response(null, {status: 301, headers: {Location: url.toString(), 'Cache-Control': 'public, max-age=86400'}});
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    let redirect = false;

    if (url.hostname.toLowerCase() === 'www.hoobuys.net') {
      url.hostname = 'hoobuys.net';
      redirect = true;
    }
    if (url.pathname === '/index.html') {
      url.pathname = '/';
      redirect = true;
    } else if (url.pathname.toLowerCase().endsWith('.html')) {
      url.pathname = url.pathname.slice(0, -5);
      redirect = true;
    }
    if (url.pathname.length > 1 && url.pathname.endsWith('/')) {
      url.pathname = url.pathname.replace(/\/+$/, '');
      redirect = true;
    }
    const legacyTarget = LEGACY_REDIRECTS.get(url.pathname);
    if (legacyTarget) {
      const target = new URL(legacyTarget, url.origin);
      target.search = url.search;
      return permanentRedirect(target);
    }
    if (redirect) return permanentRedirect(url);

    const canCache = request.method === 'GET' && !url.search;
    const cache = caches.default;
    const cacheKey = new Request(url.toString(), {method: 'GET'});
    if (canCache) {
      const cached = await cache.match(cacheKey);
      if (cached) return cached;
    }

    const response = await env.ASSETS.fetch(request);
    const contentType = response.headers.get('content-type') || '';
    if (!contentType.includes('text/html')) return response;

    let selectAdded = false;
    const transformed = new HTMLRewriter()
      .on('head', {element(element) { element.append(STYLE, {html: true}); }})
      .on('nav#nav', {element(element) { if (!selectAdded) { element.append(SELECT, {html: true}); selectAdded = true; } }})
      .on('body', {element(element) { element.append(PAGE_END, {html: true}); }})
      .transform(response);

    const headers = new Headers(transformed.headers);
    headers.set('X-Content-Type-Options', 'nosniff');
    headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');
    headers.set('X-Frame-Options', 'SAMEORIGIN');
    if (transformed.status === 404) headers.set('Cache-Control', 'no-store');
    else headers.set('Cache-Control', 'public, max-age=300, s-maxage=86400, stale-while-revalidate=604800');

    const finalResponse = new Response(transformed.body, {status: transformed.status, statusText: transformed.statusText, headers});
    if (canCache && finalResponse.ok) {
      ctx.waitUntil(
        cache.put(cacheKey, finalResponse.clone()).catch((error) => {
          console.error(JSON.stringify({
            event: 'cache_put_failed',
            path: url.pathname,
            message: error instanceof Error ? error.message : String(error)
          }));
        })
      );
    }
    return finalResponse;
  }
};
