(() => {
  const form = document.getElementById('weight-form');
  if (form) form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const values = Object.fromEntries(new FormData(form));
    const actual = Number(values.weight) / 1000;
    const volume = Number(values.length) * Number(values.width) * Number(values.height) / Number(values.divisor);
    if (![actual, volume].every(Number.isFinite)) return;
    const formatter = new Intl.NumberFormat(document.documentElement.lang, { maximumFractionDigits: 2 });
    const results = { actual, volume, greater: Math.max(actual, volume) };
    for (const [key, value] of Object.entries(results)) document.querySelector('[data-result="' + key + '"]').textContent = formatter.format(value);
    document.querySelector('.calc-result').hidden = false;
    if (typeof gtag === 'function') gtag('event', 'shipping_calculator_use', { page_language: document.documentElement.lang, page_path: location.pathname });
  });
  document.addEventListener('click', (event) => {
    const link = event.target.closest('a[href]');
    if (!link || typeof gtag !== 'function') return;
    const url = new URL(link.href, location.href);
    const data = { page_language: document.documentElement.lang, page_path: location.pathname };
    if (url.hostname === 'cnfanssp.com' || url.hostname === 'www.cnfanssp.com') {
      gtag('event', 'product_index_click', { ...data, link_url: url.origin + url.pathname });
    } else if (link.closest('.language-picker')) {
      gtag('event', 'language_switch', { ...data, target_language: link.hreflang });
    } else if (url.origin === location.origin && /\/hoobuy-|\/shipping-guide$/.test(url.pathname)) {
      gtag('event', 'guide_click', { ...data, link_url: url.pathname });
    }
  });
})();
