(() => {
  const menuButton = document.querySelector(".menu-button");
  const navigation = document.querySelector("#mainNav");

  if (menuButton && navigation) {
    menuButton.addEventListener("click", () => {
      const isOpen = navigation.classList.toggle("open");
      menuButton.setAttribute("aria-expanded", String(isOpen));
    });

    navigation.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        navigation.classList.remove("open");
        menuButton.setAttribute("aria-expanded", "false");
      });
    });
  }

  const productSearch = document.querySelector(".product-search");
  if (productSearch) {
    productSearch.addEventListener("submit", (event) => {
      const input = productSearch.querySelector('[name="keywords"]');
      input.value = input.value.trim();
      if (!input.value) {
        event.preventDefault();
        input.focus();
      }
    });
  }

  document.addEventListener("click", (event) => {
    const link = event.target.closest('a[href*="cnfanshp.com"]');
    if (!link || typeof window.gtag !== "function") return;
    window.gtag("event", "outbound_click_cnfanshp", {
      link_url: link.href,
      link_text: (link.textContent || "").trim(),
      transport_type: "beacon",
    });
  });
})();
