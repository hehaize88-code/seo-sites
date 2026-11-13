# Oopbuy Grid — oopbuygrid.com

Production website for https://oopbuygrid.com, migrated from the Oopbuy Finds preview.

## Deploy

- Repository: hehaize88-code/seo-sites
- Root directory: oopbuygrid.com
- Build: npm run build
- Deploy: npx wrangler deploy
- Worker: oopbuygrid-com
- Domains: oopbuygrid.com and www.oopbuygrid.com

The worker redirects HTTP and www to HTTPS on the apex domain. The build prerenders 6,062 HTML routes, including all 6,042 product listings, and generates sitemap.xml, sitemap-pages.xml, sitemap-products.xml and robots.txt. Unknown paths return 404. Generated files live in dist and are not committed.

## Catalog and languages

The public directory retains the verified cnfanshm.com snapshot: 6,042 listings, 11 categories, and 25,676 searchable image records. Image matching compares color and layout, not semantic identity. One listing lacks source images and a valid purchase URL; its purchase buttons remain disabled.

24 interface languages are retained. Product-name localization uses a terminology dictionary; complex or malformed source titles may remain partly untranslated. This deployment does not claim full-sentence translation or separate indexable language pages. The ten existing guides remain short guides, not expanded SEO articles.

## Source

public/app.js and public/style.css are the application source. public/index.html is the HTML shell. build.cjs prerenders the same application functions for crawlable initial HTML. Language and image-search assets are self-contained in public. No database or private credentials are required.

Large catalog JSON assets are stored losslessly in source-chunks to support API-based repository uploads. The build concatenates numbered parts into their original JSON assets.
