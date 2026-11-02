# CSSBuys DE editorial release — 2026-11-02

Production remains the static `cssbuys-de/` directory on the existing Cloudflare Pages project, deployed from `main`. No framework migration, domain change or replacement of the product catalogue.

Run with Python 3 and Beautiful Soup 4:

```sh
python tools/cssbuys-de/build.py
python tools/cssbuys-de/validate.py
node tools/cssbuys-de/events.test.mjs
```

`content/{en,de,fr,es,it,pl}.txt` contains three original localized articles. The release also updates seven existing topics in all six languages, localized FAQ pages, navigation, home feeds and the sitemap. Existing article URLs are preserved. `data-content-revision` makes the one-time old-content cleanup safe to rerun; new articles and hubs rebuild from source. Do not change that revision without reviewing the old-content transformation.

Research priorities: existing first-party query demand for TYG-EU-Tariffless Express; shipping estimate questions; a hoodie/jacket category gap. Category demand is an editorial hypothesis, not a claimed keyword volume. Public CSSBuy route and packaging information was reviewed on 2026-11-02. No live checkout, coupon redemption, shipment, product purchase or authenticity test was conducted. Numerical parcel examples are illustrative. Account-specific rehearsal prices and cancellation rules are deliberately not invented.

`catalog_outbound_click` now covers both catalogue and product exits, with language, page path, placement and destination type. The legacy `product_outbound_click` remains for historical reporting: do not sum it with the catalogue event as independent conversions. No typed search terms or URL query strings are collected by this script. GA4 key-event configuration is separate from the website release.

Validation checks all 156 sitemap URLs, canonical and indexability metadata, internal paths and fragment links, six complete 22-guide hubs, six-card home feeds, reciprocal multilingual clusters, JSON-LD, and English article length. Event behavior is verified without sending analytics data. Indexing and traffic improvements remain search-engine outcomes rather than deployment guarantees.
