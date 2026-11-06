# Hoobuys Shop editorial build

Run `python tools/hoobuys-shop/build.py`, then `python tools/hoobuys-shop/validate.py`.
The build has no third-party dependencies. Source content lives in `content/`;
the existing deployment continues to serve `hoobuys-shop/` from the GitHub main branch.

## 6 November 2026 release

- Added three complete guides: delivery stages and tracking delays, product-link
  troubleshooting, and shipping quote comparisons for Germany. English versions
  contain 1,294–1,343 words including section headings and introduction.
- Published all three in the existing nine locales: 27 new static article pages.
  All seven existing core guides receive a practical decision section and new
  relevant internal links. Their existing URLs and original publication dates
  are retained where known.
- Home, article index, navigation and metadata now expose the new topics.
  Added a direct QC navigation entry and expanded the FAQ to 20 questions in
  every locale, with matching FAQPage data on the FAQ page.
- The authored static set now contains 135 pages, including 90 article versions;
  XML and TXT sitemaps contain 157 URLs. The 20 original archive articles are
  retained with their existing translation widget; this release does not claim
  that the entire archive has authored static translations.
- New translation output was reviewed for headings, QC terminology, numerical
  examples and paragraph parity. Chinese additions and new articles were edited
  manually after translation. Existing translations were preserved elsewhere.
- New official references: Hoobuy beginner guide, estimator and Help Center;
  Germany article also links to German customs postal declaration guidance.
  The 50/12 CNY tariff is explicitly fictional, used only to explain billing
  increments. No actual Germany rate, guaranteed delivery time or tax allowance
  is asserted. Neither product destinations nor analytics identifiers change.

Research resumed from the earlier report prioritising Spreadsheet, QC, delivery
time, broken links and Germany quotes. Public official sources were rechecked.
GSC Wizard refused fresh reads because its account has no active subscription;
this release does not present earlier analytics as newly verified data. The
Cloudflare API connector requested reauthentication; publication uses the
existing GitHub main-branch Pages integration instead.

References checked 6 November 2026:

- https://hoobuy.com/beginner-guide?stepKey=Custom1
- https://hoobuy.com/estimation
- https://hoobuy.com/m/help-center
- https://www.help.zoll-portal.de/EN/Help/Services/customs-declaration-for-postal-consignments/customs-declaration-for-postal-consignments.html
- Competitor intent checks: https://hoobuyspreadsheets.org/ and https://hoobuy.me/

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
