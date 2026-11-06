"""Deployment gate: complete locales, crawlable routes, content parity and metadata."""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
import json,re,collections
B=Path(__file__).resolve().parents[1];M=json.loads((B/'_src/manifest.json').read_text());rows=M['pages'];errors=[];docs={}
for row in rows:
 lang=row['lang'];slug=row['slug'];p=B/('' if lang=='en' else lang)/(slug+'.html');s=BeautifulSoup(p.read_text(),'html.parser');docs[row['url']]=s
 if s.html.get('lang')!=lang:errors.append((p.name,'lang'))
 forms=s.select('form.product-search')
 if len(forms)!=1:errors.append((str(p),'search form count'))
 else:
  f=forms[0];q=f.select_one('input[name="keywords"]');channel=f.select_one('input[name="channelid"]')
  if f.get('action')!='https://www.cnfanssp.com/search.html' or f.get('method')!='get':errors.append((str(p),'search destination'))
  if not q or q.get('type')!='search' or not q.has_attr('required') or not q.get('placeholder'):errors.append((str(p),'search input'))
  if not channel or channel.get('value')!='2':errors.append((str(p),'search channel'))
  if not f.select_one('button[type="submit"]') or not f.select_one('label[for="product-keywords"]'):errors.append((str(p),'search controls'))
  if lang!='en' and f.label.get_text()=='Search products':errors.append((str(p),'untranslated search'))
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
  if v.netloc and v.netloc not in ['hoobuys.org','cnfanssp.com','www.cnfanssp.com','hoobuy.com']:errors.append((row['url'],'external',href));continue
  if v.netloc in ['cnfanssp.com','www.cnfanssp.com','hoobuy.com']:continue
  if v.path in ['/sitemap.xml','/sitemap.txt']:continue
  target='https://hoobuys.org'+v.path if v.path else row['url']
  if target not in docs:errors.append((row['url'],'broken link',href));continue
  if v.fragment and not docs[target].find(id=v.fragment):errors.append((row['url'],'anchor',href))
 for img in s.select('.product-card img'):
  if urlsplit(img['src']).netloc!='cnfanssp.com':errors.append((row['url'],'product image host',img['src']))
 for n in s.select('script[src^="/"],link[rel=stylesheet],img[src^="/"]'):
  url=n.get('src') or n.get('href')
  if not (B/url.lstrip('/')).exists():errors.append((row['url'],'asset',url))
for lang in M['languages']:
 titles=[s.title.get_text() for u,s in docs.items() if s.html.get('lang')==lang]
 if len(set(titles))!=len(titles):errors.append((lang,'duplicate titles'))
source=json.loads((B/'_src/original.json').read_text())
for slug,a in source.items():
 if not a['article'] or slug=='hoobuy-spreadsheet-guide':continue
 text=BeautifulSoup(a['body'],'html.parser').get_text(' ',strip=True)
 new=docs['https://hoobuys.org/'+slug].get_text(' ',strip=True)
 if text not in new:errors.append((slug,'original body not contiguous'))
assert len(rows)==270,len(rows)
assert M['articles_per_language']==23
fresh=['hoobuy-spreadsheet-women','hoobuy-budget-finds','hoobuy-links-not-working']
for slug in fresh+['hoobuy-spreadsheet-guide']:
 en=docs['https://hoobuys.org/'+slug]
 words=len(re.findall(r"\b[\w’'-]+\b",en.select_one('article').get_text(' ',strip=True)))
 if not 1200<=words<=1800:errors.append((slug,'article word count',words))
 for lang in M['languages']:
  url='https://hoobuys.org/'+('' if lang=='en' else lang+'/')+slug
  doc=docs[url]
  if len(doc.select('article h2'))!=len(en.select('article h2')):errors.append((lang,slug,'missing sections'))
  if lang!='en':
   untranslated=[p.get_text(' ',strip=True) for p in doc.select('article p') if p.get_text(' ',strip=True) in [q.get_text(' ',strip=True) for q in en.select('article p')] and len(p.get_text())>85]
   if untranslated:errors.append((lang,slug,'English body fallback',untranslated[:2]))
for lang in M['languages']:
 prefix='https://hoobuys.org/'+('' if lang=='en' else lang+'/')
 catalogue=docs[prefix+'products']
 if len(catalogue.select('.product-card'))!=10:errors.append((lang,'product count'))
 for section in ['clothing','shoes','accessories']:
  if not catalogue.select_one('#'+section):errors.append((lang,'category anchor',section))
 if len(catalogue.select('.nav a'))!=6:errors.append((lang,'navigation count'))
 for slug in fresh:
  if not docs[prefix+'guides'].find('a',href=('/' if lang=='en' else '/'+lang+'/')+slug):errors.append((lang,slug,'missing hub link'))
if errors:
 print(json.dumps(errors,ensure_ascii=False,indent=2));raise SystemExit(1)
print('PASS: 270 indexable pages; 9 languages; 23 complete guides each; 10 reciprocal alternates; 3 new full articles and rewritten spreadsheet; localized search, category anchors, products, links, assets, schema and metadata valid.')
