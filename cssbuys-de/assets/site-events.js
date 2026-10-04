(() => {
  'use strict';
  if (window.__cssbuysEvents) return;
  window.__cssbuysEvents = true;
  const language = document.documentElement.lang || 'en';
  const report = (name, extra) => {
    if (typeof window.gtag !== 'function') return;
    window.gtag('event', name, {
      page_path: location.pathname,
      content_language: language,
      transport_type: 'beacon',
      ...extra
    });
  };
  document.addEventListener('click', (event) => {
    const anchor = event.target.closest && event.target.closest('a[href]');
    if (!anchor) return;
    const destination = new URL(anchor.href, location.href);
    if (destination.hostname !== 'cnfanshp.com') return;
    const match = destination.pathname.match(/^\/AllProducts\/(\d+)\.html$/);
    report(match ? 'product_outbound_click' : 'catalog_outbound_click', {
      link_domain: destination.hostname,
      destination_path: destination.pathname,
      ...(match ? { product_id: match[1] } : {})
    });
  });
  document.addEventListener('submit', (event) => {
    const form = event.target;
    if (!(form instanceof HTMLFormElement)) return;
    const destination = new URL(form.action, location.href);
    if (destination.hostname === 'cnfanshp.com' && destination.pathname === '/search.html') {
      report('catalog_search', { link_domain: destination.hostname, destination_path: destination.pathname });
    }
  });
})();
