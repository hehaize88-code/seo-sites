const CANONICAL_HOST = "cssbuys.store";

const LEGACY_PATHS = new Map([
  ["/guides", "/guides/"],
  ["/guides.html", "/guides/"],
  ["/products/5691", "/products/3402"],
  ["/products/5940", "/products/3401"],
  ["/products/5987", "/products/3400"],
  ["/products/5975", "/products/3399"],
  ["/products/5963", "/products/3398"],
  ["/products/5985", "/products/3397"],
  ["/products/6052", "/products/3396"],
  ["/products/5910", "/products/3395"],
  ["/products/5973", "/products/3394"],
  ["/products/5751", "/products/3393"],
]);

const CATEGORY_ROUTES = new Map([
  ["accessories", "accessories"],
  ["electronics", "electronics"],
  ["headwear", "headwear"],
  ["hoodies-sweaters", "hoodies-sweaters"],
  ["jackets", "jackets"],
  ["jersey", "Jersey"],
  ["other-stuff", "other-stuff"],
  ["pants-shorts", "pants-shorts"],
  ["shoes", "shoes"],
  ["short-sets", "short-sets"],
  ["t-shirts", "t-shirts"],
]);

const SECURITY_HEADERS = {
  "Content-Security-Policy": "default-src 'self'; img-src 'self' data: https://www.cnbuycha.com; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com; connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com; form-action 'self' https://www.cnbuycha.com; base-uri 'self'; frame-ancestors 'none'; upgrade-insecure-requests",
  "Permissions-Policy": "camera=(), geolocation=(), microphone=(), payment=()",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "DENY",
};

function redirect(url, pathname, hostname = CANONICAL_HOST) {
  const target = new URL(url);
  target.protocol = "https:";
  target.hostname = hostname;
  target.port = "";
  target.pathname = pathname;
  return Response.redirect(target.toString(), 301);
}

function cleanPathname(pathname) {
  if (pathname === "/index.html") return "/";
  if (pathname.endsWith("/index.html")) return pathname.slice(0, -10);
  return pathname.endsWith(".html") ? pathname.slice(0, -5) : pathname;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const cleanPath = cleanPathname(url.pathname);
    const legacyTarget = LEGACY_PATHS.get(cleanPath) || LEGACY_PATHS.get(url.pathname);

    if (url.hostname !== CANONICAL_HOST || url.protocol !== "https:") {
      return redirect(url, legacyTarget || cleanPath);
    }

    if (legacyTarget) return redirect(url, legacyTarget);
    if (cleanPath !== url.pathname) return redirect(url, cleanPath);

    const categoryMatch = cleanPath.match(/^\/categories\/([^/]+)\/?$/);
    if (categoryMatch && CATEGORY_ROUTES.has(categoryMatch[1])) {
      const target = new URL(`https://www.cnbuycha.com/${CATEGORY_ROUTES.get(categoryMatch[1])}/`);
      target.search = url.search;
      return Response.redirect(target.toString(), 301);
    }

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
