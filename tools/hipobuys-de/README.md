# HipoBuys.de editorial build

Run from the repository root:

```sh
python -m pip install -r tools/hipobuys-de/requirements.txt
python tools/hipobuys-de/build.py
python tools/hipobuys-de/validate.py
```

The build reads seven article topics in each of eight languages from `content/` and generates 64 static pages, including eight language homepages. The safety and link troubleshooting articles are new (16 URLs); fees, shipping, W2C, QC and coupons retain their existing URLs. The two new English articles contain 1,200–1,800 words each. Every language has substantive localized body text, metadata and article navigation.

The German-only additional guides and all root product pages remain available. Product destinations are preserved. Root home, guide and language pages link directly to the new articles in every language. The sitemap contains 92 canonical URLs after this release. Existing GA4 ID and product click events are retained; article clicks now include every localized route, and native language navigation records `language_change`.

Public sources reviewed on 2026-11-02:

- https://hipobuy.com/ — purchasing, warehouse, inspection and parcel process.
- https://hipobuy.com/notice/1740653781924810754 — service and fee categories.
- https://hipobuy.com/goods/details?channel=WEIDIAN&id=7797612745 — product-source and quality/authenticity notices.
- https://hipobuy.com/goods/details?channel=WEIDIAN&id=7819303386 — store availability and restriction notices.

Advice and arithmetic examples are original explanations, not published tariffs or first-hand purchase reviews. No fixed free-photo count, additional photo/video price, exchange-rate markup, active coupon or guaranteed delivery time is asserted.

Deployment uses the existing Git integration: `hehaize88-code/seo-sites`, production branch `main`, Cloudflare Pages project `hipobuys-de-site`, output `hipobuys-de`. Generated HTML is committed; no new production build dependency is required. The worker skips legacy automatic translation injection on pages with native article-language navigation and retains the old helper on legacy pages.
