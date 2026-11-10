# Kakobuy Item Hub

Astro SSR storefront for kakobuyitemhub.com. Product data, product images and original marketplace links are read live from cnfanshm.com. No product database or admin panel.

Staging: https://kakobuyitemhub-com.hehaize88.workers.dev

## Build and deploy

- Node.js 24; npm ci; npm run build.
- npx wrangler deploy --config dist/server/wrangler.json
- Initial deployment has no custom domains; after staging validation, merge routes from wrangler.domains.json into wrangler.jsonc, build and deploy again.
- Never set PREVIEW_SOURCE_BRIDGE in this project; production reads the source directly.
- Source prices are CNY, displayed as estimated USD using the dated rate in src/content/exchange-rate.json. Refresh the rate before release; actual checkout fees/rates may differ.

## Release status

Cloudflare staging is deployed and source catalogue, category, pagination, detail and FAQ checks pass. Domain binding is pending full release validation. www-to-apex301 code preserves paths and query strings. Image search requires production inference hosting; the checked-in visual-service is the local implementation and must not be mistaken for a deployed service. Do not connect production to a temporary tunnel.

Full English/Chinese editorial content, eight interface languages. Other editorial locales explicitly display English fallback. Model files, feature index, caches and credentials are excluded. Official logo/favicon remain referenced from Kakobuy. GA4: G-KDMC5GFZXN.
