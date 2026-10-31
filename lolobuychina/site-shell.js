(() => {
  const language = document.documentElement.lang;
  const send = (name, values = {}) => {
    if (typeof window.gtag === 'function') window.gtag('event', name, {page_language: language, ...values, transport_type: 'beacon'});
  };
  const placement = node => node.closest('header') ? 'navigation' : node.closest('footer') ? 'footer' : node.closest('.product-card') ? 'product_card' : node.closest('.article-card') ? 'article_card' : 'content';
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    if (!link) return;
    const url = new URL(link.href, location.href);
    const values = {destination_url: url.href, link_text: link.textContent.trim().slice(0, 100), click_placement: placement(link)};
    if (url.hostname === 'cnfanshm.com') {
      const product = url.pathname.match(/^\/AllProducts\/(\d+)\.html$/i);
      const categories = ['/shoes/','/hoodies-sweaters/','/t-shirts/','/jackets/','/pants-shorts/','/headwear/','/accessories/','/jersey/','/electronics/'];
      send(product ? 'main_product_click' : categories.includes(url.pathname.toLowerCase()) ? 'category_click' : 'main_site_click', {...values, ...(product ? {product_id: product[1], source_id: link.dataset.productId || ''} : {})});
    } else if (url.origin === location.origin && /\/(articles|guides)\//.test(url.pathname)) {
      send('article_cta_click', {...values, destination_path: url.pathname});
    }
    if (link.closest('.language')) send('language_switch', {destination_language: link.hreflang, destination_path: url.pathname});
  }, true);
  document.querySelectorAll('[data-product-search]').forEach(form => form.addEventListener('submit', event => {
    event.preventDefault();
    const query = new FormData(form).get('keywords').trim();
    if (!query) return;
    const target = window.LBC.resolve(query);
    send('search_submit', {form_id: 'product-search', page_path: location.pathname});
    send('main_site_click', {destination_url: target, click_placement: 'search'});
    location.assign(target);
  }));
})();
