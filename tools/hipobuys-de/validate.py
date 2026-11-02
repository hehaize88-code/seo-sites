"""Validate multilingual discovery, metadata and retained product destinations."""
import json, re, subprocess
from pathlib import Path
from urllib.parse import urlparse, unquote
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
from config import LANGS, TOPICS, path

ROOT=Path(__file__).resolve().parents[2];SITE=ROOT/'hipobuys-de';BASE='https://hipobuys.de'
def parse(p):return BeautifulSoup(p.read_text(),'html.parser')
def local_file(url):
    p=SITE/unquote(urlparse(url).path).lstrip('/')
    for candidate in [p,p/'index.html',p.with_suffix('.html')]:
        if candidate.is_file():return candidate
    raise AssertionError(f'Missing target: {url}')

urls=[x.text for x in ET.parse(SITE/'sitemap.xml').findall('.//{*}loc')]
assert len(urls)==len(set(urls)), 'Duplicate sitemap URL'
for url in urls:
    s=parse(local_file(url));assert s.select_one('link[rel=canonical]')['href']==url,(url,'sitemap/canonical mismatch')

for lang in LANGS:
    for topic in [None]+TOPICS:
        url=BASE+path(lang,topic);s=parse(local_file(url))
        assert url in urls and s.html['lang']==lang
        assert len(s.select('h1'))==1 and len(s.select('link[rel=canonical]'))==1
        assert s.select_one('link[rel=canonical]')['href']==url
        assert s.title.text and s.select_one('meta[name=description]')['content']
        expected={l:BASE+path(l,topic) for l in LANGS};expected['x-default']=BASE+path('en',topic)
        actual={x['hreflang']:x['href'] for x in s.select('link[rel=alternate][hreflang]')}
        assert actual==expected,(url,'hreflang')
        assert len(s.select('.language-links a'))==8
        assert len(s.select('.language-links a[aria-current=page]'))==1
        assert 'G-Y2VLGD300R' in str(s) and s.select_one('script[src^="/assets/js/main.js"]')
        for a in s.select('a[href^="#"]'):
            assert s.find(id=a['href'][1:]),(url,a['href'])
        for data in s.select('script[type="application/ld+json"]'):
            graph=json.loads(data.string)['@graph'];assert graph[0]['inLanguage']==lang
            assert graph[0]['url']==url
        for tag in s(['style','script']):tag.decompose()
        text=s.get_text(' ',strip=True)
        assert not re.search(r'content model|SEO use|cnfans(?:hp|sp)\.com|\[\[|<a href',text,re.I),url

for p in SITE.rglob('*.html'):
    s=parse(p)
    for a in s.select('a[href]'):
        u=urlparse(a['href'])
        if u.netloc and u.netloc!='hipobuys.de':continue
        if u.path.startswith('/'):local_file(a['href'])

for p in ['index.html','products.html','categories.html']:
    original=subprocess.check_output(['git','show',f'HEAD:hipobuys-de/{p}'],cwd=ROOT,text=True)
    before=BeautifulSoup(original,'html.parser');after=parse(SITE/p)
    def destinations(s):return sorted(a['href'] for a in s.select('a[href]') if '/AllProducts/' in a['href'] or 'utm_campaign=category_lane' in a['href'])
    assert destinations(before)==destinations(after),(p,'product destinations changed')

english=(Path(__file__).parent/'content/en.md').read_text()
for chunk in english.split('@@@ ')[1:]:
    topic,title,desc,body=chunk.strip().split('\n',3)
    if topic in ['safety','links']:assert 1200<=len(body.split())<=1800,(topic,'article length')

print(f'PASS: 64 localized pages, reciprocal hreflang, {len(urls)} canonical sitemap URLs, all internal paths, retained product links and analytics.')
