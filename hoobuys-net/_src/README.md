# HooBuys.net static editions

Production remains the `hoobuys-net` directory of this GitHub repository. Generated HTML is committed; the hosting build does not need Python or a translation service.

## Edit and build

- Edit the complete English source pages in `en/` and the corresponding strings in each `i18n/<language>.json` file.
- `catalog.json` identifies translated strings by the first 12 hexadecimal characters of their SHA-256 hash. Whitespace at the edges is excluded.
- `pages.json` records the article inventory and source-string membership. It and the catalogue must be refreshed when English text changes. Do not use an English fallback for incomplete translations.
- `inline_translations.json` preserves grammatical agreement at inline boundaries. Keys combine the original preceding-fragment hash and the following inline-text hash. Values override the translated prefix, or specify `prefix` and/or `inline` fields. Empty prefixes intentionally remove English articles already incorporated into the translated noun; formula symbols remain unchanged.
- Run `python _src/build.py` from the site directory with Python 3 and `beautifulsoup4` installed.
- Run `python _src/validate.py` and `node _src/worker.test.mjs` before committing generated pages.

`prepare.py` and `finalize_sources.py` are one-time migration records, not commands to rerun against the prepared sources. `build.py` is the repeatable build. The `_src` directory is blocked by the worker and excluded from the sitemap.

`import_translations.py <directory>` records the initial import of the 21 frozen chunks per language and the coordinated privacy update. Subsequent content editing should use the committed sources and translation dictionaries rather than rerunning that migration over newer edits.

## Coverage and routing

English retains the original root URLs. Complete editions use `/zh-cn/`, `/de/`, `/fr/`, `/es/`, `/it/`, `/pl/`, `/nl/` and `/pt/`. Each of the 35 indexable pages has all nine language alternatives, a self-canonical and an English `x-default`. The 404 page is excluded from the sitemap.

Each article keeps its original subject. The product-spreadsheet guide is separate from the private order ledger. The shipping calculator topic expands the existing `/shipping-guide` rather than adding a competing URL. New guides cover product links, QC photos and Process Pending. Existing articles remain complete.

Analytics retain the existing measurement ID. Custom events record product-link clicks, product search submissions, language changes, worksheet downloads and half-article reading depth. Raw search input is not added to custom events. Receiving events and business results still need to be checked in the property's reports.

Publication is a GitHub commit to the existing production branch; verify the returned commit/check status and the live `X-Hoobuys-Release` header. Search indexing or ranking improvements are not guaranteed by deployment.
