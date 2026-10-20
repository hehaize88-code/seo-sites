# Pikobuy official brand and source pricing observations

Retrieved 2026-10-19. Public assets only; no admin access or external edits.

## Official brand assets

The official public HTML saved at `research/piko.txt` references:

- `logo.png`: https://www.pikobuy.com/images/header/pikobuy-logo-figma.png — HTTP 200 image/png, RGBA, 204 × 48.
- `favicon.png`: https://www.pikobuy.com/images/common/pikobuy-icon-192.png — HTTP 200 image/png, RGBA, 192 × 192.

These files were copied directly from their official URLs without modification. The logo is the Pikobuy wordmark with icon, not a generated substitute.

## Exact cnfanshp price conversion

Evidence: publicly delivered `https://www.cnfanshp.com/template/moban/pc/static/js/script.js?v=2.3.0`, locally `research/script.txt`.

The source itself declares `const CNY_TO_USD_RATE=7.26;` (character offset 163299 in the saved UTF-8 text), then `convertCnyToUsd` (offset 163326):

1. Empty input returns `"0.00"`.
2. If the input string includes `$`, it strips `$` and nonnumeric characters and returns the parsed number with `toFixed(2)` **without further conversion**.
3. Otherwise strip nonnumeric characters, parse as a number, divide by **7.26**, and return `toFixed(2)`.
4. Invalid or empty numeric content returns `"0.00"`.

The hard-coded 7.26 is a source display rate, not a current market-rate estimate. No rate API is used by this conversion function.

Example: source product 6045 has raw price 330; `(330 / 7.26).toFixed(2)` is `45.45`, matching its browser-rendered USD display. Preserve upstream values and derive the rate from the source script on refresh; do not relabel raw CNY as USD or convert an already dollar-denominated string again.

`source-price-conversion.js` preserves the source conversion function with only its obfuscated string lookups decoded. Decoding executed only the isolated string-array/RC4 decoder and array rotation in a no-network Node VM with string code generation disabled. The full downloaded script was never executed. This evidence file is for review, not production imports.
