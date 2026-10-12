"""Validate generated multilingual navigation and SEO invariants before publishing."""
from pathlib import Path
from urllib.parse import urlsplit
from collections import Counter
from lxml import html, etree
import json
B=Path(__file__).resolve().parents[1]
m=json.loads((B/'_src/manifest.json').read_text()); pages=m['pages']; langs=m['languages']; docs={}; titles=[]
for p in pages:
 f=B/(p['lang'] if p['lang']!='en' else '')/((p['slug']+'.html') if p['slug'] else 'index.html')
 d=html.parse(str(f)); docs[urlsplit(p['url']).path]=d; titles+=d.xpath('//title/text()')
 assert d.xpath('/html/@lang')==[p['lang']],f
 assert d.xpath('//link[@rel="canonical"]/@href')==[p['url']],f
 assert len(d.xpath('//h1'))==1,f
 assert len(d.xpath('//meta[@name="description"]/@content')[0])>30,f
 assert 'noindex' not in d.xpath('//meta[@name="robots"]/@content')[0],f
 alt={a.get('hreflang'):a.get('href') for a in d.xpath('//link[@rel="alternate"]')}
 assert set(alt)==set(langs+['x-default']),f
 for l in langs+['x-default']:
  expected='https://hoobuys.pro'+('/' if l in ['en','x-default'] else '/'+l+'/')+p['slug']
  assert alt[l]==expected,(f,l)
 for ld in d.xpath('//script[@type="application/ld+json"]/text()'):json.loads(ld)
 assert 'G-KG6V0Z9TWS' in f.read_text(),f
assert len(titles)==len(set(titles)),[x for x,n in Counter(titles).items() if n>1]
for path,d in docs.items():
 lang=d.xpath('/html/@lang')[0]
 for a in d.xpath('//a[@href]'):
  u=urlsplit(a.get('href'))
  if u.scheme or u.netloc:continue
  target=u.path or path
  if target=='/sitemap.xml':continue
  assert target in docs,(path,a.get('href'))
  if u.fragment:assert docs[target].xpath('//*[@id=$id]',id=u.fragment),(path,a.get('href'))
  if not a.get('hreflang'):assert docs[target].xpath('/html/@lang')==[lang],(path,a.get('href'),'cross-language')
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
sitemap=etree.parse(str(B/'sitemap.xml'))
assert set(sitemap.xpath('//s:loc/text()',namespaces=ns))=={p['url'] for p in pages}
assert len(sitemap.xpath('//x:link',namespaces=ns))==len(pages)*6
assert len(pages)==145 and Counter(p['lang'] for p in pages)=={l:29 for l in langs}
assert all(len(docs[('/' if l=='en' else '/'+l+'/')+'guides'].xpath('//a[contains(@class,"article-card")]'))==23 for l in langs)
print('PASS: 145 pages; 5 complete languages; unique titles; canonical/hreflang; sitemap; JSON-LD; internal links and anchors; analytics tag.')
