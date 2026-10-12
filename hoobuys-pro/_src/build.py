"""Build complete static language routes; generated HTML is committed for Pages."""
from pathlib import Path
from lxml import html, etree
from html import escape as esc
from urllib.parse import urlsplit
import json, re
B=Path(__file__).resolve().parents[1]; S=B/'_src'; ORIGIN='https://hoobuys.pro'; DATE='2026-10-12'
UI=json.loads((S/'ui.json').read_text()); LANGS=list(UI); NAMES={'en':'English','de':'Deutsch','es':'Español','fr':'Français','it':'Italiano'}
ORIGINAL={slug:json.loads((S/'original'/(slug+'.json')).read_text()) for slug in json.loads((S/'original-order.json').read_text())}; PRODUCTS=json.loads((S/'products.json').read_text())
NEW=['hoobuy-shoes-spreadsheet','hoobuy-hoodies-spreadsheet','hoobuy-size-guide','hoobuy-budget-finds']
CORE=['hoobuy-spreadsheet-guide','hoobuy-pro-qc-photo-video-checklist-2026','shipping-guide']
SLUGS=NEW+list(ORIGINAL)
PAGES=['','products','guides','faq','privacy','terms']+SLUGS

def path(lang,slug=''):
 return ('/' if lang=='en' else '/'+lang+'/')+slug

def localize(body,lang):
 root=html.fragment_fromstring(body,create_parent='div')
 for a in root.xpath('.//a[@href]'):
  href=a.get('href');v=urlsplit(href)
  if href.startswith('/') and not href.startswith('//'):
   slug=v.path.strip('/').removesuffix('.html')
   if slug=='index':slug=''
   if slug in PAGES:a.set('href',path(lang,slug)+('?' +v.query if v.query else '')+('#'+v.fragment if v.fragment else ''))
 return ''.join(etree.tostring(c,encoding='unicode',method='html') for c in root)

ART={}
for lang in LANGS:
 ART[lang]={}
 for slug in SLUGS:
  p=S/'content'/lang/(slug+'.md')
  if p.exists():
   title,desc,body=p.read_text().split('\n',2);ART[lang][slug]={'title':title,'seo':title,'description':desc,'body':body.strip(),'published':DATE}
  elif lang=='en' and slug in ORIGINAL:ART[lang][slug]=dict(ORIGINAL[slug])
  else:raise RuntimeError('Missing complete translation: '+str(p))
# Search-intent improvements retain existing English article bodies.
UPDATES={
'shipping-guide':('Hoobuy Shipping Estimate: Calculator, Weight & Final Cost','Estimate Hoobuy shipping with destination, packed weight and dimensions. Compare calculator inputs, billable weight and the final shipping charge.','<p class="answer"><strong>To estimate Hoobuy shipping, record the destination, packed weight, item category and parcel dimensions, then compare the current eligible routes.</strong> Keep a preliminary estimate separate from the shipping deposit and final carrier-verified charge. The official beginner guide describes final billing using verified package size and weight.</p><p>Use the <a href="/hoobuy-shipping-calculator-estimate-final-charge-guide-2026">calculator-to-final-charge ledger</a> when an estimate changes. For a new purchase, start with the <a href="/hoobuy-budget-finds">complete-cost budget</a> rather than treating the product price as the delivered total.</p>'),
'hoobuy-spreadsheet-guide':('Hoobuy Spreadsheet With QC: Links, Photos & Price Checks','Check a Hoobuy spreadsheet with exact product links, option prices and separate seller and warehouse QC photos. Build a dated product record.','<p class="answer"><strong>A Hoobuy spreadsheet with QC should separate the seller listing from warehouse evidence for the exact item received.</strong> Save the current URL, selected option, source price, size evidence and check date before purchase; add warehouse photos and an approval decision after arrival.</p><p>Use the dedicated <a href="/hoobuy-shoes-spreadsheet">shoe spreadsheet guide</a>, <a href="/hoobuy-hoodies-spreadsheet">hoodie spreadsheet guide</a> and <a href="/hoobuy-size-guide">size-chart guide</a> for the checks that differ by category.</p>'),
'hoobuy-pro-qc-photo-video-checklist-2026':('Hoobuy QC Photos: Shoe & Clothing Inspection Checklist','Review Hoobuy QC photos for exact item, size, measurements and visible defects. Know when to request another photo or investigate a mismatch.','<p class="answer"><strong>Start Hoobuy QC with the exact order, colour, size and quantity, then inspect measurements and visible condition.</strong> Seller images and another buyer\'s photos do not prove the condition of your item. A warehouse photo cannot authenticate a product or guarantee hidden materials and durability.</p><p>For a size decision, compare the <a href="/hoobuy-size-guide">measurement method</a> first. Shoe and hoodie checks are expanded in the <a href="/hoobuy-shoes-spreadsheet">shoe guide</a> and <a href="/hoobuy-hoodies-spreadsheet">hoodie guide</a>.</p>')}
for slug,(title,desc,intro) in UPDATES.items():
 ART['en'][slug].update(title=title,seo=title,description=desc,body=intro+ART['en'][slug]['body'])

