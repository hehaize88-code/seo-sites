export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === "www.lolobuychina.com") {
      url.hostname = "lolobuychina.com";
      return Response.redirect(url.toString(), 301);
    }

    const response = await env.ASSETS.fetch(request);
    const contentType = response.headers.get("content-type") || "";
    if (!contentType.includes("text/html")) {
      return response;
    }

    const headers = new Headers(response.headers);
    headers.set("Cache-Control", "no-cache, max-age=0, must-revalidate");
    headers.set("Cloudflare-CDN-Cache-Control", "no-store");
    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers
    });
  }
};
