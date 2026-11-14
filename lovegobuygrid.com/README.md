# lovegobuygrid.com

Independent Lovegobuy catalog, deployed from this directory only.

- Build: `npm run build`
- Deploy: `npm run deploy`
- Worker: `lovegobuygrid-com`
- Domains: `lovegobuygrid.com`, `www.lovegobuygrid.com` (308 to apex)
- Product records, prices, pictures and destination links: fetched live from cnfanshm.com; no database.
- Thirty interface languages; brands and unrecognized descriptive seller titles remain original.
- Source has no reliable SKU/QC labels; gallery stays unclassified, original Weidian link copy available.
- Image similarity: browser-local RGB fingerprints, snapshot 2026-11-13, 25,676 images across 6,041 illustrated listings. Additional photos included. New images require index rebuild. Results checked against live detail.
- FX: daily public ExchangeRate-API rates; original CNY fallback.
- Official Lovegobuy branding. Custom localized upload control.
- `/robots.txt`, `/sitemap.xml` (210 interface URLs); preview noindex removed on production. Product sitemap not yet included.

`source-chunks` contains base64 fragments of branding and derived image signatures, reconstructed into static assets at build time. No product database or uploaded query image is stored.