def card(lang,slug):
 a=ART[lang][slug];u=UI[lang]
 return f'<a class="article-card" href="{path(lang,slug)}"><h3>{esc(a["title"])}</h3><p>{esc(a["description"])}</p><span class="link">{u["read"]} →</span></a>'

def product_card(lang,p,i):
 u=UI[lang];q=u['qcShoes' if p['category']=='shoes' else 'qcClothes' if p['category'] in ['hoodies','shirts','jackets','pants','jerseys'] else 'qcOther']
 return f'''<article class="product-card" id="{p['category']}"><a class="pic" href="{p['url']}" target="_blank" rel="nofollow sponsored noopener"><img src="{p['image']}" alt="{esc(p['title'])} — {u['listing']}" width="600" height="450" {'fetchpriority="high"' if i==0 else 'loading="lazy"'}></a><h3>{esc(p['title'])}</h3><div class="meta">{u[p['category']]}</div><div class="price">{esc(p['price'])}</div><p class="qc">{q}</p><a class="btn" href="{p['url']}" target="_blank" rel="nofollow sponsored noopener">{u['view']} ↗</a></article>'''

META=[]
def page(lang,slug,title,desc,body,article=False,published=DATE,modified=DATE,noindex=False):
 u=UI[lang];url=ORIGIN+path(lang,slug)
 alts=''.join(f'<link rel="alternate" hreflang="{l}" href="{ORIGIN+path(l,slug)}">' for l in LANGS)+f'<link rel="alternate" hreflang="x-default" href="{ORIGIN+path("en",slug)}">' if not noindex else ''
 nav=''.join(f'<a {"aria-current=\"page\"" if slug==s else ""} href="{path(lang,s)}">{u[k]}</a>' for s,k in [('', 'home'),('products','finds'),('guides','guides'),('faq','faq')])
 switches=''.join(f'<a lang="{l}" hreflang="{l}" href="{path(l,slug if not noindex else "")}" {"aria-current=\"page\"" if lang==l else ""}>{NAMES[l]}</a>' for l in LANGS)
 graph=[{'@type':'WebPage','@id':url,'url':url,'name':title,'description':desc,'inLanguage':lang}]
 if article:
  graph.append({'@type':'Article','headline':title,'description':desc,'datePublished':published,'dateModified':modified,'inLanguage':lang,'mainEntityOfPage':url,'author':{'@type':'Organization','name':'hoobuys.pro Editorial'},'publisher':{'@type':'Organization','name':'hoobuys.pro Editorial'}})
  graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':u['home'],'item':ORIGIN+path(lang)},{'@type':'ListItem','position':2,'name':u['guides'],'item':ORIGIN+path(lang,'guides')},{'@type':'ListItem','position':3,'name':title,'item':url}]})
 if not slug:graph.append({'@type':'WebSite','@id':ORIGIN+'/#website','url':ORIGIN,'name':'hoobuys.pro','inLanguage':LANGS})
 result=f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc,quote=True)}"><meta name="robots" content="{'noindex,follow' if noindex else 'index,follow,max-image-preview:large'}"><link rel="canonical" href="{url}">{alts}<meta property="og:type" content="{'article' if article else 'website'}"><meta property="og:title" content="{esc(title,quote=True)}"><meta property="og:description" content="{esc(desc,quote=True)}"><meta property="og:url" content="{url}"><meta property="og:site_name" content="hoobuys.pro"><meta name="site-revision" content="2026-10-12-multilingual-seo"><link rel="stylesheet" href="/assets/styles.css"><script async src="https://www.googletagmanager.com/gtag/js?id=G-KG6V0Z9TWS"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-KG6V0Z9TWS');</script><script src="/assets/analytics.js" defer></script><script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False)}</script></head><body><a class="skip" href="#main">{u['skip']}</a><header class="top"><div class="wrap bar"><a class="brand" href="{path(lang)}">hoobuys<span>.</span>pro</a><nav class="nav" aria-label="{u['home']}">{nav}</nav><details class="language-picker"><summary>{NAMES[lang]}</summary><nav aria-label="{u['lang']}">{switches}</nav></details></div></header><main class="wrap" id="main">{localize(body,lang)}</main><footer class="foot"><div class="wrap"><p>hoobuys.pro · {u['independent']}</p><p>{u['disclosure']}</p><a href="{path(lang,'privacy')}">{u['privacy']}</a> · <a href="{path(lang,'terms')}">{u['terms']}</a> · <a href="/sitemap.xml">{u['sitemap']}</a></div></footer></body></html>'''
 dest=B/(lang if lang!='en' else '')/(slug+'.html' if slug else 'index.html');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(result)
 if not noindex:META.append({'lang':lang,'slug':slug,'url':url,'modified':modified})

