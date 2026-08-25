const CANONICAL_HOST = "hipobuys.uk";

const LEGACY_REDIRECTS = new Map([
  ["/uk-hipobuy-fees-guide-2026", "/en/hipobuy-fees/"],
  ["/uk-hipobuy-shipping-estimate-guide", "/en/shipping-from-china/"],
  ["/uk-qc-photos-before-shipping", "/qc-checklist-uk-buyers"],
  ["/uk-shipping-guide", "/hipobuy-uk-shipping-line-selection"],
  ["/uk-w2c-links-product-route-guide", "/en/w2c-links/"],
  ["/w2c-links-guide", "/en/w2c-links/"],
  ["/uk-hipobuy-coupons-insurance-checklist", "/en/hipobuy-coupon/"],
  ["/hipobuy-uk-qc-w2c-shipping-check-2026-07-10", "/hipobuy-uk-w2c-qc-shipping-workflow-2026"],
  ["/en", "/"],
  ["/en/", "/"],
]);

const SECURITY_HEADERS = {
  "Content-Security-Policy": "default-src 'self'; img-src 'self' data: https://www.cnbuycha.com; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com; connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com; form-action 'self' https://www.cnbuycha.com; base-uri 'self'; frame-ancestors 'none'; upgrade-insecure-requests",
  "Permissions-Policy": "camera=(), geolocation=(), microphone=(), payment=()",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "DENY",
};

function permanentRedirect(url, pathname, hostname = CANONICAL_HOST) {
  const target = new URL(url);
  target.protocol = "https:";
  target.hostname = hostname;
  target.port = "";
  target.pathname = pathname;
  return Response.redirect(target.toString(), 301);
}

function cleanPathname(pathname) {
  if (pathname === "/index.html") return "/";
  return pathname.endsWith(".html") ? pathname.slice(0, -5) : pathname;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const cleanPath = cleanPathname(url.pathname);
    const legacyTarget = LEGACY_REDIRECTS.get(cleanPath);

    if (url.hostname !== CANONICAL_HOST || url.protocol !== "https:") {
      return permanentRedirect(url, legacyTarget || cleanPath);
    }

    if (cleanPath === "/de" || cleanPath === "/de/" || cleanPath.startsWith("/de/")) {
      return permanentRedirect(url, cleanPath, "hipobuys.de");
    }

    if (legacyTarget) return permanentRedirect(url, legacyTarget);
    if (cleanPath !== url.pathname) return permanentRedirect(url, cleanPath);

    const response = await env.ASSETS.fetch(request);
    const headers = new Headers(response.headers);
    for (const [name, value] of Object.entries(SECURITY_HEADERS)) {
      headers.set(name, value);
    }

    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers,
    });
  },
};
