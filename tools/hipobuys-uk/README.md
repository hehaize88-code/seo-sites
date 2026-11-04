# HipoBuys UK multilingual editorial build

The reviewed publication inputs are `source.json` (English), `content.<language>.json` (the other seven editions), and `ui.json`. Edit these inputs, not generated HTML. The two original English long-form drafts are retained in `content/en/*.md` for editorial reference; `source.json` is authoritative for the build.

Build from the repository root:

```sh
python -m pip install -r tools/hipobuys-uk/requirements.txt
python tools/hipobuys-uk/build.py
python tools/hipobuys-uk/validate.py
node tools/hipobuys-uk/test-worker.mjs
```

The build writes only `hipobuys-uk/` and the route manifest in this directory. It preserves established English and localized canonical URLs. There are 27 articles, a 24-answer FAQ, a home and an article directory in each of eight languages. The new link-troubleshooting and rehearsal-parcel articles are available in all eight editions. Priority fees and shipping-line guides use edited localized copy.

German legacy routes still redirect to hipobuys.de. The new UK-specific German home is `/de/uk/`; its new guides are served locally, with corresponding hreflang links. Do not restore the old blanket `/de/*` redirect.

The existing GA4 measurement ID and outbound conversion event are preserved. No analytics or search credentials are part of the site. This repository deploys the hipobuys-uk folder through the existing Cloudflare Pages Git integration on main. No new hosting or DNS configuration is required.

Validation covers canonical URLs, sitemap membership, all eight reciprocal language targets, internal links and anchors, required assets, JSON-LD, FAQ/catalogue counts and worker routing. Browser QA also covered desktop rendering, language switching and a 390px-wide embedded viewport.

Keyword priorities for this release: localized Hipobuy fees/costs; UK shipping lines, UK Line B and GB airlines; Hipobuy links not working, Taobao/Weidian/1688 links; rehearsal parcel, volumetric weight and shipping quotes. Labels are not used to invent carrier identities or live prices. Platform facts link to official Hipobuy sources, and import context links to GOV.UK.
