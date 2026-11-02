from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import json,re,xml.etree.ElementTree as ET
from config import LANGS,HREFLANG,SLUGS
ROOT=Path(__file__).resolve().parents[2]/'cssbuys-de'
HOST='https://cssbuys.de'
NEW=['cssbuy-tyg-eu-tariffless-express','cssbuy-rehearsal-shipping','cssbuy-hoodies-jackets-spreadsheet']
def target(path):
    path=urlsplit(path).path
    if path.endswith('/'):return ROOT/path.lstrip('/')/'index.html'
    p=ROOT/path.lstrip('/')
    return p if p.suffix else p.with_suffix('.html')
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=[x.text for x in ET.parse(ROOT/'sitemap.xml').findall('.//s:loc',ns)]
errors=[];counts={};cache={}
def check(ok,msg):
    if not ok:errors.append(msg)
def load(path):
    if path not in cache:cache[path]=BeautifulSoup(path.read_text(),'html.parser')
    return cache[path]
check(len(urls)==156 and len(set(urls))==156,'Sitemap must have 156 unique URLs')
for url in urls:
    p=target(url);check(p.exists(),f'Missing sitemap target: {url}')
    if not p.exists():continue
    s=load(p);check(len(s.select('h1'))==1,f'H1: {url}')
    cs=s.select('link[rel="canonical"]');check(len(cs)==1 and cs[0]['href']==url,f'Canonical: {url}')
    robots=s.find('meta',attrs={'name':'robots'});check(not robots or 'noindex' not in robots.get('content',''),f'Noindex: {url}')
    for script in s.select('script[type="application/ld+json"]'):
        try:json.loads(script.get_text())
        except ValueError:errors.append(f'Invalid JSON-LD: {url}')
    for a in s.select('a[href]'):
        href=a['href'];parts=urlsplit(href)
        if parts.netloc and parts.netloc!='cssbuys.de':continue
        if parts.scheme and parts.scheme not in ['https','http']:continue
        if href.startswith('#'):
            if parts.fragment:check(bool(s.find(id=parts.fragment)),f'Missing anchor {url} {href}')
        elif href.startswith('/') or parts.netloc=='cssbuys.de':
            t=target(href);check(t.exists(),f'Broken link {url} -> {href}')
            if t.exists() and parts.fragment:check(bool(load(t).find(id=parts.fragment)),f'Broken cross-page anchor {url} -> {href}')
for lang in LANGS:
    pre='' if lang=='en' else '/'+lang
    hub=load(target(pre+'/guides/'));home=load(target(pre+'/'))
    check(len(hub.select('.guide-card'))==22,f'Hub count: {lang}')
    check(len(home.select('.latest-guides .guide-card'))==6,f'Homepage count: {lang}')
    check(home.select_one('.footer .language-links a')['href']=='/',f'English switch: {lang}')
    for slug in NEW+SLUGS:
        url=HOST+pre+'/guides/'+slug;s=load(target(url));a=s.select_one('article')
        check(s.html.get('lang')==HREFLANG[lang],f'Language: {url}')
        alt={x['hreflang']:x['href'] for x in s.select('link[hreflang]')}
        expected={HREFLANG[l]:HOST+(''if l=='en'else '/'+l)+'/guides/'+slug for l in LANGS};expected['x-default']=HOST+'/guides/'+slug
        check(alt==expected,f'Alternate cluster: {url}')
        ids=[x['id'] for x in a.select('[id]')];check(len(ids)==len(set(ids)),f'Duplicate IDs: {url}')
        for h in a.select('h2'):check(len(h.get_text())<140 and '\n' not in h.get_text(),f'Malformed heading: {url}')
        text=a.get_text(' ',strip=True)
        check('[[' not in text and not re.search(r'\]\(https?://',text),f'Unrendered links: {url}')
        if slug in NEW:
            count=len(a.get_text(' ',strip=True).split());counts[lang+'/'+slug]=count
            check(count>=600,f'Thin new article: {url}: {count}')
            if lang=='en':check(1200<=count<=1800,f'English article length: {url}: {count}')
        if lang=='en':
            for phrase in ['keyword cannibalization','Do not hide content on mobile','Keep title and description in the document head','better SEO content']:
                check(phrase not in text,f'Editorial pollution: {url}: {phrase}')
if errors:
    print('\n'.join(errors));raise SystemExit(1)
print(f'PASS: {len(urls)} canonical/indexable sitemap URLs; local links and anchors; 6 × 22 guides; 6 × 6 homepage cards; 60 refreshed/new multilingual guide alternates and structured data.')
print('New article word counts:',json.dumps(counts,ensure_ascii=False))
