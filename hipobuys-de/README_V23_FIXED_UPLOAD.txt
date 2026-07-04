HipoBuys.de V23 fixed multilang upload

Fix:
- Root pages no longer depend on missing /assets/css/style.css.
- CSS is embedded directly into root-level HTML pages.
- Multilingual /en /de /fr /es /it /pl /pt /nl pages are retained.
- sitemap.xml and robots.txt are retained.

Deploy:
Upload the contents of this folder to Cloudflare Pages project hipobuys-de.
Root must directly contain index.html, languages.html, sitemap.xml, robots.txt and language folders.
