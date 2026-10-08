# cssbuys.store static publishing

The Cloudflare Pages project publishes `cssbuys-store/` on the repository's existing `main` integration. No Cloudflare dashboard changes are needed.

## Build

Use Python 3 with BeautifulSoup4 installed:

```sh
python tools/cssbuys-store/build.py
python tools/cssbuys-store/validate.py
node tools/cssbuys-store/behavior.test.mjs
```

Production contains eight complete language routes (English at `/`, plus de, fr, es, it, pl, nl and pt). Each has a homepage, guide index, FAQ, 17 full article pages and 10 product reference pages. Language switches retain the corresponding page. The sitemap includes 240 canonical pages. Legacy redirects and intentionally excluded historical pages remain intact.

Edit article fragments in `articles/<language>/`, article metadata and `ui.<language>.json` before building. Seven priority titles and the new article openings have explicit reviewed overrides. Product reference prices are USD values observed on the source catalogue on 2026-10-08, not checkout offers. They exclude shipping and other charges. Product names identify catalogue listings and do not certify authenticity.

## Translation workflow

`translate.py` uses official Argos translation models with CTranslate2 and SentencePiece (or Moses plus subword-nmt for Polish). Install dependencies from `requirements-translation.txt`; download the corresponding official English-to-language models separately. Model binaries and disposable sentence caches are intentionally excluded from git. Generated article fragments and complete UI translations are committed so normal builds require no translation model or network access.

```sh
python tools/cssbuys-store/translate.py --models /path/to/models
```

Models prepare drafts. Review factual statements, negation, numbers, brand names and natural wording before publishing. Keep corrected strings in `translation-overrides.json` so later draft regeneration preserves them. Run `build.py` after translation edits. All seven non-English languages must be updated together when changing source articles.

## Analytics and acceptance checks

The existing GA4 measurement ID is unchanged. `open_main_site` identifies page language, placement and product ID. Search submissions also emit `search` with the query. Navigation has a short bounded fallback if analytics is slow or blocked. The worker skips adding a duplicate script to newly generated pages.

Check live homepage search, a product link, a localized article and language switching after deployment. Confirm sitemap availability and submit it through the site's existing Search Console property. Index requests do not guarantee indexing or rankings.
