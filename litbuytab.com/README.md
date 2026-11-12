# litbuytab.com
Independent Litbuy product-discovery site. Product data and photos are fetched from cnfanshm.com; no product database or admin panel.

## Cloudflare Workers deployment
Root directory: `litbuytab.com`
Build command: `npm ci --ignore-scripts && npm run build`
Deploy command: `npx wrangler deploy`
Domains configured: `litbuytab.com`, `www.litbuytab.com` (308 redirect to apex).
Requires a Cloudflare account containing this zone and Workers deployment access. Do not put API tokens in this repository.

The browser-local image search uses the checked-in cnfanshm image descriptors and checksum-verified model asset chunks. The build restores model files and bundles the search worker. Uploads stay in the visitor's browser.

Eight interface languages; compact mobile layout. Source lacks verified SKU and QC fields, so no fabricated variants or QC photos. See `public/visual/coverage.json` for image-index dates and coverage. Sitemap is built from all indexed product refs. Prices use source CNY values and dated exchange rates.
