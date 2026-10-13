(() => {
  'use strict';
  const language = document.documentElement.lang || 'en';
  const emit = (name, extra = {}) => {
    if (typeof window.gtag === 'function') {
      window.gtag('event', name, {page_path: location.pathname, content_language: language, ...extra});
    }
  };
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    if (!link) return;
    let url;
    try { url = new URL(link.href, location.href); } catch { return; }
    if (url.hostname === 'cnfanssp.com') {
      emit('product_index_click', {link_url: url.origin + url.pathname});
    } else if (link.matches('[data-tracker-download]')) {
      emit('tracker_download', {link_url: url.pathname});
    } else if (link.closest('.language-menu')) {
      emit('language_switch', {target_language: link.hreflang});
    } else if (url.origin === location.origin && /\/(?:hoobuy[^/]*|shipping-guide)$/.test(url.pathname)) {
      emit('guide_click', {link_url: url.pathname});
    }
  });
  document.querySelectorAll('[data-product-search]').forEach(form => {
    form.addEventListener('submit', event => {
      const input = form.querySelector('[name="keywords"]');
      input.value = input.value.trim();
      if (!input.value) { event.preventDefault(); input.focus(); return; }
      // Deliberately omit the entered keyword or pasted product URL from analytics.
      emit('product_search');
    });
  });
  const calculator = document.querySelector('[data-weight-calculator]');
  if (calculator) calculator.addEventListener('submit', event => {
    event.preventDefault();
    const names = ['weight', 'length', 'width', 'height', 'divisor'];
    const values = names.map(name => Number(calculator.elements.namedItem(name).value));
    const output = calculator.querySelector('output');
    if (values.some(value => !Number.isFinite(value) || value <= 0)) {
      output.textContent = calculator.dataset.error;
      return;
    }
    const [weight, length, width, height, divisor] = values;
    const volume = length * width * height / divisor;
    if (!Number.isFinite(volume)) { output.textContent = calculator.dataset.error; return; }
    const format = new Intl.NumberFormat(language, {maximumFractionDigits: 3});
    output.textContent = `${calculator.dataset.volume}: ${format.format(volume)} kg\n${calculator.dataset.billed}: ${format.format(Math.max(weight, volume))} kg`;
    emit('shipping_weight_calculation');
  });
  document.addEventListener('click', event => {
    document.querySelectorAll('.language-menu[open]').forEach(menu => {
      if (!menu.contains(event.target)) menu.open = false;
    });
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') document.querySelectorAll('.language-menu[open]').forEach(menu => {
      menu.open = false;
      menu.querySelector('summary').focus();
    });
  });
})();
