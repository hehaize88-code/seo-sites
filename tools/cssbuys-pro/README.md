# CSSBuys.pro content maintenance

This directory updates only `cssbuys-pro/`, the existing Cloudflare Pages output directory.
Install Python `beautifulsoup4` if unavailable, then run from the repository root:

```sh
python tools/cssbuys-pro/build.py
python tools/cssbuys-pro/validate.py
node tools/cssbuys-pro/check-runtime.mjs
```

`content/` contains complete six-language article bodies; `editorial/` contains
verified metadata, FAQ answers, source notes and exact legacy editorial corrections.
`ui.py` contains the six-language shared interface. Update the release date and asset
versions when making substantive changes. Never replace translation text with English.

The local weight planner uses user-provided line rules, not live CSSBuy shipping
prices. The budget worksheet uses user-entered CNY costs. Neither sends user-entered
measurements or costs to a server. Existing GA4 destination/search event names are
preserved; calculator events record only the page language. The edge worker must not
inject a second analytics click handler.

Publish through the existing `main` branch / Cloudflare Pages integration with
output directory `cssbuys-pro`. Confirm the live assets, new URLs, sitemap and
404 status after deployment. The generator does not submit indexing requests.
