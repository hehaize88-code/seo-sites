#!/usr/bin/env python3
"""Check the published static directory, including locale parity and local destinations."""
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse, unquote
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from ui import LANGS, DOMAIN

ROOT = Path(__file__).resolve().parents[2] / 'cssbuys-pro'
errors = []
def check(ok, message):
    if not ok: errors.append(message)
def resolve(path):
    p = ROOT / unquote(path).lstrip('/')
    if p.is_dir(): return p / 'index.html'
    if p.is_file(): return p
    return p.with_suffix('.html') if not p.suffix else p

pages = {p: BeautifulSoup(p.read_text(), 'html.parser') for p in ROOT.rglob('*.html')}
canonicals = {}
for p, s in pages.items():
    rel = str(p.relative_to(ROOT))
    if rel == 'guides.html' or 'categories/' in rel or p.name == '404.html': continue
    lang = s.html.get('lang')
    check(lang in LANGS, f'{rel}: unexpected lang {lang}')
    cs = s.select('link[rel="canonical"]')
    check(len(cs) == 1, f'{rel}: canonical count')
    if not cs: continue
    canonical = cs[0]['href']
    check(canonical not in canonicals, f'{rel}: duplicate canonical {canonical}')
    canonicals[canonical] = p
    check(resolve(urlparse(canonical).path) == p, f'{rel}: canonical does not resolve to self')
    check(len(s.find_all('h1')) == 1, f'{rel}: H1 count')
    check(bool(s.title and s.title.get_text(strip=True)), f'{rel}: missing title')
    check(bool(s.find('meta', attrs={'name':'description'})), f'{rel}: description')
    ids = [x['id'] for x in s.select('[id]')]
    check(not [k for k,v in Counter(ids).items() if v>1], f'{rel}: duplicate IDs')
    alts = {a['hreflang']:a['href'] for a in s.select('link[rel="alternate"][hreflang]')}
    check(set(alts) == set(LANGS)|{'x-default'}, f'{rel}: hreflang set')
    for key,href in alts.items():
        target = resolve(urlparse(href).path)
        check(target in pages, f'{rel}: missing alternate {href}')
        if target in pages:
            backs = {x['hreflang']:x['href'] for x in pages[target].select('link[rel="alternate"][hreflang]')}
            check(backs.get(lang)==canonical, f'{rel}: non-reciprocal alternate {key}')
    for el in s.select('script[type="application/ld+json"]'):
        try: json.loads(el.string or el.get_text())
        except Exception as exc: errors.append(f'{rel}: invalid JSON-LD {exc}')
    if '/products/' not in canonical and not canonical.endswith('/languages'):
        check(len(s.select('script[src*="site-events.js"]'))==1, f'{rel}: analytics script count')
        check('G-VWHN1W22CP' in str(s), f'{rel}: GA tag changed/missing')
    for el in s.select('a[href],link[href],script[src],img[src]'):
        href = el.get('href', el.get('src', ''))
        url = urlparse(href)
        if url.scheme and url.scheme not in ('http','https'): continue
        if url.netloc and url.netloc != 'cssbuys.pro': continue
        if not url.path: target=p
        elif url.path.startswith('/'): target=resolve(url.path)
        else: target=resolve(str((p.parent/url.path).relative_to(ROOT)))
        check(target.exists(), f'{rel}: broken local destination {href}')
        if url.fragment and target in pages:
            check(bool(pages[target].find(id=unquote(url.fragment))), f'{rel}: missing fragment {href}')

for lang in LANGS:
    folder=ROOT / ('' if lang=='en' else lang)
    guides=list((folder/'guides').glob('*.html'))
    check(len(guides)==26, f'{lang}: expected 25 guides + hub, got {len(guides)}')
    hub=pages[folder/'guides/index.html']
    check(len(hub.select('.guide-card'))==25, f'{lang}: hub card count')
    check(len(pages[folder/'faq.html'].select('.faq-card'))==28, f'{lang}: FAQ count')
    for slug in ['cssbuy-returns-refunds','cssbuy-shipping-deposit-final-cost','cssbuy-warehouse-storage-deadlines']:
        article=pages[folder/f'guides/{slug}.html'].article
        count=len(article.get_text(' ',strip=True).split())
        check(count>=1200 if lang!='zh' else len(article.get_text())>2500, f'{lang}/{slug}: incomplete body ({count} words)')

sm=ET.parse(ROOT/'sitemap.xml'); ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=[x.text for x in sm.findall('s:url/s:loc',ns)]
check(len(urls)==len(set(urls))==234, f'sitemap count {len(urls)}, expected 234')
check(set(urls)==set(canonicals), 'sitemap differs from canonical page set')
check('ANALYTICS_SCRIPT' not in (ROOT/'_worker.js').read_text(), 'old injected tracker remains')
if errors:
    print('\n'.join(errors)); raise SystemExit(f'FAILED: {len(errors)} checks')
print(f'PASS: {len(pages)} HTML files, {len(urls)} canonical URLs, 150 guides, six-language parity, links, hreflang, schema, FAQ and tracking.')
