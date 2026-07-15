const PRIMARY_ORIGIN = "https://hoobuys.net";

const LEGACY_ROUTES = {
  "/hoobuy-pro-w2c-qc-shipping-workflow-2026": "/hoobuy-net-w2c-qc-shipping-workflow-2026",
  "/hoobuy-pro-qc-photo-video-checklist-2026": "/hoobuy-net-w2c-qc-shipping-workflow-2026",
  "/hoobuy-pro-europe-parcel-ledger-w2c-qc-2026-07-14": "/hoobuy-net-shipping-cost-parcel-route-2026",
  "/hoobuy-shop-w2c-qc-shipping-workflow-2026": "/hoobuy-net-w2c-qc-shipping-workflow-2026",
  "/hoobuy-shop-coupon-qc-before-shipping-2026": "/hoobuy-net-w2c-qc-shipping-workflow-2026",
  "/hoobuy-group-haul-w2c-qc-cost-ledger-2026-07-15": "/hoobuy-net-shipping-cost-parcel-route-2026",
  "/hoobuy-org-w2c-qc-shipping-workflow-2026": "/hoobuy-net-w2c-qc-shipping-workflow-2026",
  "/hoobuy-org-w2c-spreadsheet-method-2026": "/hoobuy-spreadsheet-guide",
  "/sitemap.txt": "/sitemap.xml"
};

function normalizePath(pathname) {
  let path = pathname.replace(/\/{2,}/g, "/");
  if (path === "/en" || path === "/en/") {
    path = "/";
  } else if (path.toLowerCase().startsWith("/en/")) {
    path = path.slice(3) || "/";
  }
  if (/\/index\.html$/i.test(path)) {
    path = path.slice(0, -"index.html".length);
  } else if (/\.html$/i.test(path)) {
    path = path.slice(0, -".html".length);
  }
  const language = path.split("/")[1]?.toLowerCase();
  if (["de", "fr", "es", "pl"].includes(language) && path.replace(/\/+$/, "") === `/${language}`) {
    return `/${language}/`;
  }
  if (path.length > 1) path = path.replace(/\/+$/, "");
  return path || "/";
}

export default {
  async fetch(request) {
    const source = new URL(request.url);
    const normalizedPath = normalizePath(source.pathname);
    const destination = new URL(PRIMARY_ORIGIN);
    destination.pathname = LEGACY_ROUTES[normalizedPath.toLowerCase()] || normalizedPath;
    destination.search = source.search;

    return new Response(null, {
      status: 308,
      headers: {
        Location: destination.toString(),
        "Cache-Control": "public, max-age=3600"
      }
    });
  }
};
