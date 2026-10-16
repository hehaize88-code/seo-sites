"""Build all static language routes. Requires beautifulsoup4; no runtime translation."""
import argparse, hashlib, html, json, re
from pathlib import Path
from xml.sax.saxutils import escape as xe
from bs4 import BeautifulSoup, NavigableString, Comment, Doctype
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'pikobuychina'
DOMAIN='https://pikobuychina.com'
LANGS={'en':'English','zh':'中文','fr':'Français','de':'Deutsch','es':'Español','it':'Italiano','pl':'Polski','nl':'Nederlands','pt':'Português'}
DATE='2026-10-16'
pages=json.loads((ROOT/'pages.json').read_text())
seo_titles=json.loads((ROOT/'seo-titles.json').read_text())
E=html.escape
def url(slug,lang='en'):
 return ('/' if lang=='en' else '/'+lang+'/')+slug
def key(t):return hashlib.sha256(t.encode()).hexdigest()[:12]
def shell(p):
 nav=[('','Home'),('finds','Finds'),('categories','Categories'),('w2c','W2C'),('qc','QC'),('shipping','Shipping'),('coupons','Coupons'),('articles','Articles')]
 header='<a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="brand" href="/"><img src="/assets/123.png" alt="PikobuyChina" width="220" height="47"></a><details class="menu" open><summary>Menu</summary><nav aria-label="Main navigation">'+''.join('<a href="/'+s+'">'+t+'</a>' for s,t in nav)+'</nav></details><label class="language"><span>Language</span><select id="language" aria-label="Language"></select></label></div></header>'
 intro=('<p class="lead">'+E(p['intro'])+'</p>') if p['intro'] else ''
 hero='' if p['slug']=='' else '<header class="page-hero"><p class="eyebrow">INDEPENDENT BUYER GUIDES</p><h1>'+E(p['title'])+'</h1>'+intro+'</header>'
 body=p['body']
 if p['article']:
  b=BeautifulSoup(body,'html.parser')
  for i,h in enumerate(b.select('h2'),1):
   if not h.get('id'):h['id']='section-'+str(i)
  toc='<details class="contents"><summary>In this guide</summary><ol>'+''.join('<li><a href="#'+h['id']+'">'+E(h.get_text(' ',strip=True))+'</a></li>' for h in b.select('h2'))+'</ol></details>'
  related=['guides/pikobuy-image-search-product-finder-2026','guides/pikobuy-link-not-working-weidian-taobao-2026','guides/pikobuy-shoe-size-guide-qc-measurements-2026','articles/pikobuy-qc-photo-checklist-2026','articles/pikobuy-spreadsheet-2026-guide']
  if any(t in p['slug'] for t in ['cost','fees','conversion','weight','reinforcement']):
   related=['articles/pikobuy-shipping-cost-coupons-2026','guides/pikobuy-actual-vs-volumetric-weight-billable-cost-2026','guides/pikobuy-total-landed-cost-worksheet-2026','guides/pikobuy-service-payment-fees-audit-2026','guides/pikobuy-shipping-line-comparison-framework-2026']
  elif any(t in p['slug'] for t in ['tracking','domestic','how-long','submit','restricted','canada','shipping-line']):
   related=['guides/pikobuy-tracking-order-status-guide-2026','guides/how-long-does-pikobuy-take-2026','guides/how-to-submit-pikobuy-parcel-2026','guides/pikobuy-restricted-goods-route-availability-2026','guides/pikobuy-shipping-line-comparison-framework-2026']
  related=[s for s in related if s!=p['slug']]
  rel='<section class="related"><h2>Continue with the next decision</h2><ul>'+''.join('<li><a href="/'+q['slug']+'">'+E(q['title'])+'</a></li>' for s in related for q in pages if q['slug']==s)+'</ul></section>'
  sources='<section class="sources"><h2>Sources and live checks</h2><p>Independent guidance based on the public platform workflow. Check the current listing, account and route terms before payment; availability, fees and policies can change.</p><ul><li><a href="https://www.pikobuy.com/home" target="_blank" rel="noopener">PikoBuy product search and sourcing</a></li><li><a href="https://www.pikobuy.com/guide" target="_blank" rel="noopener">Official beginner workflow</a></li><li><a href="https://www.pikobuy.com/shipping-cost" target="_blank" rel="noopener">Official shipping estimator</a></li><li><a href="https://www.pikobuy.com/protocol/shipping" target="_blank" rel="noopener">Shipping terms</a></li><li><a href="https://www.pikobuy.com/protocol/returns" target="_blank" rel="noopener">Return and exchange terms</a></li></ul></section>'
  hero='<div class="breadcrumbs"><a href="/">Home</a> / <a href="/articles">Articles</a></div>'+hero
  body='<div class="article-meta"><span>Updated</span> <time datetime="'+DATE+'">'+DATE+'</time><span> · PikobuyChina</span></div>'+toc+'<article class="prose">'+str(b)+rel+sources+'</article>'
 footer='<footer><div class="footer-inner"><div><strong class="notranslate">PikobuyChina</strong><p>Independent buying, QC, shipping and tracking guidance. This site is not owned by or affiliated with PikoBuy.</p></div><div class="footer-links"><a href="/guides">Guides by stage</a><a href="/faq">Buyer glossary</a><a href="/seo-guide">Buying workflow</a><a href="/sitemap.xml">Sitemap</a></div></div></footer>'
 return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+E(p['title'])+'</title><meta name="description" content="'+E(p['description'])+'"><meta name="robots" content="index,follow"><link rel="stylesheet" href="/assets/site.css?v=20261016"><meta name="theme-color" content="#142f2b"></head><body>'+header+'<main id="main" class="'+('article-page' if p['article'] else 'site-main')+'">'+hero+body+'</main>'+footer+'<script src="/assets/site.js?v=20261016" defer></script></body></html>'
