# Superbuy Grid — superbuygrid.com

Independent Superbuy product directory. Official Superbuy logo and favicon assets are used; the site clearly states that it is not affiliated with Superbuy.

## Cloudflare deployment

- Repository: `hehaize88-code/seo-sites`
- Root directory: `superbuygrid.com`
- Branch: `main`
- Build command: `npm run build`
- Deploy command: `npm run deploy`
- Node: 22.16.0 or newer
- Worker: `superbuygrid-com`
- Custom domains: `superbuygrid.com`, `www.superbuygrid.com`
- Git build include path: `superbuygrid.com/**`

The Worker redirects HTTP and www to `https://superbuygrid.com` with 308, preserving path and query. Build output is generated in `dist/`; it is not committed. Unknown routes return 404. The server renders the current route and source product data before hydration. Google and Bing DNS verification records are unrelated to this deployment and must be preserved.

## Data and images

Catalog, product titles/prices, image URLs and other-agent purchase links come directly from `https://cnfanshm.com`, with a short in-memory response cache. There is no product database, admin application, or locally hosted product image inventory. Images load from their original source URLs. Currency conversion uses ExchangeRate-API and falls back to CNY if unavailable.

Image search uses 25,676 source image fingerprints captured on 2026-11-13. `source-chunks/image-index.json.part*` hold only search descriptors, source image URLs and product identifiers. The build creates browser search chunks, validating every URL and fingerprint. Search compares color and layout, not semantic item identity. Refresh the index to include newly added source images. One source listing had no available images and is not searchable.

Six interface languages are supported (EN, DE, FR, ES, IT, ZH). Product descriptor translation preserves brand/model names; malformed or uncommon source wording may remain partly untranslated. Style-specific links are enabled only if the source explicitly supplies that image's SKU URL; otherwise only the original listing link is available.

## Mobile

The mobile layout reduces vertical spacing, caps gallery heights, uses two compact product columns and retains 20-product pagination. Saved products also paginate. Style/agent panels scroll; QC reference images form a horizontal strip. All content remains reachable. Short pages remain shorter than three screens; long lists/detail pages target roughly three to five phone screens, depending on screen size, language and expanded sections.

## Indexing

The build generates `/sitemap.xml`, `/sitemap-pages.xml`, `/sitemap-products.xml`, and `/robots.txt` for the production domain. Sitemap product identifiers derive from the image-index snapshot, while product contents are fetched live. Saved lists and search-query results are not indexed.
