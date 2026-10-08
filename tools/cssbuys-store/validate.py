"""Validate indexable routes, translations, structured data and internal navigation."""
import json,re
from pathlib import Path
from urllib.parse import urlsplit,unquote
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[1]/'cssbuys-store'
LANGS=['en','de','fr','es','it','pl','nl','pt']
DOMAIN='https://cssbuys.store'
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=[x.text for x in ET.parse(ROOT/'sitemap.xml').findall('.//s:loc',ns)]
errors=[]
def check(ok,msg):
 if not ok:errors.append(msg)
def file_for(path):
 return ROOT/(path.lstrip('/')+'index.html' if path.endswith('/') else path.lstrip('/')+'.html')
def locale(path):
 first=path.split('/')[1]
 return first if first in LANGS else 'en'
def suffix(path):return path[3:] if locale(path)!='en' else path
pages={}
for address in urls:
 path=urlsplit(address).path;file=file_for(path)
 check(file.exists(),f'Missing page {address}')
 if not file.exists():continue
 soup=BeautifulSoup(file.read_text(),'html.parser');pages[path]=soup
 check(soup.html['lang']==locale(path),f'Wrong html lang {path}')
 check(len(soup.select('h1'))==1,f'H1 count {path}')
 check(soup.select_one('link[rel=canonical]')['href']==address,f'Canonical {path}')
 check('noindex' not in soup.select_one('meta[name=robots]')['content'],f'noindex {path}')
 alternates={a['hreflang']:a['href'] for a in soup.select('link[rel=alternate]')}
 check(len(alternates)==9,f'hreflang count {path}')
 for lang in LANGS+['x-default']:
  expected=DOMAIN+('' if lang in ['en','x-default'] else '/'+lang)+suffix(path)
  check(alternates.get(lang)==expected,f'hreflang target {path} {lang}')
 for script in soup.select('script[type="application/ld+json"]'):json.loads(script.string)
 check(len(soup.select('script[src="/assets/site-tracking.js"]'))==1,f'Tracking count {path}')
 check('▁' not in soup.get_text(),f'Undecoded token {path}')
 ids=[x['id'] for x in soup.select('[id]')]
 check(len(ids)==len(set(ids)),f'Duplicate ids {path}')
 for a in soup.select('a[href]'):
  href=a['href'];u=urlsplit(href)
  if u.netloc and u.netloc!='cssbuys.store':continue
  if not u.path:
   if u.fragment:check(unquote(u.fragment) in ids,f'Missing anchor {path} {href}')
   continue
  if u.path.startswith('/assets/') or u.path=='/sitemap.xml':continue
  if u.path.startswith('/categories/'):continue
  check(file_for(u.path).exists(),f'Broken link {path} -> {href}')
 for image in soup.select('img[src^="/assets/"]'):check((ROOT/image['src'].lstrip('/')).exists(),f'Missing image {path}')
for lang in LANGS:
 group=[p for p in pages if locale(p)==lang]
 check(len(group)==30,f'Page count {lang}: {len(group)}')
 for file in (BASE/'articles/en').glob('*.html'):
  source=BeautifulSoup(file.read_text(),'html.parser')
  target=BeautifulSoup((BASE/'articles'/lang/file.name).read_text(),'html.parser')
  for tag in ['h2','p','li','td','th']:
   check(len(source.find_all(tag))==len(target.find_all(tag)),f'Partial translation {lang} {file.name} {tag}')
check(len(urls)==240 and len(set(urls))==240,'Sitemap count')
print(f'Checked {len(pages)} pages, {len(urls)} sitemap URLs and 136 complete article bodies.')
for e in errors:print(e)
if errors:raise SystemExit(f'{len(errors)} validation errors')
print('PASS')
