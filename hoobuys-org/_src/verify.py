"""Deployment gate: complete locales, crawlable routes, content parity and metadata."""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import json,re,collections
B=Path(__file__).resolve().parents[1];M=json.loads((B/'_src/manifest.json').read_text());rows=M['pages'];errors=[];docs={}
for row in rows:
 lang=row['lang'];slug=row['slug'];p=B/('' if lang=='en' else lang)/(slug+'.html');s=BeautifulSoup(p.read_text(),'html.parser');docs[row['url']]=s
 if s.html.get('lang')!=lang:errors.append((p.name,'lang'))
 if len(s.select('h1'))!=1:errors.append((str(p),'h1 count',len(s.select('h1'))))
 if s.select_one('link[rel=canonical]')['href']!=row['url']:errors.append((p.name,'canonical'))
 alts=s.select('link[rel=alternate][hreflang]')
 if len(alts)!=10 or {a['hreflang'] for a in alts}!=set(M['languages']+['x-default']):errors.append((p.name,'alternates'))
 if not s.title.get_text().strip() or not s.select_one('meta[name=description]')['content']:errors.append((p.name,'empty metadata'))
 if 'G-Q60K7ELE45' not in str(s) or 'translate.google' in str(s):errors.append((p.name,'script'))
 if '▁' in str(s):errors.append((p.name,'tokenizer artifact'))
 for script in s.select('script[type="application/ld+json"]'):
  j=json.loads(script.string)
  for a in j['@graph']:
   if a.get('@type')=='Article' and (a.get('inLanguage')!=lang or a.get('headline')!=s.title.get_text()):errors.append((p.name,'Article schema'))
 en=BeautifulSoup((B/(slug+'.html')).read_text(),'html.parser')
 for tag in ['h2','h3','p','table','tr','li']:
  if len(s.select('main '+tag))!=len(en.select('main '+tag)):errors.append((p.name,lang,'structure',tag))
for row in rows:
 s=docs[row['url']]
 for a in s.select('a[href],link[rel=alternate]'):
  href=a.get('href');v=urlsplit(href)
  if v.netloc and v.netloc not in ['hoobuys.org','cnfanshp.com']:errors.append((row['url'],'external',href));continue
  if v.netloc=='cnfanshp.com':continue
  if v.path in ['/sitemap.xml','/sitemap.txt']:continue
  target='https://hoobuys.org'+v.path if v.path else row['url']
  if target not in docs:errors.append((row['url'],'broken link',href));continue
  if v.fragment and not docs[target].find(id=v.fragment):errors.append((row['url'],'anchor',href))
 for n in s.select('script[src^="/"],link[rel=stylesheet],img[src^="/"]'):
  url=n.get('src') or n.get('href')
  if not (B/url.lstrip('/')).exists():errors.append((row['url'],'asset',url))
for lang in M['languages']:
 titles=[s.title.get_text() for u,s in docs.items() if s.html.get('lang')==lang]
 if len(set(titles))!=len(titles):errors.append((lang,'duplicate titles'))
source=json.loads((B/'_src/original.json').read_text())
for slug,a in source.items():
 if not a['article']:continue
 text=BeautifulSoup(a['body'],'html.parser').get_text(' ',strip=True)
 new=docs['https://hoobuys.org/'+slug].get_text(' ',strip=True)
 if text not in new:errors.append((slug,'original body not contiguous'))
assert len(rows)==243,len(rows)
assert M['articles_per_language']==20
if errors:
 print(json.dumps(errors,ensure_ascii=False,indent=2));raise SystemExit(1)
print('PASS: 243 indexable pages; 9 languages; 20 complete guides each; 10 reciprocal alternates; original article bodies retained; links, assets, schema and metadata valid.')
