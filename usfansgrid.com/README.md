# USFans — The Find Edit

Production domain: https://usfansgrid.com. Deployment authorized on 2026-11-12.

## Deployment destination after approval

`https://github.com/hehaize88-code/seo-sites/tree/main/usfansgrid.com`. Cloudflare Worker: `usfansgrid-com`. This project is separate from usfanstab.com.

## Data

- All catalogue entries, prices, seller images, product galleries and original marketplace URLs are fetched from `https://cnfanshm.com` when requested.
- Product images load from that source's `/uploads/` URLs. No generated images, substitute stock photos, product fixtures, catalogue database or management dashboard.
- An in-process 60-second HTML request cache avoids repeated source requests. It expires automatically and is not a persistent catalogue.
- Saved finds store only listing IDs in the visitor's browser; details are loaded again from the source.
- USFans purchase links use the verified `/product/3/{weidianId}` route only when the source supplies a Weidian original URL. Missing or unavailable source data is displayed as unavailable.
- Prices are source CNY values. No invented exchange rates, availability counts or QC photos.

## Languages

English, German, French, Spanish, Italian, Portuguese, Polish and Simplified Chinese use separate routes. Interface, guides, FAQ and common product-type words are translated. Brands, model strings and original IDs are preserved. The product-name vocabulary is presentation logic, not stored product data. Unknown source words are kept rather than guessed.

## Preview

Production pages use canonical and reciprocal hreflang URLs on usfansgrid.com. Preview hosts remain noindex. Search/filter and saved pages are noindex. The XML sitemap index links the page sitemap and eight product sitemaps.

Built with the Sites Vinext starter. `npm run dev` starts development; `npm run build` builds the Worker. No D1 or R2 bindings are configured.

## Product detail and visual search upgrade
- Official USFans header logo: `https://media.usfans.com/webresource/v1/app/7f2439bb1554488bb7a14afb3f638c3e.webp`; favicon: `https://www.usfans.com/favicon.png`. Original bytes retained.
- Currency references: Frankfurter daily CNY rates, date displayed; missing rates revert to CNY. All cards and detail views share the preference.
- Other-agent URLs are parsed directly from each source listing. No new referral codes are invented.
- Source gallery photos do not identify SKU choices. Copying the Weidian link copies the source product URL; there is no invented SKU query string. QC is separately labeled only when the source provides reliable QC metadata (currently absent).
- Eight supported locales translate the complete interface and descriptive product vocabulary. Brand and model names remain unchanged. Language changes preserve path/query, including the active gallery photo.
- Visual search compares DINOv2 descriptors for every indexed image and ranks each product by its best image. Results re-fetch current source data and verify the image URL fingerprint before displaying the exact matched photo.
- Product data and photos remain at cnfanshm.com. The static visual artifact contains only record IDs, image-position references, URL hashes and image vectors. There is no product database and uploaded search photos stay in the browser.
- `public/visual/index.json` publishes coverage counts, completeness and build date. Never describe an incomplete build as full-site gallery coverage.
- Rebuild: `npm run visual:index`. Crawl checkpoints live under ignored `work/visual/`, not in the published app. The default command refreshes catalogue pages and galleries, then uses a bounded image-download pool with serialized model inference. `--resume-catalog --crawl-only` resumes an interrupted gallery crawl; `scripts/index-images-pooled.mjs` and `scripts/package-visual-index.mjs` resume image work from ignored checkpoints.
- Preview remains noindex; production is usfansgrid.com.

### Verified gallery coverage (2026-11-11)
6,041 products, 25,648 unique images and 25,676 product/photo references were checked against the complete source crawl. No missing products or images remained. `node scripts/audit-visual-index.mjs --require-complete` verifies the published feature index against the crawl. New or changed source images require rebuilding the visual index; displayed product details and prices remain live.

## Cloudflare Workers Git build
- Repository: hehaize88-code/seo-sites, branch main, root directory usfansgrid.com.
- Build command: npm run build:cloudflare
- Deploy command: npm run deploy:cloudflare
- Node.js 22 or later. No database, API credentials or new paid service required.
- Bind usfansgrid.com and www.usfansgrid.com as custom domains after deployment. The Worker redirects www and HTTP to HTTPS on the apex.
- Mobile layout uses compact spacing and horizontally scrollable galleries. Saved finds and image-search results show 12 items per page without dropping matches. Catalogue keeps 20 items per page.
