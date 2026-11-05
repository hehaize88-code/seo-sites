"""Validate indexable routes, translations, structured data and internal navigation."""
import json,re
from pathlib import Path
from urllib.parse import urlsplit,unquote
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from editorial import NEW_ARTICLES, UPDATED
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
articles = json.loads((BASE/'articles.json').read_text())
products = json.loads((BASE/'products.json').read_text())
page_count = 3 + len(articles) + len(NEW_ARTICLES) + len(products)
for lang in LANGS:
 group=[p for p in pages if locale(p)==lang]
 check(len(group)==page_count,f'Page count {lang}: {len(group)}')
 for slug in NEW_ARTICLES:
  article_path=('' if lang=='en' else '/'+lang)+'/guides/'+slug
  page=pages.get(article_path)
  check(page is not None, f'Missing guide {article_path}')
  if page:
   metadata=next(s for s in json.loads(page.select_one('script[type="application/ld+json"]').string) if s.get('@type')=='Article')
   check(metadata['headline']==page.h1.get_text(strip=True) and metadata['inLanguage']==lang and metadata['datePublished']==UPDATED, f'Article metadata {article_path}')
   check(len(page.select('article > h2'))>=5 and len(page.select('article > p'))>=10, f'Incomplete article {article_path}')
   check(any(a.get('href')==article_path for a in pages[('' if lang=='en' else '/'+lang)+'/guides/'].select('a')), f'Missing hub link {article_path}')
 for file in (BASE/'articles/en').glob('*.html'):
  source=BeautifulSoup(file.read_text(),'html.parser')
  target=BeautifulSoup((BASE/'articles'/lang/file.name).read_text(),'html.parser')
  for tag in ['h2','p','li','td','th']:
   check(len(source.find_all(tag))==len(target.find_all(tag)),f'Partial translation {lang} {file.name} {tag}')
check(len(urls)==len(set(urls))==page_count*len(LANGS),'Sitemap count')
print(f'Checked {len(pages)} pages, {len(urls)} sitemap URLs and {(len(articles)+len(NEW_ARTICLES))*len(LANGS)} complete article bodies.')
for e in errors:print(e)
if errors:raise SystemExit(f'{len(errors)} validation errors')
print('PASS')
