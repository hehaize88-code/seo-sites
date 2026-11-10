# Deployment record — 2026-11-10

Account: 9010cea800ac2a140509889d88fe612e (Wrangler OAuth; no credentials in this repository).
Zone: 75fefb3dfbb09ee9cdcd24fbf69a8791.
Main Worker: kakobuyitemhub-com -> kakobuyitemhub.com.
Redirect Worker: kakobuyitemhub-www -> www.kakobuyitemhub.com.

The user chose browser-local inference instead of paid hosting. Main site, model chunks and feature snapshot run from Cloudflare; no local services are required. No new paid subscription or inference service was enabled.

Validation: Astro build; six original/cropped query tests using the browser WASM engine all returned the target first; cloud image-search status6027, matched-ID detail API and bad-ID400; model/runtime assets reachable. Catalogue/search/category pagination, product details/USD,28FAQ/10guides, robots/sitemap and canonical verified over HTTPS. Redirect Worker handles dynamic AND static www paths; retest them with query strings after deployments. Mobile layout and browser event interaction have not been visually verified because the browser tool is unavailable.

All source images are remote; image-feature vectors are the user-approved search index. No product database. Preview and production folders are separate; apply future production edits here.

## Browser search fix — 2026-11-10
The browser distribution of Transformers retained bare ONNX package imports, so a native module Worker failed before inference. Prebuild now bundles these dependencies with esbuild and the WASM backend into `/visual/runtime-v2/transformers.js`; a build guard rejects unresolved package imports. The worker URL is versioned to bypass old caches.
Production deployment: `e3a39b69-010d-488d-ab3c-cebd593e897b`. Headless Chrome against the live domain (no request interception) returned eight results for source product 6067, with that product first, both on initial load and after a cached reload. A 390×844 viewport has no horizontal overflow. This does not establish real phone performance.
