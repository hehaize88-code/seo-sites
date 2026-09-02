(() => {
  const send = (name, params = {}) => {
    if (typeof window.gtag === "function") window.gtag("event", name, { ...params, transport_type: "beacon" });
  };
  const placement = (node) => {
    const section = node.closest(".article,.card,.cat,.search,.actions,nav,header,footer");
    if (!section) return "page";
    if (section.matches("nav,header")) return "navigation";
    if (section.matches("footer")) return "footer";
    if (section.classList.contains("article")) return "article_card";
    if (section.classList.contains("cat")) return "category_card";
    if (section.classList.contains("search")) return "search";
    if (section.classList.contains("actions")) return "hero_action";
    return "content_card";
  };
  document.addEventListener("click", (event) => {
    const link = event.target.closest("a[href]");
    if (!link) return;
    const url = new URL(link.href, location.href);
    const linkText = (link.textContent || "").trim().replace(/\s+/g, " ").slice(0, 80);
    if (url.hostname === "cnfanshm.com") {
      const product = url.pathname.match(/^\/AllProducts\/(\d+)\.html$/i);
      const categoryPaths = ["/shoes/","/hoodies-sweaters/","/t-shirts/","/jackets/","/pants-shorts/","/headwear/","/accessories/","/jersey/","/electronics/"];
      send(product ? "main_product_click" : categoryPaths.includes(url.pathname.toLowerCase()) ? "category_click" : "main_site_click", {
        destination_url: url.href, link_text: linkText, click_placement: placement(link),
        ...(product ? { product_id: product[1] } : {})
      });
    } else if (url.hostname === location.hostname && (url.pathname.startsWith("/articles/") || url.pathname.startsWith("/guides/"))) {
      send("article_cta_click", { destination_path: url.pathname, link_text: linkText, click_placement: placement(link) });
    }
  }, true);
  document.addEventListener("submit", (event) => {
    send("search_submit", { form_id: event.target.id || "site-search", page_path: location.pathname });
  }, true);
})();