LEGAL=json.loads((S/'legal.json').read_text())
for lang,u in UI.items():
 home=f'<section class="hero"><div class="eyebrow">{u["independent"]}</div><h1>{u["homeTitle"]}</h1><p>{u["intro"]}</p><form class="search" action="https://cnfanssp.com/search.html" method="get" target="_blank"><label class="sr-only" for="q">{u["search"]}</label><input id="q" name="keywords" required placeholder="{u["searchHint"]}"><input type="hidden" name="channelid" value="2"><button type="submit">{u["search"]} ↗</button></form><div class="actions"><a class="btn" href="/products">{u["browse"]}</a><a href="/shipping-guide">{ART[lang]["shipping-guide"]["title"]} →</a></div></section>'
 home+=f'<section class="section"><div class="section-head"><h2>{u["finds"]}</h2><a href="/products">{u["browse"]} →</a></div><div class="product-grid">'+''.join(product_card(lang,p,i) for i,p in enumerate(PRODUCTS[:5]))+f'</div><p class="meta">{u["currency"]}</p></section>'
 home+=f'<section class="section"><div class="section-head"><h2>{u["latest"]}</h2><a href="/guides">{u["all"]} →</a></div><div class="article-grid">'+''.join(card(lang,s) for s in NEW)+'</div></section>'
 home+=f'<section class="section"><h2>{u["essential"]}</h2><div class="essential-links">'+''.join(f'<a href="/{s}">{esc(ART[lang][s]["title"])} →</a>' for s in CORE)+'</div></section>'
 home+=f'<section class="section"><h2>{u["more"]}</h2><nav class="chips">'+''.join(f'<a href="/products#{p["category"]}">{u[p["category"]]}</a>' for p in PRODUCTS)+'</nav></section>'
 faqdoc=html.fragment_fromstring(LEGAL[lang]['faq']['body'],create_parent='div');faqitems=faqdoc.xpath('.//details')
 home+=f'<section class="section"><div class="section-head"><h2>{u["faq"]}</h2><a href="/faq">{u["faq"]} →</a></div><div class="faq-list home-faq">'+''.join(etree.tostring(faqitems[i],encoding='unicode',method='html') for i in [0,4,8])+'</div></section>'
 page(lang,'',u['homeTitle'],u['homeDesc'],home)
 chips=''.join(f'<a href="#{p["category"]}">{u[p["category"]]}</a>' for p in PRODUCTS)
 prod=f'<section class="hero"><h1>{u["productsTitle"]}</h1><p>{u["catalogNote"]}</p><p class="meta">{u["currency"]}</p><nav class="chips">{chips}</nav></section><div class="product-grid">'+''.join(product_card(lang,p,i) for i,p in enumerate(PRODUCTS))+'</div>'
 cats={'shoes':'shoes','hoodies':'hoodies-sweaters','shirts':'t-shirts','jackets':'jackets','pants':'pants-shorts','headwear':'headwear','accessories':'accessories','jerseys':'Jersey','electronics':'electronics','other':'other-stuff'}
 prod+=f'<section class="section"><h2>{u["more"]}</h2><div class="chips">'+''.join(f'<a href="https://cnfanssp.com/{v}/" target="_blank" rel="nofollow sponsored noopener" data-category="{k}">{u[k]} ↗</a>' for k,v in cats.items())+'</div></section><div class="article-grid">'+''.join(card(lang,s) for s in NEW[:2])+'</div>'
 prod+=f'<p><a class="btn" href="https://cnfanssp.com/AllProducts/" target="_blank" rel="nofollow sponsored noopener">{u["index"]} ↗</a></p>'
 page(lang,'products',u['productsTitle'],u['productsDesc'],prod)
 hub=f'<section class="hero"><h1>{u["guideTitle"]}</h1><p>{u["guideIntro"]}</p></section><h2>{u["latest"]}</h2><div class="article-grid">'+''.join(card(lang,s) for s in NEW)+f'</div><section class="section"><h2>{u["all"]}</h2><div class="article-grid">'+''.join(card(lang,s) for s in ORIGINAL)+'</div></section>'
 page(lang,'guides',u['guideTitle'],u['guideDesc'],hub)
 for slug,a in ART[lang].items():
  root=html.fragment_fromstring(a['body'],create_parent='div')
  for old in root.xpath('.//section[contains(@class,"sources")]'):old.getparent().remove(old)
  toc=[]
  for i,h in enumerate(root.xpath('.//h2')):
   h.set('id','section-'+str(i+1));toc.append(f'<li><a href="#section-{i+1}">{esc(h.text_content())}</a></li>')
  text=''.join(etree.tostring(c,encoding='unicode',method='html') for c in root)
  related=[s for s in (NEW+CORE) if s!=slug][:4]
  updated=DATE if lang!='en' or slug in NEW+CORE else '2026-09-10'
  meta=u['review'] if updated==DATE else '2026-09-10'
  article=f'<div class="breadcrumbs"><a href="/">{u["home"]}</a> / <a href="/guides">{u["guides"]}</a></div><article class="article"><h1>{esc(a["title"])}</h1><p class="meta">{meta}</p><p class="disclosure">{u["disclosure"]}</p><nav class="toc" aria-label="{u["toc"]}"><strong>{u["toc"]}</strong><ol>{"".join(toc)}</ol></nav>{text}<section class="sources"><h2>{u["sources"]}</h2><p>{u["sourceNote"]}</p></section><section class="related"><h2>{u["related"]}</h2><ul>'+''.join(f'<li><a href="/{s}">{esc(ART[lang][s]["title"])}</a></li>' for s in related)+f'</ul><a class="btn" href="/products">{u["browse"]} →</a></section></article>'
  page(lang,slug,a['seo'],a['description'],article,True,a['published'],updated)
 for slug in ['faq','privacy','terms']:
  a=LEGAL[lang][slug];page(lang,slug,a['title'],a['description'],f'<article class="article"><h1>{a["title"]}</h1>{a["body"]}</article>')
 page(lang,'404',u['notFound'],u['notFoundText'],f'<section class="hero"><h1>{u["notFound"]}</h1><p>{u["notFoundText"]}</p><a class="btn" href="{path(lang,"guides")}">{u["all"]}</a></section>',noindex=True)

