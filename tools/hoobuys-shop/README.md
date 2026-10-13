# Hoobuys Shop editorial build

Run `python tools/hoobuys-shop/build.py`, then `python tools/hoobuys-shop/validate.py`.
The build has no third-party dependencies. Source content lives in `content/`;
the existing deployment continues to serve `hoobuys-shop/` from the GitHub main branch.

## 13 October 2026 release

- Three new guides: finding order QC photos, investigating Process Pending, and
  comparing actual and volumetric shipping weight.
- Four rewritten guides: extra QC requests, spreadsheet tracking, parcel review,
  and print alignment. Existing URLs are retained.
- All seven guides and five navigation/hub pages are authored in English,
  Simplified Chinese, German, French, Spanish, Italian, Polish, Dutch and Portuguese.
  This produces 108 static pages, including 63 article versions.
- Each static language page has its own canonical, reciprocal language links,
  translated navigation and complete body content in the HTML response.
- The 20 other specialist articles retain their original content and existing
  automatic translation. They are all linked in the archive and sitemaps; they
  are not advertised as authored static translations.
- The existing logo, ten product destinations and eight category destinations
  remain. Product search submits to the existing main product site.
- The tracker download is an actual blank, localized CSV with 22 columns. It is
  not a supposedly verified catalogue. The calculator reports illustrative
  weight, not shipping prices or route availability.
- The previous GSC TXT sitemap endpoint remains valid and now includes all
  indexable pages. XML includes the same URLs and language alternates.

## Editorial basis and limits

Public search results and competitor features showed distinct intentions around
QC finding, order progress, cost estimation and spreadsheet tracking. These are
topic hypotheses, not measured search-volume or competitor-ranking estimates.
No new search-volume, fee, refund-policy or delivery-time claims are invented.
The publication addresses discovery and task completion before adding more
similar generic QC checklists. Article FAQs and repetitive boilerplate were not
added. Account-specific conditions must be checked in the live account.

Reference pages examined for topic and implementation research:

- https://pikobuy.to/qc/hoobuy
- https://www.jadeship.com/shipping-calculator/classic/hoobuy
- https://hoobuy-sheet.com/
- https://hoobuyspreadsheet.app/
- https://hoobuy.com/help-center
- https://hoobuy.com/estimation
- https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites
- https://developers.google.com/search/docs/specialty/international/localized-versions
- https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing
- https://developers.google.com/search/docs/fundamentals/creating-helpful-content

Official Hoobuy pages did not expose sufficient readable body content during
research to verify current account procedures or tariffs. Examples are generic
decision guidance. The calculator divisor is explicitly user supplied; 6,000 is
only an illustrative example in the article. No competitor wording is copied.

## Analytics and maintenance

The existing GA4 measurement ID remains `G-X7V92TETF6`. New authored pages record
`guide_click`, `product_index_click`, `product_search`, `tracker_download`,
`shipping_weight_calculation` and `language_switch`. Search terms, private order
IDs, payment details and calculator values are not sent by these custom events.
The older article widget retains its prior event handling.

Use the same completed date window to compare GSC clicks, impressions and pages
with GA4 organic landing sessions and task events. Small initial samples cannot
establish a reliable CTR lift. Google determines indexing and search snippets;
publishing or submitting a sitemap does not guarantee indexing or rankings.

For a later edit, update only genuinely changed pages' editorial date and the
worker/static asset cache version. Validate before committing. The validator
checks all generated links, reciprocal hreflang, self-canonicals, schema,
section availability without JavaScript, CSVs and exact sitemap coverage.
Browser layout QA is skipped when no supported managed-preview browser is
available; deployment checks do not substitute for visual verification.
