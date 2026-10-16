"""Release checks for generated public HTML, links, localization and sitemap."""
import collections, json, re, sys
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'pikobuychina'
LANGS=['en','zh','fr','de','es','it','pl','nl','pt']
pages=json.loads((ROOT/'pages.json').read_text())
source={e['id']:e['text'] for e in json.loads((ROOT/'translation-source.json').read_text())}
errors=[]
def check(test,message):
 if not test:errors.append(message)
def route(slug,lang):return ('/' if lang=='en' else '/'+lang+'/')+slug
known={route(p['slug'],l):p for l in LANGS for p in pages}
docs={}
for lang in LANGS[1:]:
 f=ROOT/'locales'/f'{lang}.json'
 if not f.exists():errors.append('Missing locale '+lang);continue
 d=json.loads(f.read_text())
 check(set(source)<=set(d),'Incomplete dictionary '+lang)
 for k,v in d.items():
  check(isinstance(v,str) and v.strip(),'Empty translation '+lang+' '+k)
  if k in source and len(source[k].split())>8:check(v!=source[k],'Untranslated body '+lang+' '+k)
for lang in LANGS:
 for p in pages:
  path=OUT/('' if lang=='en' else lang)/(p['slug']+'.html' if p['slug'] else 'index.html')
  if not path.exists():errors.append('Missing page '+str(path));continue
  raw=path.read_text();s=BeautifulSoup(raw,'html.parser');r=route(p['slug'],lang);docs[r]=s
  check(raw.lower().startswith('<!doctype html>'),'Doctype '+r)
  check(s.html.get('lang')==('zh-CN' if lang=='zh' else lang),'HTML language '+r)
  check(len(s.select('h1'))==1,'H1 count '+r)
  check(len(s.select('link[rel=canonical]'))==1,'Canonical count '+r)
  check(s.select_one('link[rel=canonical]')['href']=='https://pikobuychina.com'+r,'Canonical target '+r)
  alts=s.select('link[hreflang]');check(len(alts)==10,'Hreflang count '+r)
  expected={'zh-CN' if l=='zh' else l:'https://pikobuychina.com'+route(p['slug'],l) for l in LANGS}
  expected['x-default']='https://pikobuychina.com'+route(p['slug'],'en')
  check({x['hreflang']:x['href'] for x in alts}==expected,'Hreflang targets '+r)
  ids=[x['id'] for x in s.select('[id]')];check(len(set(ids))==len(ids),'Duplicate IDs '+r)
  check(len(s.select('#language option'))==9,'Language switch coverage '+r)
  check(len(s.select('.language-links a'))==9,'Crawlable language links '+r)
  for a in s.select('a[href]'):
   href=a['href'];u=urlsplit(href)
   if href.startswith('#'):check(u.fragment in ids,'Broken fragment '+r+' '+href)
   if href.startswith('/') and not href.startswith('//'):
    if u.path not in ['/sitemap.xml','/sitemap.txt'] and not u.path.startswith('/assets/'):
     check(u.path in known,'Broken page link '+r+' '+href)
  for img in s.select('img[src]'):
   check(bool(img.get('alt')),'Image alt '+r)
   if img['src'].startswith('/assets/'):check((OUT/img['src'][1:]).is_file(),'Image asset '+r)
  for sc in s.select('script[type="application/ld+json"]'):
   data=json.loads(sc.string or sc.get_text());check(data.get('@context')=='https://schema.org','Schema context '+r)
   check(data.get('url')=='https://pikobuychina.com'+r,'Schema URL '+r)
   check(data.get('inLanguage')==s.html['lang'],'Schema language '+r)
  check('G-VLWTW53ETS' in raw,'Analytics configuration '+r)
  check('data:image/' not in raw,'Embedded image payload '+r)
  check('t[fall[l]]' not in raw,'Client English fallback '+r)
  if p['article']:check(not s.main.select('#faq,.faq'),'FAQ residue '+r)
for lang in LANGS:
 hub=docs.get(route('articles',lang));actual={a['href'] for a in hub.select('.card[href]')} if hub else set()
 check(actual=={route(p['slug'],lang) for p in pages if p['article']},'Incomplete article hub '+lang)
titles=collections.Counter(s.title.get_text() for s in docs.values())
check(all(v==1 for v in titles.values()),'Duplicate page titles')
tree=ET.parse(OUT/'sitemap.xml');ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
entries=tree.findall('s:url',ns);urls=[e.find('s:loc',ns).text for e in entries]
check(set(urls)=={'https://pikobuychina.com'+r for r in known},'Sitemap coverage')
check(len(urls)==len(set(urls))==297,'Sitemap URL count')
check(all(len(e.findall('x:link',ns))==10 for e in entries),'Sitemap alternates')
if errors:
 print('\n'.join(errors[:100]));print('FAIL',len(errors));sys.exit(1)
print('PASS: 297 canonical pages; 22 articles × 9 languages; complete dictionaries, hubs, links, metadata, JSON-LD and hreflang.')
