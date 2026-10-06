(() => {
  if (window.hipobuysAnalyticsBound) return;
  window.hipobuysAnalyticsBound = true;
  const send = (name, values) => {
    if (typeof window.gtag === "function") window.gtag("event", name, { ...values, transport_type: "beacon" });
  };
  document.addEventListener("click", (event) => {
    const link = event.target instanceof Element ? event.target.closest("a[href]") : null;
    if (!link) return;
    const url = new URL(link.href, location.href);
    if (!["cnfanshp.com", "www.cnfanshp.com"].includes(url.hostname)) return;
    send("outbound_click_cnfanshp", { link_url: link.href, link_text: link.textContent.trim(), source_page: location.pathname });
  });
  document.addEventListener("submit", (event) => {
    const form = event.target;
    if (!(form instanceof HTMLFormElement) || !form.matches(".product-search") || event.defaultPrevented) return;
    const field = form.querySelector('[name="keywords"]');
    if (!field || !field.value.trim()) return;
    // Measure successful search submissions without copying visitor-entered text into analytics.
    send("product_search_submit", { source_page: location.pathname, destination: new URL(form.action).hostname });
  });
})();
