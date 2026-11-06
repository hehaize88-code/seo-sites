# hipobuys.store editorial build

Source content is maintained in `content/{en,de,fr,es,it,pl,pt,nl}.txt`.
All ten article topics must exist in every language. English retains the
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

## November 2026 release

- Added three distinct guides in all eight languages: returns/refunds and wallet credit, missing QC photos and precise extra-photo requests, and shipping estimate versus final charge (24 URLs). English drafts are 1,200–1,300 words; every translation covers all eight sections and the same worked examples.
- Improved all seven existing editorial topics (56 URLs), including query-led titles/descriptions for the four high-priority pages, stage/action tables and contextual next-step navigation. Kept original URLs and publication dates.
- Added twenty localized FAQ answers per language and consistent navigation to Spreadsheet, QC, Shipping, FAQ, Articles and buying guidance. Existing archive pages remain accessible.
- Preserved G-N31DJZNW37 and existing product/calculator events; added guide_next_click with only destination path and existing language/path context. No account conversion or external analytics configuration changes are implied.
- Regenerated all three equivalent sitemap endpoints with 186 canonical routes; added HTTP normalization to the existing single-step host/path redirect.

Prioritization evidence: GSC settled 7 October–3 November 2026 had 54 clicks / 3,086 impressions / 1.7% CTR versus 35 / 1,724 / 2.0% in the prior period. Shipping-time had 0 clicks / 277 impressions; tracking 4 / 303; calculator 9 / 277; warehouse 13 / 265. Bing 7 October–5 November had 0 clicks / 16 impressions. Its broader keyword research suggests spreadsheet and shop intent, not Google search volumes. GA4 9 October–5 November recorded 118 sessions, 50 organic sessions, 6 outbound_product_click events and 5 shipping_weight_calculation events. These periods and measures are not combined into one metric.

Primary policy sources reviewed 6 November 2026:
- https://hipobuy.com/notice/1740617772327604226 (Chinese returns policy: eligibility, application timing, condition and buyer-reason return charges)
- https://hipobuy.com/notice/1901881491622285313 (Chinese order/parcel status: domestic stage, intake/storage, balance credits and shipping top-up stage)
- https://hipobuy.com/notice/1740653781924810754 (service and fee components)
- https://hipobuy.com/ (warehouse inspection workflow; company-office addresses do not establish a personal forwarding destination)

Competitor topic checks included hipobuyspreadsheet.com/guide/returns-and-refunds/ and hipobuywithqc.com/qc. Their wording and unverified timing claims are not reproduced as platform rules. New guides are original practical explanations with illustrative, explicitly labelled arithmetic. There are no live price, stock, ranking or delivery guarantees.

Run the structural and runtime checks above before committing generated output. The verifier now requires ten articles and twenty FAQ answers in each of eight languages, complete new-article sections, reciprocal language metadata, contextual internal links and sitemap coverage. No other domain folder is part of this release.
