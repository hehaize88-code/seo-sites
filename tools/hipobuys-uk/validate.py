"""Validate publication routes, locale alternates, structured data and local links."""
import json,re,sys
from pathlib import Path
from urllib.parse import urljoin,urlsplit,unquote
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
BASE=Path(__file__).resolve().parent;SITE=BASE.parents[1]/'hipobuys-uk';ORIGIN='https://hipobuys.uk'
R=json.loads((BASE/'routes.json').read_text());UI=json.loads((BASE/'ui.json').read_text()); errors=[];cache={}
def file(path):
 p=SITE/path.lstrip('/')
 return p/'index.html' if path.endswith('/') else p if p.is_file() else Path(str(p)+'.html') if Path(str(p)+'.html').is_file() else p/'index.html'
def soup(path):
 if path not in cache: cache[path]=BeautifulSoup(file(path).read_text(),'html.parser')
 return cache[path]
def check(ok,msg):
 if not ok:errors.append(msg)
for lang, routes in R.items():
 check(len(routes)==30,f'{lang}: missing entries')
 for key,path in routes.items():
  if not file(path).is_file():errors.append(f'Missing {path}');continue
  s=soup(path);can=s.select_one('link[rel=canonical]');check(can and can.get('href')==ORIGIN+path,f'Canonical {path}')
  check(s.html.get('lang')==UI[lang]['lang'],f'lang {path}')
  alts={a['hreflang']:a['href'] for a in s.select('link[hreflang]')}
  check(len(alts)==9,f'alternates {path}')
  for other in R:check(alts.get(UI[other]['lang'])==ORIGIN+R[other][key],f'alternate {path} {other}')
  check(alts.get('x-default')==ORIGIN+R['en'][key],f'xdefault {path}')
  check(len(s.select('h1'))==1,f'h1 {path}')
  check('▁' not in s.get_text(),f'token artifact {path}')
  check('G-GYK9GRD9N8' in str(s),f'GA tag {path}')
  for ld in s.select('script[type="application/ld+json"]'):
   try: json.loads(ld.string or ld.get_text())
   except Exception as e:errors.append(f'JSONLD {path}: {e}')
  if key=='faq':
   check(len(s.select('.article > h2'))>=24,f'FAQ count {path}')
  if key=='index':check(len(s.select('.cards .card'))==27,f'catalogue {path}')
  for el in s.select('a[href],script[src],link[href],img[src]'):
   href=el.get('href',el.get('src'));u=urlsplit(urljoin(ORIGIN+path,href))
   if u.scheme not in ['http','https'] or u.netloc!='hipobuys.uk':continue
   if not file(unquote(u.path)).is_file():errors.append(f'Broken {path} => {href}');continue
   if el.name=='a' and u.fragment and not soup(unquote(u.path)).find(id=unquote(u.fragment)):errors.append(f'Fragment {path} => {href}')
urls=[x.text for x in ET.parse(SITE/'sitemap.xml').findall('{*}url/{*}loc')]
check(len(urls)==len(set(urls)),'duplicate sitemap')
for u in urls:
 p=urlsplit(u).path
 check(file(p).is_file(),f'sitemap missing {p}')
 if file(p).is_file():
  c=soup(p).select_one('link[rel=canonical]');check(c and c.get('href')==u,f'sitemap canonical {p}')
for p in ['/languages']:
 s=soup(p);check(s.select_one('meta[property="og:url"]')['content']==ORIGIN+p,'language directory OG')
for e in sorted(set(errors)):print(e)
print(f'{len(R)} languages; {sum(map(len,R.values()))} localized pages; {len(urls)} sitemap URLs; {len(set(errors))} errors')
sys.exit(bool(errors))
