from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import json,re,xml.etree.ElementTree as ET
B=Path(__file__).resolve().parent;O=B.parents[1]/'lolobuychina';C=json.loads((B/'content.en.json').read_text());L=['en','de','fr','es','it','pt','ja','ko','zh'];domain='https://lolobuychina.com'
def path(l,r):return ('' if l=='en' else '/'+l)+r
def file(p):return O/(p.lstrip('/')+('index.html' if p.endswith('/') else '.html'))
routes={path(l,r):(l,r) for l in L for r in C};errors=[];soups={r:BeautifulSoup(file(r).read_text(),'html.parser') for r in routes}
for r,(l,base) in routes.items():
 s=soups[r]
 def check(ok,message):
  if not ok:errors.append(r+': '+message)
 check(s.html['lang']==l,'lang');check(len(s.find_all('h1'))==1,'one h1');check(s.find('link',rel='canonical')['href']==domain+r,'canonical')
 alts={x['hreflang']:x['href'] for x in s.find_all('link',rel='alternate')};check(len(alts)==10,'10 alternates');check(alts.get('x-default')==domain+base,'x-default')
 for a in L:check(alts.get(a)==domain+path(a,base),'alternate '+a)
 for a in s.select('.language a'):check(a['href']==path(a['hreflang'],base),'switch loses article')
 check('G-ZCJYW7N8RN' in str(s),'analytics');check(len(s.select('meta[name=description]'))==1,'description')
 check('__' not in s.main.get_text(),'template placeholder');check('▁' not in s.main.get_text(),'tokenizer artifact');check('cnfanshm.com' not in s.get_text(),'visible hub domain')
 for a in s.find_all('a',href=True):
  u=urlsplit(a['href'])
  if not u.netloc:
   target=u.path or r
   check(target in routes,'internal link '+a['href'])
   if u.fragment and target in soups:check(soups[target].find(id=u.fragment) is not None,'fragment '+a['href'])
 for x in s.find_all(['img','script','link']):
  href=x.get('src') or (x.get('href') if 'stylesheet' in x.get('rel',[]) else '')
  if href and href.startswith('/'):check((O/href.lstrip('/')).is_file(),'asset '+href)
 schema=json.loads(s.select_one('script[type="application/ld+json"]').string);check(schema['url']==domain+r and schema['inLanguage']==l,'schema language/url')
 if l!='en' and C[base]['article']:
  check(s.main.get_text()!=soups[base].main.get_text(),'English fallback')
  check(len(s.find_all('h2'))==len(soups[base].find_all('h2')),'section parity')
 for f in s.find_all('form'):check(f.select_one('input[name=keywords]') is not None,'working search field')
 for table in s.find_all('table'):
  check(table.find('tr') is not None,'empty table')
sm=ET.parse(O/'sitemap.xml');urls=[n.text for n in sm.findall('.//{*}loc')];assert len(urls)==len(set(urls))==261;assert set(urls)=={domain+r for r in routes}
for route in ['/articles/lolobuy-link-not-working','/articles/lolobuy-returns-refunds']:
 words=len(soups[route].main.get_text(' ',strip=True).split());assert words>=1200,(route,words)
assert len(soups['/faq'].find_all('details'))>=25
if errors:print('\n'.join(errors));raise SystemExit(f'{len(errors)} validation errors')
print('PASS: 261 pages, 9 languages, 21 articles each, metadata, hreflang, language switches, all internal links/assets, sitemap, complete article sections and new article lengths.')
