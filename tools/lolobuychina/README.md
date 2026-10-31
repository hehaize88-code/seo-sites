# LoloBuyChina static site

Cloudflare Pages publishes `lolobuychina/` from this repository's existing `main` integration. Generated files are committed; deployment needs no package installation or build command changes.

## Build and check

Python 3 with BeautifulSoup4 is required for local editing:

```sh
python tools/lolobuychina/build.py
python tools/lolobuychina/validate.py
node tools/lolobuychina/behavior.test.mjs
```

English content lives in `content.en.json`. Eight translation dictionaries supply complete static translations; `overrides.json`, `reviewed/<language>.json` and `extra/<language>-*.json` contain reviewed wording. Later layers take precedence. The normal build uses committed dictionaries and no translation network service. Optional draft generation in `translate.py` uses separately downloaded official Argos models; binaries are not included. Drafts require semantic review before publication, especially negation, payment destinations, units and policies. Core pages, new articles, metadata and headings have explicit reviewed text; older long-form translations have targeted semantic review rather than native-editor certification.

All nine languages (English at `/`, de, fr, es, it, pt, ja, ko, zh) have the same 29 canonical routes: eight core pages and 21 articles. Language switches retain the page. Reciprocal hreflang and x-default are emitted in HTML and sitemap.xml. Removed duplicate guides and legacy article indexes redirect in the Worker. Unknown routes return an actual 404 with noindex.

The product catalogue links and source-ID mappings are retained. Unmatched marketplace identifiers open search, never invented catalogue URLs. Product cards show source IDs and a current-price link instead of presenting a fixed historical exchange rate as an offer. The existing GA4 ID is unchanged; product, category, article, search and language events include the page language.

Source review: 2026-10-31. Official homepage states 180 days of free storage; order-level eligibility and deadlines still control, and storage does not extend return windows. No universal return deadline, fee percentage, shipping divisor or transit promise is asserted.

Do not change the translation source without updating every locale. The build fails on missing translation strings. Run all checks before committing the generated directory. Browser QA should include homepage, localized article, language switching, product search, mobile layout and live redirects after Pages deployment.
