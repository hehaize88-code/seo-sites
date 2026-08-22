const STYLE = `<style>.lang-switch{height:40px;border:1px solid #1cbfd1;border-radius:999px;background:#061c2b;color:#eaffff;font-weight:900;padding:0 12px;outline:0;min-width:112px;color-scheme:dark}.lang-switch option{background:#fff!important;color:#061226!important;font-weight:800}.mobile-lang-wrap{position:fixed;right:14px;bottom:14px;z-index:9999;display:none}.mobile-lang-wrap .lang-switch{box-shadow:0 12px 30px rgba(0,0,0,.28);background:#08283b}@media(max-width:760px){nav#nav .lang-switch{grid-column:1/-1;width:100%;margin-top:4px}.mobile-lang-wrap{display:block}.mobile-lang-wrap .lang-switch{width:118px;height:38px;font-size:12px}}.goog-te-banner-frame.skiptranslate{display:none!important}body{top:0!important}</style>`;
const SELECT = `<select class="lang-switch" aria-label="Change language" onchange="setPageLang(this.value)"><option value="">Language</option><option value="en">EN</option><option value="zh-CN">中文</option><option value="de">DE</option><option value="fr">FR</option><option value="es">ES</option><option value="it">IT</option><option value="pl">PL</option><option value="nl">NL</option><option value="pt">PT</option></select>`;
const FOOTER = `<div class="mobile-lang-wrap">${SELECT}</div><div id="google_translate_element" style="display:none"></div><script>function googleTranslateElementInit(){var l=(document.documentElement.lang||'en');new google.translate.TranslateElement({pageLanguage:l,includedLanguages:'en,zh-CN,de,fr,es,it,pl,nl,pt',autoDisplay:false},'google_translate_element')}function setPageLang(v){if(!v)return;var s=(document.documentElement.lang||'en');document.cookie='googtrans=/'+s+'/'+v+';path=/';document.cookie='googtrans=/'+s+'/'+v+';domain=.'+location.hostname+';path=/';location.reload()}</script><script src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>`;

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.hostname === 'www.hoobuys.org') {
      url.hostname = 'hoobuys.org';
      return new Response(null, {
        status: 301,
        headers: { Location: url.toString(), 'Cache-Control': 'public, max-age=3600' },
      });
    }

    const cacheable = request.method === 'GET' && !url.search;
    const cacheKey = new Request(url.toString(), request);
    if (cacheable) {
      const cached = await caches.default.match(cacheKey);
      if (cached) return cached;
    }

    const res = await env.ASSETS.fetch(request);
    const contentType = res.headers.get('content-type') || '';
    if (!contentType.includes('text/html') || res.status !== 200) return res;

    const canonicalPath = url.pathname === '/' ? '/' : url.pathname.replace(/\.html$/, '');
    const canonical = `https://hoobuys.org${canonicalPath}`;
    let added = false;
    const addLang = {
      element(element) {
        if (!added) {
          element.append(SELECT, { html: true });
          added = true;
        }
      },
    };

    const transformed = new HTMLRewriter()
      .on('link[rel="canonical"]', { element(element) { element.remove(); } })
      .on('head', { element(element) { element.append(`${STYLE}<link rel="canonical" href="${canonical}">`, { html: true }); } })
      .on('nav#nav', addLang)
      .on('body', { element(element) { element.append(FOOTER, { html: true }); } })
      .transform(res);

    const headers = new Headers(transformed.headers);
    headers.set('Cache-Control', 'public, max-age=0, s-maxage=86400, stale-while-revalidate=604800');
    const finalResponse = new Response(transformed.body, {
      status: transformed.status,
      statusText: transformed.statusText,
      headers,
    });

    if (cacheable) ctx.waitUntil(caches.default.put(cacheKey, finalResponse.clone()));
    return finalResponse;
  },
};
