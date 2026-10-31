"""Build all nine static locales. No runtime translation or external build service."""
from pathlib import Path
from bs4 import BeautifulSoup,Comment
import json,re,html,gzip
from xml.sax.saxutils import escape as xml
B=Path(__file__).resolve().parent;OUT=B.parents[1]/'lolobuychina';ORIGIN='https://lolobuychina.com'
LANGS={'en':'English','de':'Deutsch','fr':'Français','es':'Español','it':'Italiano','pt':'Português','ja':'日本語','ko':'한국어','zh':'简体中文'}
C=json.loads((B/'content.en.json').read_text());RED=json.loads((B/'redirects.json').read_text());PRODUCTS=json.loads((B/'products.json').read_text())
OVERRIDES=json.loads((B/'overrides.json').read_text()) if (B/'overrides.json').exists() else {}
for reviewed_file in (B/'reviewed').glob('*.json'):
 OVERRIDES.setdefault(reviewed_file.stem,{}).update(json.loads(reviewed_file.read_text()))
for extra_file in (B/'extra').glob('*.json'):
 OVERRIDES.setdefault(extra_file.stem.split('-')[0],{}).update(json.loads(extra_file.read_text()))
UI=['Home','Finds','Directory','W2C Links','QC Photos','Shipping','Articles','FAQ']
NAV=['/','/finds','/directory','/w2c','/qc','/shipping','/articles/','/faq']
CATS=[('Shoes','/shoes/'),('Sweatshirts','/hoodies-sweaters/'),('T-Shirts','/t-shirts/'),('Jackets','/jackets/'),('Pants / Shorts','/pants-shorts/'),('Headwear','/headwear/'),('Accessories','/accessories/'),('Jersey','/Jersey/'),('Electronics','/electronics/')]
FEATURED=['/articles/lolobuy-link-not-working','/articles/lolobuy-returns-refunds','/guides/lolobuy-qc-photo-checklist-2026','/guides/lolobuy-shipping-calculator-estimate-final-charge','/articles/lolobuy-shoe-finds-sizing-qc','/articles/lolobuy-tracking-order-status']
def path(lang,route):return ('' if lang=='en' else '/'+lang)+route

