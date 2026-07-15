const LOCALIZED_LANGUAGES = new Set(["de", "fr", "es", "pl"]);

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
  if (LOCALIZED_LANGUAGES.has(language) && path.replace(/\/+$/, "") === `/${language}`) {
    return `/${language}/`;
  }
  if (path.length > 1) path = path.replace(/\/+$/, "");
  return path || "/";
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const original = url.toString();
    if (url.hostname.toLowerCase() === "www.hoobuys.net") url.hostname = "hoobuys.net";
    url.pathname = normalizePath(url.pathname);

    if (url.toString() !== original) {
      return new Response(null, {
        status: 308,
        headers: {
          Location: url.toString(),
          "Cache-Control": "public, max-age=3600"
        }
      });
    }
    return env.ASSETS.fetch(request);
  }
};
