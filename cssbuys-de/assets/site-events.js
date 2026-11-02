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
    if (!['cnfanshp.com', 'www.cnfanshp.com'].includes(destination.hostname)) return;
    const match = destination.pathname.match(/^\/AllProducts\/(\d+)\.html$/);
    const details = {
      link_domain: destination.hostname,
      destination_path: destination.pathname,
      destination_kind: match ? 'product' : 'catalogue',
      link_placement: anchor.dataset.outboundPlacement || 'other',
      ...(match ? { product_id: match[1] } : {})
    };
    // One consistent conversion candidate covers catalogue and product exits.
    report('catalog_outbound_click', details);
    // Preserve the legacy product series for historical comparisons.
    if (match) report('product_outbound_click', details);
  });
  document.addEventListener('submit', (event) => {
    const form = event.target;
    if (!(form instanceof HTMLFormElement)) return;
    const destination = new URL(form.action, location.href);
    if (['cnfanshp.com', 'www.cnfanshp.com'].includes(destination.hostname) && destination.pathname === '/search.html') {
      report('catalog_search', { link_domain: destination.hostname, destination_path: destination.pathname });
    }
  });
})();
