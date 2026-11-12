# Litbuy preview
User requirements: all product data and images read only from https://cnfanshm.com. No independent database or admin. Public preview first; formal domain later. Deployment repository: https://github.com/hehaize88-code/seo-sites, one folder per domain.
Verified official register https://litbuy.com/register ; Weidian purchase /product/2/{original marketplace ID}.
2026-11-12: live source HTML adapter for home, categories, keyword search, pagination, product galleries and original IDs. No product fixtures. Eight UI languages. Generic category product titles translated; complex source titles preserved and disclosed. Source prices displayed as listed, currency not assumed due to inconsistent upstream metadata. Preview noindex. No QC claims or synthetic imagery.

## 2026-11-12 detail and visual search revision
- Official branding: https://litbuy.com/static/img/logo.9dc463e0.png and https://litbuy.com/favicon-new.ico, downloaded unchanged into public/brand. Official page DOM and HTML checked.
- Official product 7777809164 displayed CNY 159, matching source numeric 159; previous sample 7755101935 displayed CNY169. Source detail USD structured metadata is inconsistent; displayed product numeric values treated as CNY after sample checks. FX from Frankfurter CNY latest, date shown, unavailable rates fall back to CNY.
- 8 locale detail rendering checks passed, invalid source URL rejected, source agent links cleaned without changing product identity. No third-party referral codes added.
- cnfanshm inspected detail lacks verified independent SKU/style and QC fields. Gallery selectable, item link copy available; no false SKU deep links or QC classification. User's style-specific request remains limited by upstream missing fields.
- Browser-rendered cnfanshm product 6079 checked: raw HTML price159 becomes displayed USD21.90 in source JavaScript; confirms raw price is converted by source, not original USD. Source UI shows four gallery images and no styles/QC selector.

- Reused same-source DINOv2 image descriptors from seo-sites/usfansgrid.com (2026-11-11), verified all 754 freshly read detail galleries against index; current 208 catalogue pages list 6042 records. All 6041 image-bearing products represented, 25648 unique images. Record640 has empty source gallery and ID, excluded. This is an image fingerprint asset, no product database; live result details still cnfanshm. Provenance/limitations public/visual/coverage.json.
- Search uses browser-local DINOv2 ONNX model, matched image SHA256 verifies live source URL before result display and detail navigation.

## Mobile compact revision
Mobile CSS applies to home, catalogue/search/category pages, details, image search and all 8 locales. Keeps20 products/page, two columns with compact object-fit images, two-line card names with complete titles on details, scrollable categories/thumbnails, visible language/currency/buy controls. Target about3–5 screens on catalogue-rich pages, shorter when content is limited; no artificial padding.