def translatable_nodes(s):
 for n in s.find_all(string=True):
  if isinstance(n,(Comment,Doctype)) or not n.strip():continue
  if n.parent.name in ['script','style','time']:continue
  if n.find_parent(class_='notranslate'):continue
  if not re.search('[A-Za-z]',n):continue
  if n.strip() in ['PikobuyChina','· PikobuyChina','W2C','QC','USD']:continue
  yield n
def attributes(s):
 for el in s.find_all(True):
  for a in ['placeholder','aria-label']:
   if el.get(a):yield el,a
  if el.name=='meta' and el.get('name')=='description':yield el,'content'
def extract():
 texts={}
 for p in pages:
  s=BeautifulSoup(shell(p),'html.parser')
  for n in translatable_nodes(s):texts.setdefault(key(str(n).strip()),str(n).strip())
  for el,a in attributes(s):texts.setdefault(key(el[a]),el[a])
 entries=[{'id':k,'text':t} for k,t in texts.items()]
 (ROOT/'translation-source.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2))
 print('Translation strings',len(entries),'words',sum(len(x['text'].split()) for x in entries))
def build(strict=True):
 catalog={l:json.loads((ROOT/'locales'/f'{l}.json').read_text()) for l in LANGS if l!='en' and (ROOT/'locales'/f'{l}.json').exists()}
 if strict and len(catalog)!=8:raise ValueError('All eight translation dictionaries are required')
 if strict:
  required=set()
  for p in pages:
   source=BeautifulSoup(shell(p),'html.parser')
   required.update(key(str(n).strip()) for n in translatable_nodes(source))
   required.update(key(el[a]) for el,a in attributes(source))
  incomplete={l:len([k for k in required if not isinstance(d.get(k),str) or not d[k].strip()]) for l,d in catalog.items()}
  if any(incomplete.values()):raise ValueError('Incomplete translations; no output written: '+str(incomplete))
 allurls=[];missing={}
 for lang in (LANGS if strict else ['en']):
  if lang!='en' and lang not in catalog:continue
  for p in pages:
   s=BeautifulSoup(shell(p),'html.parser');s.html['lang']='zh-CN' if lang=='zh' else lang
   def tr(t):
    if lang=='en':return t
    result=catalog[lang].get(key(t))
    if not result:missing.setdefault(lang,set()).add(t);return t
    return result
   for n in list(translatable_nodes(s)):
    original=str(n); text=original.strip();n.replace_with(original[:len(original)-len(original.lstrip())]+tr(text)+original[len(original.rstrip()):])
   for el,a in attributes(s):el[a]=tr(el[a])
   for a in s.find_all('a',href=True):
    href=a['href']
    if href.startswith('/') and not href.startswith('//') and not href.startswith('/assets/') and href not in ['/sitemap.xml','/sitemap.txt']:
     a['href']=url(href[1:],lang)
   for l,name in LANGS.items():
    option=s.new_tag('option',value=url(p['slug'],l));option.string=name
    if l==lang:option['selected']='selected'
    s.select_one('#language').append(option)
   language_links=s.new_tag('nav',attrs={'class':'language-links','aria-label':tr('Language')})
   for l,name in LANGS.items():
    a=s.new_tag('a',href=url(p['slug'],l),hreflang=('zh-CN' if l=='zh' else l));a.string=name
    if lang==l:a['aria-current']='page'
    language_links.append(a)
   s.footer.append(language_links)
   canonical=DOMAIN+url(p['slug'],lang)
   can=s.new_tag('link',rel='canonical',href=canonical);s.head.append(can)
   for l in list(LANGS)+['x-default']:
    tag=s.new_tag('link',rel='alternate',hreflang=('zh-CN' if l=='zh' else l),href=DOMAIN+url(p['slug'],l if l!='x-default' else 'en'));s.head.append(tag)
   if p['slug'] in seo_titles:s.title.string=seo_titles[p['slug']][lang]
   title=s.title.get_text();desc=s.find('meta',attrs={'name':'description'})['content']
   for prop,value in [('og:title',title),('og:description',desc),('og:url',canonical),('og:type','article' if p['article'] else 'website'),('og:site_name','PikobuyChina'),('og:image',DOMAIN+'/assets/123.png')]:
    t=s.new_tag('meta',property=prop,content=value);s.head.append(t)
   schema={'@context':'https://schema.org','@type':'Article' if p['article'] else 'WebPage','name':title,'description':desc,'url':canonical,'inLanguage':s.html['lang']}
   if p['article']:
    schema.update(headline=title,dateModified=DATE,author={'@type':'Organization','name':'PikobuyChina'},publisher={'@type':'Organization','name':'PikobuyChina'},mainEntityOfPage=canonical)
    if p['published']:schema['datePublished']=p['published']
   j=s.new_tag('script',type='application/ld+json');j.string=json.dumps(schema,ensure_ascii=False);s.head.append(j)
   ga=s.new_tag('script',src='https://www.googletagmanager.com/gtag/js?id=G-VLWTW53ETS');ga['async']='';s.head.append(ga)
   g=s.new_tag('script');g.string="window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-VLWTW53ETS');";s.head.append(g)
   for table in s.find_all('table'):
    wrap=s.new_tag('div',attrs={'class':'table-scroll','tabindex':'0'});table.wrap(wrap)
   dest=OUT/('' if lang=='en' else lang)/(p['slug']+'.html' if p['slug'] else 'index.html');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(str(s)+'\n')
   allurls.append((p['slug'],lang,canonical))
 if missing and strict:raise ValueError('Missing translations: '+str({l:len(v) for l,v in missing.items()}))
 # Localized URLs are canonical and independently crawlable, even with JavaScript disabled.
 xml=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
 for slug,lang,canonical in allurls:
  xml.append('<url><loc>'+xe(canonical)+'</loc><lastmod>'+DATE+'</lastmod>')
  for l in list(LANGS)+['x-default']:
   xml.append('<xhtml:link rel="alternate" hreflang="'+('zh-CN' if l=='zh' else l)+'" href="'+xe(DOMAIN+url(slug,l if l!='x-default' else 'en'))+'"/>')
  xml.append('</url>')
 xml.append('</urlset>');(OUT/'sitemap.xml').write_text('\n'.join(xml)+'\n');(OUT/'sitemap.txt').write_text('\n'.join(v[2] for v in allurls)+'\n')
 print('Built',len(allurls),'pages; missing', {l:len(v) for l,v in missing.items()})
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--extract',action='store_true');ap.add_argument('--english-only',action='store_true');args=ap.parse_args()
 if args.extract:extract()
 else:build(not args.english_only)