def build():
 for f in OUT.rglob('*.html'):f.unlink()
 for lang in LANGS:
  file=B/'translations'/f'{lang}.json';gz=file.with_suffix('.json.gz')
  cache={} if lang=='en' else json.loads(file.read_text() if file.exists() else gzip.decompress(gz.read_bytes()))
  override=OVERRIDES.get(lang,{})
  def t(s):
   if lang=='en':return s
   if s in override:return override[s]
   def one(x):
    if re.fullmatch(r'[0-9. ×÷=+$%–−,() /]+', x):return x
    if x in override:return override[x]
    if x not in cache:raise ValueError(f'Missing {lang}: {x}')
    return cache[x].replace('▁',' ').strip()
   v=' '.join(one(x) for x in re.split(r'(?<=[.!?])\s+(?=[A-Z“"0-9])',s))
   v=re.sub(r'LoloAcheter|LoloComprar|LoloCompre|ロロブイ|洛洛布依|洛洛布伊|洛洛布衣', 'LoloBuy',v)
   v=re.sub(r'(?i)lolo\s*buy\s*china','LoloBuyChina',v)
   v=re.sub(r'(?i)lolo\s*buy','LoloBuy',v)
   v=v.replace('Weidien','Weidian').replace('Weidiana','Weidian')
   if lang=='zh':v=v.replace('二极管','体积重除数').replace('引用','报价').replace('返回请求','退货申请').replace('返回期限','退货期限').replace('信贷','入账金额')
   if lang=='ja':v=v.replace('最終的な引用','最終見積もり').replace('船積み','発送')
   if lang=='ko':v=v.replace('순서 단계','주문 단계').replace('플랫폼 균형','플랫폼 잔액')
   return v
  def e(s):return html.escape(t(s),quote=True)
  def link(r,label):return f'<a href="{path(lang,r)}">{e(label)}</a>'
  def cards(routes):
   return '<div class="article-grid">'+''.join(f'<a class="article-card" href="{path(lang,r)}"><h3>{e(C[r]["title"])}</h3><p>{e(C[r]["description"])}</p><span>{e("Read article")} →</span></a>' for r in routes)+'</div>'
  def nav(route):return '<nav aria-label="'+e('Main navigation')+'">'+''.join(f'<a {"aria-current=page" if r==route else ""} href="{path(lang,r)}">{e(label)}</a>' for r,label in zip(NAV,UI))+'</nav>'
  def prod():return '<div class="products">'+''.join(f'<a class="product-card" data-product-id="{p["id"]}" href="{p["url"]}"><img src="{p["img"]}" alt="{e(p["cat"])} · {p["id"]}" width="600" height="600" loading="lazy"><div><h3>{e(p["cat"])} · {p["id"]}</h3><p>{e("Source ID")}: {p["id"]}</p><p>{e("Check current price")}</p><span>{e("View product")} ↗</span></div></a>' for p in PRODUCTS)+'</div>'
  def categories():return '<div class="categories">'+''.join(f'<a href="https://cnfanshm.com{u}"><h3>{e(n)}</h3><span>{e("Browse category")} ↗</span></a>' for n,u in CATS)+'</div>'
  def search():return f'<form class="search" data-product-search><label for="product-query">{e("Product link, source ID or keyword")}</label><div><input id="product-query" name="keywords" type="search" required placeholder="{e("Search product link, source ID or keyword")}"><button type="submit">{e("Search")}</button></div></form>'
  def article_index():
   groups={x:[] for x in ['Link and ordering guides','QC, sizing and buyer evidence','Shipping and cost planning','Orders, returns and tracking']}
   for r,p in C.items():
    if not p['article']:continue
    group='Orders, returns and tracking' if any(x in r for x in ['tracking','refund']) else 'QC, sizing and buyer evidence' if any(x in r for x in ['qc-photo','hoodie','shoe-finds','reviews']) else 'Link and ordering guides' if any(x in r for x in ['link-not','ordering','w2c-qc']) else 'Shipping and cost planning'
    groups[group].append(r)
   return ''.join('<section><h2>'+e(g)+'</h2>'+cards(rs)+'</section>' for g,rs in groups.items())
  for route,p in C.items():
   body=BeautifulSoup(p['body'],'html.parser')
   if lang!='en':
    for el in body.find_all(['p','h2','h1','li','td']):
     key=el.get_text(' ',strip=True)
     if key in override and not el.find('a'):
      el.clear();el.append(override[key]);el['data-reviewed']='1'
   for n in list(body.find_all(string=True)):
    s=str(n).strip()
    if n.parent.has_attr('data-reviewed') or n.parent.name in ['code','script','style'] or isinstance(n,Comment) or not re.search('[A-Za-z]',s) or s.startswith('__'):continue
    raw=str(n);n.replace_with((' ' if raw.startswith((' ','\n')) else '')+t(s)+(' ' if raw.endswith((' ','\n')) else ''))
   for reviewed in body.select('[data-reviewed]'):del reviewed['data-reviewed']
   for a in body.find_all('a',href=True):
    if a['href'].startswith('/'):
     h=a['href'];base,sep,frag=h.partition('#');base=RED.get(base,base)
     a['href']=path(lang,base)+(sep+frag if sep else '')
   for image in body.find_all('img'):
    # Existing English diagram assets contain embedded English; use localized text tables already in the article.
    if image.get('src','').endswith(('lolobuy-storage-planner.svg','lolobuy-total-cost-worksheet.svg')):image.decompose()
    elif image.get('alt') and re.search('[A-Za-z]',image['alt']):image['alt']=t(image['alt'])
   if p['article']:
    for h in body.find_all('h1'):h.decompose()
    toc=[]
    for i,h in enumerate(body.find_all('h2')):
     h['id']=h.get('id',f'section-{i+1}');toc.append(f'<a href="#{h["id"]}">{html.escape(h.get_text(" ",strip=True))}</a>')
    top=f'<p class="eyebrow">{e("Independent buying guide")}</p><h1>{e(p["title"])}</h1><p class="byline">{e("LoloBuyChina Editorial")} · {e("Updated 31 October 2026")}</p>'
    top+=f'<details class="contents"><summary>{e("Contents")}</summary><nav>'+''.join(toc)+'</nav></details>'
    body_html=top+str(body)+f'<aside class="related"><h2>{e("Related reading")}</h2>'+ ' · '.join(link(r,l) for r,l in [('/w2c','W2C Links'),('/qc','QC Photos'),('/shipping','Shipping'),('/articles/','Articles'),('/faq','FAQ')])+'</aside>'
   else:body_html=str(body)
   for tag,val in [('__SEARCH__',search()),('__PRODUCTS__',prod()),('__CATEGORIES__',categories()),('__FEATURED__',cards(FEATURED)),('__ALL_ARTICLES__',article_index())]:body_html=body_html.replace(tag,val)
   canonical=ORIGIN+path(lang,route)
   alternates=''.join(f'<link rel="alternate" hreflang="{l}" href="{ORIGIN+path(l,route)}">' for l in LANGS)+f'<link rel="alternate" hreflang="x-default" href="{ORIGIN+route}">'
   schema={'@context':'https://schema.org','@type':'Article' if p['article'] else 'WebPage','headline':t(p['title']),'description':t(p['description']),'url':canonical,'inLanguage':lang,'dateModified':'2026-10-31','publisher':{'@type':'Organization','name':'LoloBuyChina','url':ORIGIN+'/'}}
   if p['article']:schema.update({'datePublished':p['published'],'mainEntityOfPage':canonical,'author':{'@type':'Organization','name':'LoloBuyChina Editorial'}})
   switch='<details class="language"><summary>'+LANGS[lang]+'</summary><div>'+''.join(f'<a href="{path(l,route)}" lang="{l}" hreflang="{l}" {"aria-current=true" if l==lang else ""}>{label}</a>' for l,label in LANGS.items())+'</div></details>'
   doc=f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(p['title'])}</title><meta name="description" content="{e(p['description'])}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}">{alternates}<meta property="og:title" content="{e(p['title'])}"><meta property="og:description" content="{e(p['description'])}"><meta property="og:url" content="{canonical}"><meta property="og:type" content="{'article' if p['article'] else 'website'}"><link rel="stylesheet" href="/site.css"><script defer src="/catalog-links.js"></script><script defer src="/site-shell.js"></script><script async src="https://www.googletagmanager.com/gtag/js?id=G-ZCJYW7N8RN"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-ZCJYW7N8RN');</script><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace('</','<\\/')}</script></head><body><a class="skip" href="#main">{e('Skip to content')}</a><header class="site-header"><div class="topbar"><a class="brand" href="{path(lang,'/')}"><img src="/logo.svg" alt="LoloBuyChina" width="200" height="37"></a>{switch}</div>{nav(route)}</header><main id="main" class="{'reading' if p['article'] else 'wide'}">{body_html}</main><footer><p>© 2026 LoloBuyChina · {e('Independent product discovery and buying guides. Not operated by LoloBuy.')}</p>{link('/articles/','Articles')} · {link('/faq','FAQ')}</footer></body></html>'''
   dest=OUT/(path(lang,route).lstrip('/')+('index.html' if route.endswith('/') else '.html'));dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(doc)
  error=f'<!doctype html><html lang="{lang}"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>404 · {e("Page not found")}</title><link rel="stylesheet" href="/site.css"><main class="reading"><h1>{e("Page not found")}</h1><p>{e("The requested page is unavailable. Choose a guide or return to the homepage.")}</p>{link("/","Back to home")}</main></html>'
  dest=OUT/(('' if lang=='en' else lang+'/')+'404.html');dest.write_text(error)
 routes=[path(l,r) for l in LANGS for r in C]
 sm=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
 for l in LANGS:
  for r in C:
   sm.append('<url><loc>'+ORIGIN+path(l,r)+'</loc><lastmod>2026-10-31</lastmod>'+''.join(f'<xhtml:link rel="alternate" hreflang="{al}" href="{ORIGIN+path(al,r)}"/>' for al in LANGS)+f'<xhtml:link rel="alternate" hreflang="x-default" href="{ORIGIN+r}"/></url>')
 sm.append('</urlset>');(OUT/'sitemap.xml').write_text('\n'.join(sm));(OUT/'sitemap.txt').write_text('\n'.join(ORIGIN+r for r in routes)+'\n')
 (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://lolobuychina.com/sitemap.xml\n')
 worker=(B/'worker.js').read_text().replace('__ROUTES__',json.dumps(routes)).replace('__REDIRECTS__',json.dumps(RED)).replace('__LANGS__',json.dumps(list(LANGS)))
 (OUT/'_worker.js').write_text(worker)
 (OUT/'site.css').write_text((B/'site.css').read_text());(OUT/'site-shell.js').write_text((B/'site-shell.js').read_text())
 print('Built',len(routes),'canonical pages across',len(LANGS),'languages')
if __name__=='__main__':build()
