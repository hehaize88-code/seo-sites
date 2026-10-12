# hipobuys.store editorial build

Source content is maintained in `content/{en,de,fr,es,it,pl,pt,nl}.txt`.
All seven article topics must exist in every language. English retains the
existing root URLs; other languages use their existing language directory.
The old English homepage `/en/` redirects to `/`.

Run from the repository root with Python (lxml available) and Node:

```
python tools/hipobuys-store/build.py
python tools/hipobuys-store/verify.py
node tools/hipobuys-store/verify-runtime.mjs
git diff --check
```

The static output is `hipobuys-store/`. The existing production integration
deploys this directory from GitHub `main`; no new hosting project is needed.
Review generated HTML, `_worker.js` and the sitemaps in the same commit as
their source changes. `routes.json` is generated, not an independent route list.

## October 2026 changes

- Reworked tracking, warehouse address, shipping calculator and rehearsal guides.
- Added shipping-time, clothing/shoe sizing and sneaker-selection guides.
- Published all seven topics in eight languages (56 article URLs), including
  reciprocal hreflang, same-article language navigation and localized metadata.
- Replaced English boilerplate in the 40 existing localized topic landing pages
  with localized introductions and relevant reading routes.
- All eight homepages and article indexes link to the localized article set.
- Added an illustrative billable-weight tool. It provides no live prices and
  does not assume its example divisor is a Hipobuy-wide rule.
- Existing product images are retained in home previews; current stock and
  prices are not claimed to have been verified. Product CTAs use cnfanshp.com.
- Allowed GA4 collection endpoints in CSP, kept G-N31DJZNW37, and added
  `outbound_product_click`, `product_search`, `language_switch` and
  `shipping_weight_calculation` events. Custom search tracking excludes the
  entered search words. Actual collection still requires production validation.
- Stopped rewriting official Hipobuy references into internal guide URLs.
- Fixed `/locale/index.html` normalization and supplied the complete sitemap at
  both `/sitemap.xml` and the previously submitted `/google-sitemap.xml`.

Research prioritization used GSC's 12 September–9 October 2026 window: the
order-status page had 462 impressions/3 clicks, warehouse 295/10, rehearsal
149/6 and calculator 85/5. Shipping-time has a small observed query signal;
sizing and sneaker discovery are competitor-informed opportunities, not
measured keyword-volume claims. No CTR, ranking or traffic increase is promised.

Primary reference entry points:
- https://hipobuy.com/
- https://hipobuy.com/estimation
- https://www.dhl.com/discover/en-gb/ship-with-dhl/products-and-services/weight-and-dimensions
- https://www.nike.com/size-fit/mens-footwear
- https://developers.google.com/tag-platform/security/guides/csp?hl=en

Account-specific receiving addresses, current shipping prices, exact delivery
promises, storage deadlines and current rehearsal fees are intentionally not
invented. The live account and selected carrier terms determine those details.
