# Hipobuy Tab — hipobuytab.com

Independent Hipobuy directory deployed to Cloudflare Workers with static assets. This folder is self-contained; sibling domains in seo-sites are unchanged.

## Deployment

Cloudflare project: `hipobuytab-com`. Repository: `hehaize88-code/seo-sites`, branch `main`, root directory `hipobuytab.com`.

Build: `ONNXRUNTIME_NODE_INSTALL_CUDA=skip npm ci && npm run build`.
Deploy: `npm run deploy` (uses `dist/server/wrangler.json`). Set `NODE_VERSION=22.16.0` and `ONNXRUNTIME_NODE_INSTALL_CUDA=skip` in the build environment. No D1, R2, paid inference, or product database is required. The pinned model/runtime files are installed during the build, served from this domain and never fetched from a third party by visitors.

Attach `hipobuytab.com` and `www.hipobuytab.com` as Worker custom domains. The Worker redirects www and HTTP to HTTPS apex, preserving paths and queries. All assets pass through the Worker so www asset URLs redirect too.

## Live catalogue

Product names, original links, prices, platform links and images are fetched from **https://cnfanshm.com**. `lib/catalog.ts` is a stateless adapter. No local product inventory, admin panel, copied product pictures, or fallback catalogue exists. Source pictures are not claimed to be warehouse QC or selectable SKUs. Currency prices use daily Frankfurter reference rates; CNY remains the fallback.

## Features

EN/DE/FR/ES/IT/PT/PL/ZH interfaces, 20 FAQ entries per language, three guides per language, original official Hipobuy logo/favicon, live catalogue/search, saved IDs on the visitor device, gallery, source purchasing links, Weidian link copy, 28 display currencies, browser-local image matching. Product vocabulary is localized while brand/model tokens are preserved; unknown words retain their source spelling.

Image search covers 6,041 source items in the shipped index. Uploaded images stay on the visitor device. The visual feature index is derived search data, not a product database. New source products require the documented index refresh. See VISUAL-SEARCH.md.

## SEO

Canonical origin: `https://hipobuytab.com`. English homepage is `/` (`/en` redirects); other pages retain locale-prefixed URLs. Eight-way hreflang and x-default are emitted. Internal search/filter URLs are noindex; main routes are indexable. Invalid routes and absent products use 404. `/robots.txt` advertises `/sitemap.xml`; it links a page map and eight product maps generated from the verified source IDs. Sitemaps refresh when the visual snapshot is rebuilt and the site redeployed.

## Development

`npm run dev`, `npm run check`, `npm run build`. The deployed app uses Vinext/React and a stateless Cloudflare Worker. No dependency on ChatGPT Sites authentication or hosting remains.
