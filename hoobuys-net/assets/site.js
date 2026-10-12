// Analytics report language and content paths, without transmitting search input.
(() => {
  const send = (name, extra = {}) => {
    if (typeof window.gtag === 'function') {
      window.gtag('event', name, {
        page_path: location.pathname,
        page_language: document.documentElement.lang,
        ...extra,
      });
    }
  };
  document.addEventListener('click', (event) => {
    const a = event.target.closest && event.target.closest('a[href]');
    if (!a) return;
    const url = new URL(a.href, location.href);
    if (url.hostname === 'cnfanssp.com' || url.hostname === 'cnfanshp.com') {
      send('outbound_product_click', {link_url: url.origin + url.pathname});
    }
    if (a.closest('[data-language-links]')) send('language_change', {selected_language: a.hreflang});
    if (a.hasAttribute('download')) send('worksheet_download');
  });
  document.addEventListener('submit', (event) => {
    const form = event.target;
    if (!form.matches('form.search')) return;
    const input = form.querySelector('[name="keywords"]');
    if (input) {
      input.value = input.value.trim();
      if (!input.value) { event.preventDefault(); input.focus(); return; }
    }
    send('product_search_submit');
  });
  const article = document.querySelector('#main-article');
  if (!article) return;
  let sent = false;
  const check = () => {
    const rect = article.getBoundingClientRect();
    if (!sent && scrollY > 0 && innerHeight >= rect.top + rect.height * 0.5) {
      sent = true;
      send('article_scroll_50');
      removeEventListener('scroll', check);
    }
  };
  addEventListener('scroll', check, {passive: true});
})();
