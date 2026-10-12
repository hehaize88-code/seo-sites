# hoobuys.org multilingual SEO release — 2026-10-12

Scope is only `hoobuys-org/`. The existing GitHub main → Pages integration remains the deployment path; no hosting account configuration is changed.

- 9 complete static locales: en, zh-CN, de, fr, es, it, pl, nl, pt.
- 27 indexable URLs per locale; 20 full guides per locale, including three new 1,240–1,270-word English originals.
- Original article body text is retained. All 17 existing guides gain practical introductions and related reading; shipping and the two shorter workflows are expanded.
- Distinct home/product/guide titles, reciprocal hreflang, self-canonicals, localized Article metadata and navigation, XML and text sitemaps.
- The user-confirmed main site for hoobuys.org is https://cnfanssp.com. All language versions use this domain for product and category links, and GA4 outbound product-click tracking matches it. Product records and image URLs were re-read from this site; identical numeric IDs on another domain are not treated as the same products. All 10 destinations, their images and all 7 category routes returned HTTP 200 on 12 October 2026.
- GA4 property tag G-Q60K7ELE45 retained; product_index_click and guide_click retained, language_switch and shipping_calculator_use added. Click payloads omit query strings and entered parcel values.
- Offline Argos translation drafts, with reviewed titles, navigation, introductions and terminology overrides. Models are not deployed. Translation caches and full generated HTML are committed.

## Inputs to the work

The content plan prioritizes product-link discovery, spreadsheet workflows, usable shipping tools and QC guidance. Public SERP examples included JadeShip's HooBuy spreadsheet search and SpreadFinds' HooBuy page. No competitor keyword volumes are asserted. Account analytics and search-performance exports are not included in this public repository.

## Fact checking for new guides

Official sources checked 12 October 2026:
- https://hoobuy.com/estimation — destination, grams, centimetre dimensions, category, minimum and subsequent units, route limits, illustrative volumetric divisor.
- https://hoobuy.com/product/2/7734015200 — basic inspection is not authentication.
- https://hoobuy.com/product/2/7668054600 — QC interface and separate seller-to-warehouse/international delivery stages.
- https://hoobuy.com/ — purchase, warehouse review, consolidation and international shipping sequence.

No live freight price, universal divisor, guaranteed QC count, fee schedule, return period, refund policy or delivery promise was inferred. New calculations and budgets are explicitly hypothetical editorial examples. Official sources are fact-check inputs, not commercial outbound CTAs.

## Rebuild and verify

Runtime dependencies: Python with beautifulsoup4 and ftfy. For new translation text, also install ctranslate2, sentencepiece, sacremoses and subword-nmt. Argos models are downloaded separately from the official argospm-index.

1. `python hoobuys-org/_src/build.py`
2. When English source text changes, run `python hoobuys-org/_src/translate.py --models /path/to/argos-models`.
3. For changes to reviewed translations, update the override scripts, run editorial-overrides.py then review-translations.py.
4. `python hoobuys-org/_src/build.py --all`
5. `python hoobuys-org/_src/verify.py`
6. `node hoobuys-org/_src/check-runtime.mjs`

Publish the committed static output. The worker blocks public access to `_src`, preserves old extensionless URLs and existing fragment IDs, redirects html/index aliases and serves 404 status for missing pages. No browser-based local visual QA was run because the managed Sites environment requires skipping it when its browser tool is unavailable. Production is checked separately after deployment.
