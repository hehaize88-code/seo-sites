(() => {
  const translations = new Map([
    ["打开完整文章 →", "Read the full guide →"],
    ["新增 FAQ", "New FAQ"],
    ["Hipobuy DE 买家为什么要记录商品属性？", "Why should HipoBuy DE buyers record product attributes?"],
    ["鞋盒、厚外套、电子配件或易碎物品会影响线路选择，提前记录能减少发货前误判。", "Shoe boxes, thick jackets, electronic accessories, and fragile items can affect route eligibility. Recording them early reduces mistakes before parcel submission."],
    ["Hipobuy DE 的 QC 图片和海关说明有什么关系？", "How do HipoBuy DE QC photos relate to customs information?"],
    ["QC 图片帮助确认实际商品和包装，海关与申报信息仍应以平台结算和线路提示为准。", "QC photos help confirm the actual item and packaging. Customs and declaration information should still be checked against the current checkout and route notices."]
  ]);

  function replaceText(root) {
    if (!root) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    for (const node of nodes) {
      const raw = node.nodeValue || "";
      const trimmed = raw.trim();
      if (!translations.has(trimmed)) continue;
      node.nodeValue = raw.replace(trimmed, translations.get(trimmed));
    }
  }

  function applyEnglishFix() {
    document.querySelectorAll(".daily-seo-update").forEach(replaceText);
    const pageLang = (document.documentElement.lang || "en").toLowerCase();
    if (pageLang === "en" || pageLang.startsWith("en-")) {
      document.querySelectorAll("option").forEach((option) => {
        if (option.textContent.trim() === "中文") option.textContent = "Chinese";
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
      applyEnglishFix();
      setTimeout(applyEnglishFix, 100);
    });
  } else {
    applyEnglishFix();
    setTimeout(applyEnglishFix, 100);
  }
})();
