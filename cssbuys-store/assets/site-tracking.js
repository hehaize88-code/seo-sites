(function () {
  'use strict';
  if (window.__cssbuysTrackingReady) return;
  window.__cssbuysTrackingReady = true;
  function track(name, values) {
    if (typeof window.gtag !== 'function') return false;
    window.gtag('event', name, Object.assign({
      source_page: window.location.pathname,
      page_language: document.documentElement.lang || 'en',
      transport_type: 'beacon'
    }, values));
    return true;
  }
  function outbound(event) {
    if (event.type === 'auxclick' && event.button !== 1) return;
    var element = event.target instanceof Element ? event.target : event.target.parentElement;
    var link = element && element.closest('a[href]');
    if (!link) return;
    var url;
    try { url = new URL(link.href, window.location.href); } catch (error) { return; }
    if (url.hostname !== 'cnfanssp.com' && url.hostname !== 'www.cnfanssp.com') return;
    track('open_main_site', {
      link_url: url.href,
      link_domain: url.hostname,
      link_text: (link.textContent || link.getAttribute('aria-label') || '').trim().slice(0, 100),
      click_location: link.dataset.location || 'article_link',
      product_id: link.dataset.productId || ''
    });
  }
  document.addEventListener('click', outbound);
  document.addEventListener('auxclick', outbound);
  window.addEventListener('pageshow', function () {
    document.querySelectorAll('[data-main-search]').forEach(function (form) {
      delete form.dataset.submitting;
    });
  });
  document.addEventListener('submit', function (event) {
    var form = event.target;
    if (!(form instanceof HTMLFormElement) || !form.matches('[data-main-search]')) return;
    var input = form.elements.namedItem('keywords');
    var term = input ? input.value.trim().slice(0, 120) : '';
    if (!term) { event.preventDefault(); if (input) input.focus(); return; }
    input.value = term;
    if (form.dataset.submitting === 'true') { event.preventDefault(); return; }
    track('search', {search_term: term});
    if (typeof window.gtag !== 'function') return;
    event.preventDefault();
    form.dataset.submitting = 'true';
    var submitted = false;
    function proceed() {
      if (submitted) return;
      submitted = true;
      HTMLFormElement.prototype.submit.call(form);
    }
    track('open_main_site', {
      link_url: form.action,
      link_domain: 'www.cnfanssp.com',
      click_location: 'homepage_search',
      event_callback: proceed,
      event_timeout: 250
    });
    window.setTimeout(proceed, 300);
  });
}());
