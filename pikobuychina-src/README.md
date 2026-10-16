# PikoBuyChina static source

Production output is `../pikobuychina/`. The existing Git integration deploys that directory from `main`; no build command or hosting-account change is required.

`pages.json` contains the English page copy and stable routes. `locales/{lang}.json` contains complete keyed text translations. `translation-source.json` is the translation inventory. `seo-titles.json` holds concise, reviewed search titles. Shared rendering, canonical tags, reciprocal hreflang, structured data, language links and sitemaps are produced by `build.py`.

To regenerate with Python and Beautiful Soup installed:

```sh
python pikobuychina-src/build.py
python pikobuychina-src/validate.py
```

The normal build requires all eight translation dictionaries. It fails on missing strings instead of accepting an English fallback. `--english-only` is a local development option, not a publishable release. Commit the generated output with the corresponding source changes.

The English routes are preserved. Other languages use `/zh/`, `/fr/`, `/de/`, `/es/`, `/it/`, `/pl/`, `/nl/` and `/pt/`. The existing Worker only normalizes legacy URLs and headers; it does not inject or translate page content.

The release contains 33 canonical pages per language, including 22 article detail pages. Three new guides cover image search, Taobao/Weidian link troubleshooting and shoe sizing with QC measurements. Product catalog links and retained images remain from the existing site; displayed USD values are marked as reference prices.

Keep policy claims qualified and linked to official sources. Do not add invented coupon codes, guaranteed transit times, fixed shipping rates, authenticity claims or unverified product images. When editing a source string, refresh the inventory and provide all translations before building.

The site retains its GA4 measurement ID and article, catalog and product-click events. Search submission records the destination, not arbitrary visitor-entered text.
