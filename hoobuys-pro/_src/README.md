# hoobuys.pro static source

The deployed output directory is `hoobuys-pro`. Generated HTML, sitemap and assets are committed; the existing GitHub-triggered Pages deployment needs no new build configuration.

## Edit and build

Use Python 3.12+ with `lxml` installed.

```sh
python hoobuys-pro/_src/build.py
python hoobuys-pro/_src/check.py
node hoobuys-pro/_src/check_worker.mjs
```

`content/<language>/<slug>.md` uses a title on the first line, meta description on the second, and HTML body after that. All new articles must exist in en, de, es, fr and it. The generator fails on missing translations. Existing English source articles are in `original/`; their order is in `original-order.json`. Priority English introductions and metadata are updated in `build.py`. Shared localized text is in `ui.json` and `legal.json`. Product records in `products.json` are dated references, not live prices.

Keep equivalent article slugs across languages. English uses root URLs and other languages use locale prefixes. Both page metadata and XML sitemap must retain reciprocal hreflang and self-referencing canonical URLs. Generated files include the existing analytics property and language-aware click events. CSS and analytics files receive content-hash filenames so visitors do not reuse assets from older HTML releases. Keep older hashed assets until cached HTML has expired.

`_worker.js` normalizes old HTML aliases and host variants, protects `_src`, and lets Pages serve extensionless static assets. Tests cover redirect behavior independently of the deployment platform. Verify actual routes on production after publishing.
