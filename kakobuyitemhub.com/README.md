# Kakobuy Item Hub

Production: https://kakobuyitemhub.com
Staging: https://kakobuyitemhub-com.hehaize88.workers.dev

Astro SSR site in the independent `kakobuyitemhub.com` folder of `hehaize88-code/seo-sites`. Product information, prices, original links and product images come from cnfanshm.com. No independent product database or admin panel.

## Build and publish

Use Node.js 24. Run `npm ci`, then `npm run build`. The prebuild step verifies model/index asset checksums and restores missing files from the deployed asset snapshot (about108MB). Generated model/feature assets are ignored in Git; application code, snapshot manifest and generation scripts are versioned. Original product images are never copied into these assets.

Deploy the main site with `npx wrangler deploy --config dist/server/wrangler.json`. Deploy the independent www redirect with `npx wrangler deploy --config wrangler.redirect.jsonc`. Do not add www to the main config: the small redirect Worker handles ALL www paths, including static assets. Never use the local preview source relay or temporary tunnel for production.

## Browser image search

User chose browser inference to avoid paid inference hosting. A dedicated browser Worker runs quantized CLIP ViT-B/32 with WebAssembly, then searches 6027 image-feature vectors locally. Uploaded/selected photo pixels never leave the device. Only up to8 matched product IDs are sent to `/api/visual/products` to fetch current source metadata. First use downloads about108MB of public model/runtime/index files, cached in Cache Storage when available; low-memory devices may need to retry on a computer. No paid API, R2, KV, database or persistent inference server was added.

`public/visual/search-worker.js` is the browser worker. `src/content/visual-status.json` describes the current snapshot; `src/content/visual-assets.json` pins checksums. Full images stay on cnfanshm.com. The snapshot is dated and does not auto-refresh when the source changes.

To regenerate: run the existing `visual-service/build-index.mjs` with the required model cache locally; then run `node scripts/prepare-visual-assets.mjs INDEX_JSON MODEL_DIRECTORY`. Publish under a NEW asset version path when changing existing immutable assets, update the worker/manifest references and tracked checksums, rebuild and deploy. The local server in `visual-service/server.mjs` is legacy development support; production does not call it.

## Content and SEO

English/Chinese editorial content with official references; 8 interface languages. Untranslated editorial locales clearly fall back to English. Source CNY prices are converted to estimated USD at the dated rate in `src/content/exchange-rate.json`; the rate is a snapshot, not a live checkout quote. Registration and buying links retain their supplied affiliate codes. Official Kakobuy logo/favicon; GA4 G-KDMC5GFZXN.

Apex HTTPS is canonical; www/HTTP return301 preserving path/query. Main HTML is indexable on apex only; staging, search queries and untranslated locales are noindex. Robots and sitemap are server routes. Browser click/visual QA is limited by the current local browser-tool failure; WASM engine retrieval, HTTP routes, static assets, metadata and redirects are tested separately.
