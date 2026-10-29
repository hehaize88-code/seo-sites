# Multilingual SEO release — 2026-10-29

## Scope and research decisions

The site owner authorised improvements and production deployment across every existing language. The research reviewed first-party Search Console, Bing Webmaster and GA4 reports, public search results, competitor coverage and Pikobuy's official documentation. Private report exports and account data are not included in this public repository.

The prioritised search intents are Pikobuy spreadsheet/product discovery, QC photos and measurements, shipping cost calculation, destination planning, warehouse consolidation and tracking that has stopped updating. No competitor traffic estimates, keyword difficulty scores or monthly keyword volumes were verified. The site has a short observation history; this release makes no traffic-growth promise.

## Published changes

- 24 complete language editions remain: nl, en, de, es, fr, it, pl, pt, ro, sv, da, fi, el, cs, hu, bg, sk, hr, sl, lt, lv, et, ga, mt.
- Three new articles, each with approximately 1,200–1,250 English prose words, a comparison worksheet and a worked example. Every locale retains all paragraphs, sections and tables.
- Existing tracking, QC measurement and warehouse-return articles gain a decision section. All ten existing articles receive relevant links to the new content.
- QC and shipping hubs receive substantive, localised steps and official-source links.
- Three focused category landing pages per language: `/spreadsheet/shoes/`, `/spreadsheet/sweatshirts/` and `/spreadsheet/tshirts/`. Each has category-specific product HTML from the live source, localised copy, a unique canonical and crawlable links. Other filters remain query controls.
- Homepage and catalog titles/descriptions now explain their actual content. No invented brands, prices, QC images, ratings or availability claims were introduced.
- 23 routes per language, 552 canonical HTML pages in total. The sitemap includes all locales, x-default and explicit editorial modification dates.
- Product detail, purchase-link, registration-link, category and catalog-search intent events use the existing GA4 tag on the production hostname only. No purchase or registration completion is inferred.

## Primary sources checked

- [Shopping guide](https://www.pikobuy.com/guide): separates purchase, warehouse inspection, international shipping payment and dispatch. Its three-day statement refers to tracking availability after dispatch, not delivery.
- [Shipping estimator](https://www.pikobuy.com/shipping-cost): destination, product type, kg and three dimensions in cm. No destination quote, fixed tariff or universal volumetric divisor is asserted.
- [Contact page](https://www.pikobuy.com/contact): items from different sellers can share a parcel. A saving is not guaranteed for every configuration.
- [Returns](https://www.pikobuy.com/protocol/returns): timing, seller approval and packaging conditions matter. Published shipping-fee wording is inconsistent; exact charges require confirmation for the order.
- [Shipping terms](https://www.pikobuy.com/protocol/shipping): forwarding and inspection limitations. No universal free-storage duration was established.
- [User agreement](https://www.pikobuy.com/protocol/user): inspection is not universal proof of authenticity or performance.
- [Terms](https://www.pikobuy.com/protocol/terms): cross-border charges can be additional. The Europe article gives no tax rates, thresholds or legal exemptions.

The new prose consists primarily of original planning methods, decision worksheets and clearly labelled hypothetical examples. Official-source summaries are limited and do not reproduce policy tables.

## Verification and follow-up

Run `npm run check:catalog`, `npm run check:source`, `npm run build`, then `npm run check:editorial`. Checks cover all locale content shapes and rendered paragraphs, canonical/hreflang, internal links, real product snapshots, sitemap coverage, article metadata, source-backed purchase IDs, filtering/pagination, Worker responses and preview/query noindex behaviour. Every rendered page is compared byte-for-byte with its Worker response. HTML is compressed by locale and the runtime caches at most two expanded locales, keeping the release artifact within a conservative 3 MB compressed project budget. After deployment, run `npm run check:live` to verify all 192 new article/category and expanded hub URLs, the live sitemap and catalog/product APIs.

Production remains the existing `pikobuysheet-nl` Cloudflare Worker, deployed automatically from GitHub `main` changes under `pikobuysheet-nl/**`. This release does not change DNS, security settings, platform credentials or the source database.

After sufficient data accumulates, compare Google and Bing impressions/clicks by query and landing page over matched periods. Inspect the new category and article URLs for discovery/indexation. In GA4 compare organic landing sessions with `view_item`, `purchase_click` and `signup_click`; the last two indicate clicks, not completed conversions. Keep branded and non-branded findings separate and avoid interpreting tiny samples as durable conversion rates.