ns='http://www.sitemaps.org/schemas/sitemap/0.9';xh='http://www.w3.org/1999/xhtml'
root=etree.Element('{'+ns+'}urlset',nsmap={None:ns,'xhtml':xh})
for m in META:
 row=etree.SubElement(root,'{'+ns+'}url');etree.SubElement(row,'{'+ns+'}loc').text=m['url'];etree.SubElement(row,'{'+ns+'}lastmod').text=m['modified']
 for lang in LANGS+['x-default']:etree.SubElement(row,'{'+xh+'}link',rel='alternate',hreflang=lang,href=ORIGIN+path('en' if lang=='x-default' else lang,m['slug']))
(B/'sitemap.xml').write_bytes(etree.tostring(root,encoding='utf-8',xml_declaration=True,pretty_print=True));(B/'sitemap.txt').write_text('\n'.join(m['url'] for m in META)+'\n')
(B/'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /_src/\nSitemap: https://hoobuys.pro/sitemap.xml\n')
(S/'manifest.json').write_text(json.dumps({'date':DATE,'languages':LANGS,'articles_per_language':len(SLUGS),'pages':META},ensure_ascii=False,indent=2))
print(f'Built {len(META)} indexable pages, {len(SLUGS)} guides per language, {len(LANGS)} languages.')
