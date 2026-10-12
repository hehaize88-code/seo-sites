"""Reproducible static publishing. Run build.py, translate.py, then build.py --all.

Only hoobuys-org is generated. No build step is required in the hosting project.
"""
from pathlib import Path
from bs4 import BeautifulSoup
from html import escape as e
import json, re, hashlib, sys
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET

B=Path(__file__).resolve().parents[1]; S=B/'_src'; DATE='2026-10-12'; ORIGIN='https://hoobuys.org'
LANGS=['en','zh-CN','de','fr','es','it','pl','nl','pt']
NAMES={'en':'English','zh-CN':'简体中文','de':'Deutsch','fr':'Français','es':'Español','it':'Italiano','pl':'Polski','nl':'Nederlands','pt':'Português'}
P=json.loads((S/'original.json').read_text()); PRODUCTS=json.loads((S/'products.json').read_text())
NEW={
 'hoobuy-shipping-calculator-weight-and-cost':('HooBuy Shipping Calculator: Weight, Dimensions & Cost','Use the HooBuy shipping calculator with the right weight and dimensions. Compare volumetric weight, parcel scenarios and dated shipping estimates.'),
 'hoobuy-qc-photo-checklist':('HooBuy QC Photos: Practical Shoe & Clothing Checklist','Check HooBuy QC photos for the exact order, size, measurements and visible defects. See what to inspect and how to request useful evidence.'),
 'hoobuy-total-cost-budget':('HooBuy Total Cost: Product, Shipping & Budget Guide','Build a HooBuy total-cost budget with product prices, domestic and international shipping. Separate estimates, paid amounts and unknown charges.')}
for slug,(title,desc) in NEW.items():P[slug]={'title':title,'description':desc,'body':(S/'content'/(slug+'.html')).read_text(),'article':True,'published':DATE}

UPDATES={
 'hoobuy-spreadsheet-guide':('HooBuy Spreadsheet Guide: Verified Links, Size & QC','Build a HooBuy spreadsheet with exact product links, selected prices, size evidence and QC status. Use clear fields from discovery to shipping.','Start a HooBuy spreadsheet with one row per exact product option. Save the current link, selected price, size evidence and verification date; add order details, warehouse QC and parcel measurements as they become available.'),
 'hoobuy-product-link-verification-taobao-1688-weidian-2026':('HooBuy Links: Verify Taobao, 1688 & Weidian Products','Check HooBuy product links from Taobao, 1688 and Weidian. Resolve redirects, verify seller and item identity, and preserve the exact selected option.','To verify a HooBuy product link, open the final destination and match the marketplace, item ID, seller and selected option. A familiar product image alone cannot confirm that a replacement link describes the same listing.'),
 'hoobuy-org-w2c-qc-shipping-workflow-2026':('HooBuy W2C to Shipping: Links, QC & Parcel Checklist','Follow a HooBuy purchase from product discovery to QC and shipping. Use practical checkpoints for listing identity, measurements and parcel readiness.','Use four checkpoints: verify the product link, record the exact order, review warehouse evidence and estimate the packed parcel. Close critical unknowns at each checkpoint before moving to the next decision.'),
 'hoobuy-org-w2c-spreadsheet-method-2026':('HooBuy W2C Spreadsheet: Fields, Status & Examples','Organize W2C product links with source IDs, selected options, price dates and QC status. Keep blocked, ordered and parcel-ready rows distinct.','A W2C spreadsheet needs a stable candidate ID, the exact source link and option, dated price evidence and a next-action status. Separate a discovered product from one that is ready to order or ship.'),
 'hoobuy-shoes-spreadsheet-size-qc-fields-2026':('HooBuy Shoes Spreadsheet: Sizing & QC Checklist','Compare HooBuy shoe finds using exact sizes, foot measurements, QC views and packaging records. Keep labels and measured fit evidence separate.','For a shoe spreadsheet, record the exact size label and the sizing method behind it. Plan QC views for both shoes, labels and outsoles, then keep packaging choices separate from the fit decision.'),
 'hoobuy-hoodie-spreadsheet-fabric-measurements-weight-2026':('HooBuy Hoodie Spreadsheet: Size, Fabric & QC Checks','Compare HooBuy hoodies by chest, length and sleeve measurements. Record fabric claims, QC checks and weight without guessing from size labels.','Compare hoodies using compatible chest, length and sleeve measurements. Keep the seller’s fabric description separate from what warehouse photos show, and label weight as estimated or measured.'),
 'shipping-guide':('HooBuy Shipping Guide: Prepare & Compare Your Parcel','Prepare a HooBuy parcel with weight, dimensions, destination and packaging checks. Connect shipping estimates to QC approval and a complete budget.','Before choosing shipping, confirm the approved items, destination, contents, packed weight and dimensions. Compare eligible routes using the same parcel inputs and keep the estimate separate from the amount actually paid.')}
for slug,(title,desc,intro) in UPDATES.items():
 P[slug].update(title=title,description=desc)
 P[slug]['body']='<p class="answer">'+intro+'</p>'+P[slug]['body']
# Existing bodies remain intact; improve their first practical decision and connected reading.
EXTRA={
 'hoobuy-1688-finds-moq-variants-seller-questions-2026':'Before saving a 1688 find, check the minimum order quantity for the exact variant and quantity you intend to buy. Record seller answers separately from the page text.',
 'hoobuy-taobao-finds-compare-listings-2026':'Compare Taobao finds only after selecting the intended size, colour and version. Save the selected price and seller identity before deciding which listing is cheaper.',
 'hoobuy-weidian-finds-options-seller-signals-2026':'A useful Weidian find includes the exact item and seller, original option labels and a current check date. Similar photographs do not make two listings equivalent.',
 'hoobuy-size-chart-workflow-measurements-2026':'Compare the seller’s chart with measurements taken using the same units and endpoints. Flat garment width, body circumference and recommended fit ranges are different measurements.',
 'hoobuy-bags-spreadsheet-dimensions-hardware-shipping-2026':'Compare bags by exterior dimensions, included pieces and visible hardware details. Keep the bag’s dimensions separate from the packed parcel size used for shipping.',
 'hoobuy-jersey-spreadsheet-sizing-customization-qc-2026':'Record the jersey edition, size and exact customization text before ordering. Later QC should check that selected spelling, number and visible badge placement match the order.',
 'hoobuy-keyword-search-better-product-finds-2026':'Build product searches from a category and a useful attribute, then add material, fit or construction terms only when they help distinguish candidates. Verify the resulting listing before saving it.',
 'hoobuy-seller-page-checklist-before-saving-find-2026':'Before adding a find to your shortlist, confirm the seller, item, selected option, displayed price and size evidence. Keep an unresolved critical question visible as a blocker.',
 'hoobuy-autumn-finds-spreadsheet-2026':'Build an autumn shortlist around the clothing you will actually use. Compare layers, measurements and packing needs before adding overlapping products to one parcel.',
 'hoobuy-holiday-shopping-timeline-spreadsheet-2026':'Plan backwards from your real use date and set a stop-adding date for the parcel. Seller dispatch, warehouse review and international delivery are separate uncertainties.'}
for slug,intro in EXTRA.items():P[slug]['body']='<p class="answer">'+intro+'</p>'+P[slug]['body']
P['shipping-guide']['body']+='''<h2>Prepare a parcel record</h2><ol><li>List the warehouse identifiers for the items you have approved.</li><li>Record the destination and the actual contents.</li><li>Keep item weights separate from the finished parcel weight.</li><li>Record length, width and height after the proposed packing is known.</li><li>Compare eligible routes and preserve the date and currency of each estimate.</li></ol><h2>Keep packing choices explicit</h2><p>Write down whether original boxes, protective material or other packaging are required. A smaller parcel is useful only if the configuration is feasible and still protects the contents you intend to receive. Recheck dimensions when the configuration changes.</p><h2>Follow the detailed guides</h2><p>Use the <a href="/hoobuy-shipping-calculator-weight-and-cost">shipping calculator and weight guide</a> for units, volumetric calculations and a worked example. Use the <a href="/hoobuy-total-cost-budget">total-cost budget</a> to keep domestic delivery, international shipping and optional charges on separate lines.</p><p>Complete the <a href="/hoobuy-qc-photo-checklist">QC photo review</a> before adding an unresolved item to a parcel. Keep any question about current order options separate from a shipping estimate.</p>'''
for slug in ['hoobuy-org-w2c-spreadsheet-method-2026','hoobuy-org-w2c-qc-shipping-workflow-2026']:
 P[slug]['body']+='''<h2>Work through one candidate</h2><p>Imagine a hoodie discovered through a shared link. Start by recording the final marketplace URL, seller and exact colour and size. Save the selected price and the seller’s chest-width and length method, then compare those measurements with a garment you own.</p><p>After ordering, attach the order and warehouse identifiers to that same row. Use <a href="/hoobuy-qc-photo-checklist">QC photos</a> to check the received label, visible condition and relevant measurements. An unclear measurement stays unresolved instead of becoming an automatic approval.</p><h2>Move from an approved item to a parcel</h2><p>Once the item is approved for your use, add it to a dated parcel version. Individual item weight is an early input; packed dimensions and weight belong to the later shipping record. Follow the <a href="/hoobuy-shipping-calculator-weight-and-cost">shipping calculator guide</a> and preserve the inputs behind every estimate.</p><p>Keep the <a href="/hoobuy-total-cost-budget">complete budget</a> alongside the workflow. A paid product, pending domestic delivery and estimated international shipment are different cost states. A missing figure should remain pending until there is evidence to resolve it.</p>'''

ARTICLES=list(NEW)+[s for s,a in P.items() if a['article'] and s not in NEW]
PAGES=['index','products','guides','faq','privacy','terms','languages']+ARTICLES+['404']
def route(lang,slug):return ('/' if lang=='en' else '/'+lang+'/')+('' if slug=='index' else slug)
def card(slug):
 a=P[slug];return f'<a class="article-card" href="/{slug}"><h3>{e(a["title"])}</h3><p>{e(a["description"])}</p><span>Read guide →</span></a>'
def products(limit=10):
 return '<div class="product-grid">'+''.join(f'<article class="product-card"><a href="{p["url"]}" rel="nofollow sponsored"><img src="{p["image"]}" alt="{e(p["title"])} product listing" width="600" height="600" loading="lazy"></a><h3>{e(p["title"])}</h3><p>Check the selected option, current price and size evidence.</p><a class="button" href="{p["url"]}" rel="nofollow sponsored">View product ↗</a></article>' for p in PRODUCTS[:limit])+'</div>'
CALCULATOR='''<section class="calculator" aria-labelledby="calculator-title"><h3 id="calculator-title">Parcel weight calculator</h3><p>Arithmetic helper only. Enter the divisor used by the route you are checking. The suggested value is an example, not a universal shipping rule.</p><form id="weight-form"><div class="input-grid"><label>Actual weight (g)<input name="weight" type="number" min="1" max="1000000" step="any" value="2400" required></label><label>Length (cm)<input name="length" type="number" min="0.1" max="1000" step="any" value="40" required></label><label>Width (cm)<input name="width" type="number" min="0.1" max="1000" step="any" value="30" required></label><label>Height (cm)<input name="height" type="number" min="0.1" max="1000" step="any" value="25" required></label><label>Route divisor<input name="divisor" type="number" min="1" max="100000" step="any" value="6000" required></label></div><button type="submit">Calculate weight</button></form><div class="calc-result" aria-live="polite" hidden><p><span>Actual weight:</span> <strong data-result="actual"></strong> kg</p><p><span>Volumetric weight:</span> <strong data-result="volume"></strong> kg</p><p><span>Greater of the two:</span> <strong data-result="greater"></strong> kg</p><p>Minimum units, rounding, eligibility and prices must be checked for the selected route.</p></div></section>'''

SEARCH='''<form class="product-search" role="search" action="https://cnfanssp.com/search.html" method="get"><label for="product-keywords">Search products</label><div class="search-fields"><input type="search" id="product-keywords" name="keywords" placeholder="Search shoes, hoodies, bags..." maxlength="120" required><input type="hidden" name="channelid" value="2"><button type="submit">Search</button></div></form>'''

BODY={}
BODY['index']='''<section class="hero"><div><p class="eyebrow">Independent HooBuy buying guides</p><h1>HooBuy Finds & Product Links</h1><p class="lead">Find a product. Check the details. Plan the parcel.</p><p>Browse product links and practical guides for spreadsheet research, sizing, QC photos and shipping costs.</p><div class="actions"><a class="button" href="/products">Browse product links →</a><a class="button secondary" href="/hoobuy-spreadsheet-guide">Build your spreadsheet</a></div></div><div class="hero-panel"><span class="step-label">YOUR NEXT STEP</span><a href="/hoobuy-product-link-verification-taobao-1688-weidian-2026"><b>01</b><span>Verify the exact product link</span><span>↗</span></a><a href="/hoobuy-qc-photo-checklist"><b>02</b><span>Review warehouse QC photos</span><span>↗</span></a><a href="/hoobuy-shipping-calculator-weight-and-cost"><b>03</b><span>Estimate parcel weight and cost</span><span>↗</span></a></div></section>'''
BODY['index']=BODY['index'].replace('<div class="actions">',SEARCH+'<div class="actions">',1)
BODY['index']+='<section class="section"><div class="section-head"><h2>Start with a product</h2><a href="/products">All product links →</a></div>'+products(5)+'</section>'
BODY['index']+='<section class="section"><div class="section-head"><h2>Make the next decision easier</h2><a href="/guides">All guides →</a></div><div class="article-grid">'+''.join(card(s) for s in NEW)+'</div></section>'
BODY['index']+='<section class="section"><h2>Build a reliable shortlist</h2><div class="article-grid">'+''.join(card(s) for s in ['hoobuy-spreadsheet-guide','hoobuy-shoes-spreadsheet-size-qc-fields-2026','hoobuy-hoodie-spreadsheet-fabric-measurements-weight-2026'])+'</div></section>'
P['index'].update(title='HooBuy Finds & Product Links | Spreadsheet, QC & Shipping',description='Explore HooBuy product links and practical guides. Verify listings, compare sizes, review QC photos and plan shipping with a parcel weight calculator.')
BODY['products']='<section class="page-intro"><p class="eyebrow">Product discovery</p><h1>HooBuy Product Links & Finds</h1><p>Use these product routes as a starting point. Confirm the exact listing, selected option, price and availability on the destination page.</p><p>These are discovery links, not a claim of current stock, independent testing or verified warehouse QC.</p></section>'+products()
BODY['products']+='<section class="section"><h2>Browse by category</h2><div class="chips">'+''.join(f'<a href="https://cnfanssp.com/{slug}/" rel="nofollow sponsored">{name} ↗</a>' for slug,name in [('shoes','Shoes'),('hoodies-sweaters','Hoodies'),('t-shirts','T-shirts'),('jackets','Jackets'),('pants-shorts','Pants and shorts'),('accessories','Accessories'),('AllProducts','All products')])+'</div></section><div class="article-grid">'+card('hoobuy-product-link-verification-taobao-1688-weidian-2026')+card('hoobuy-shoes-spreadsheet-size-qc-fields-2026')+card('hoobuy-hoodie-spreadsheet-fabric-measurements-weight-2026')+'</div>'
P['products'].update(title='HooBuy Product Links & Finds: Shoes, Hoodies & More',description='Browse HooBuy product research routes for shoes, hoodies, bags and clothing. Pair each find with current price, exact variant, sizing and QC checks.')
BODY['guides']='<section class="page-intro"><p class="eyebrow">The buying guide library</p><h1>HooBuy Spreadsheet, QC & Shipping Guides</h1><p>Choose the guide for your next decision: verify a link, compare measurements, inspect QC photos or prepare a parcel budget.</p></section><h2>New practical guides</h2><div class="article-grid">'+''.join(card(s) for s in NEW)+'</div><section class="section"><h2>All guides</h2><div class="article-grid">'+''.join(card(s) for s in ARTICLES if s not in NEW)+'</div></section>'
P['guides'].update(title='HooBuy Guides: Product Links, Spreadsheet, QC & Shipping',description='Read complete HooBuy guides for product links, spreadsheets, shoe and clothing sizes, QC photos, shipping estimates and a total-cost budget.')
for slug in ARTICLES:
 a=P[slug];soup=BeautifulSoup(a['body'].replace('https://cnfanshp.com','https://cnfanssp.com'),'html.parser')
 for holder in soup.select('[data-weight-tool]'):holder.replace_with(BeautifulSoup(CALCULATOR,'html.parser'))
 toc=[]
 for i,h in enumerate(soup.find_all('h2')):
  hid=h.get('id') or 'section-'+str(i+1);h['id']=hid;toc.append(f'<li><a href="#{hid}">{e(h.get_text())}</a></li>')
 related=[s for s in list(NEW)+['hoobuy-spreadsheet-guide'] if s!=slug]
 BODY[slug]=f'<nav class="breadcrumbs"><a href="/">Home</a> / <a href="/guides">Guides</a></nav><article class="article"><header><p class="eyebrow">Independent practical guide</p><h1>{e(a["title"])}</h1><p class="meta">Updated: <time datetime="{DATE}">{DATE}</time> · hoobuys.org Editorial</p></header><nav class="toc" aria-label="On this page"><details><summary>On this page</summary><ol>{"".join(toc)}</ol></details></nav>{soup}<section class="related"><h2>Continue reading</h2><ul>'+''.join(f'<li><a href="/{s}">{e(P[s]["title"])}</a></li>' for s in related)+'</ul><a class="button" href="/products">Explore product links →</a></section></article>'
for slug in ['faq','privacy','terms']:
 BODY[slug]=f'<article class="article"><h1>{e(P[slug]["title"].split(" | ")[0])}</h1>{P[slug]["body"]}</article>'
BODY['languages']='<article class="article"><h1>Read in your language</h1><p>Every language includes the same guides and product routes. Use the language menu on any page to switch to its equivalent.</p><div class="language-list">'+''.join(f'<a lang="{l}" hreflang="{l}" href="{route(l,"index")}">{NAMES[l]}</a>' for l in LANGS)+'</div></article>'
BODY['404']='<section class="page-intro"><h1>Page not found</h1><p>The requested page is unavailable. Browse the current guides or return to the home page.</p><a class="button" href="/guides">Browse guides</a></section>'
P['404'].update(title='Page not found | hoobuys.org',description='Find the current HooBuy guides and product research pages.')

for slug in PAGES:
 if slug!='index':BODY[slug]='<div class="search-strip">'+SEARCH+'</div>'+BODY[slug]

assets={}
for name in ['styles.css','site.js']:
 data=(B/'assets'/name).read_bytes();stem,ext=name.rsplit('.',1);hashed=stem+'.'+hashlib.sha256(data).hexdigest()[:12]+'.'+ext
 (B/'assets'/hashed).write_bytes(data);assets[name]='/assets/'+hashed

def document(slug):
 a=P[slug];url=ORIGIN+route('en',slug);article=a.get('article',False)
 graph=[{'@type':'WebPage','@id':url,'url':url,'name':a['title'],'description':a['description'],'inLanguage':'en'}]
 if article:graph += [{'@type':'Article','headline':a['title'],'description':a['description'],'datePublished':a['published'],'dateModified':DATE,'inLanguage':'en','mainEntityOfPage':url,'author':{'@type':'Organization','name':'hoobuys.org Editorial'},'publisher':{'@type':'Organization','name':'hoobuys.org'}},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':ORIGIN+'/'},{'@type':'ListItem','position':2,'name':'Guides','item':ORIGIN+'/guides'},{'@type':'ListItem','position':3,'name':a['title'],'item':url}]}]
 if slug=='index':graph.append({'@type':'WebSite','name':'hoobuys.org','url':ORIGIN+'/','inLanguage':LANGS})
 nav=''.join(f'<a href="/{s if s!="index" else ""}"'+(' aria-current="page"' if s==slug else '')+f'>{label}</a>' for s,label in [('index','Home'),('products','Product links'),('guides','Guides'),('faq','FAQ')])
 switches=''.join(f'<a lang="{l}" hreflang="{l}" href="{route(l,slug if slug!="404" else "index")}"'+(' aria-current="page"' if l=='en' else '')+f'>{NAMES[l]}</a>' for l in LANGS)
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(a['title'])}</title><meta name="description" content="{e(a['description'],quote=True)}"><meta name="robots" content="{'noindex,follow' if slug=='404' else 'index,follow,max-image-preview:large'}"><meta name="site-revision" content="2026-10-12-org-multilingual"><link rel="canonical" href="{url}"><meta property="og:type" content="{'article' if article else 'website'}"><meta property="og:title" content="{e(a['title'],quote=True)}"><meta property="og:description" content="{e(a['description'],quote=True)}"><meta property="og:url" content="{url}"><meta property="og:site_name" content="hoobuys.org"><link rel="stylesheet" href="{assets['styles.css']}"><script async src="https://www.googletagmanager.com/gtag/js?id=G-Q60K7ELE45"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-Q60K7ELE45');</script><script defer src="{assets['site.js']}"></script><script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False)}</script></head><body><a class="skip" href="#main">Skip to content</a><header class="top"><div class="wrap bar"><a class="brand" href="/">hoobuys<span>.</span>org</a><nav class="nav" aria-label="Main navigation">{nav}</nav><details class="language-picker"><summary>English</summary><nav aria-label="Language">{switches}</nav></details></div></header><main id="main" class="wrap">{BODY[slug]}</main><footer class="foot"><div class="wrap"><p class="footer-brand">hoobuys.org</p><p>Independent product-discovery and buying guides. This site is not HooBuy and does not process orders. Check current listing and platform information before purchase.</p><nav><a href="/privacy">Privacy</a><a href="/terms">Terms</a><a href="/languages">Languages</a><a href="/sitemap.xml">Sitemap</a></nav></div></footer></body></html>'''

EN={slug:document(slug) for slug in PAGES}
(S/'english-pages.json').write_text(json.dumps(EN,ensure_ascii=False,indent=2))
# Cached sentence translations are generated offline. They are not a browser dependency.
from translate import render_localized
MANIFEST=[]
for lang in (LANGS if '--all' in sys.argv else ['en']):
 cache=json.loads((S/'translations'/(lang+'.json')).read_text()) if lang!='en' else {}
 for slug,doc in EN.items():
  rendered=render_localized(doc,lang,slug,cache,LANGS,NAMES,route)
  dest=B/('' if lang=='en' else lang)/(slug+'.html');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(rendered)
  if slug!='404':MANIFEST.append({'lang':lang,'slug':slug,'url':ORIGIN+route(lang,slug)})
ns='http://www.sitemaps.org/schemas/sitemap/0.9';xh='http://www.w3.org/1999/xhtml';ET.register_namespace('',ns);ET.register_namespace('xhtml',xh)
root=ET.Element('{'+ns+'}urlset')
for row in MANIFEST:
 el=ET.SubElement(root,'{'+ns+'}url');ET.SubElement(el,'{'+ns+'}loc').text=row['url'];ET.SubElement(el,'{'+ns+'}lastmod').text=DATE
 for lang in LANGS+['x-default']:ET.SubElement(el,'{'+xh+'}link',rel='alternate',hreflang=lang,href=ORIGIN+route('en' if lang=='x-default' else lang,row['slug']))
(B/'sitemap.xml').write_bytes(ET.tostring(root,encoding='utf-8',xml_declaration=True));(B/'sitemap.txt').write_text('\n'.join(x['url'] for x in MANIFEST)+'\n')
(B/'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /_src/\nSitemap: https://hoobuys.org/sitemap.xml\n')
(S/'manifest.json').write_text(json.dumps({'date':DATE,'languages':LANGS,'articles_per_language':len(ARTICLES),'pages':MANIFEST},indent=2))
print('Built',len(MANIFEST),'indexable pages;',len(ARTICLES),'articles per language')

(B/"_worker.js").write_text((S/"worker-template.js").read_text().replace("__PAGES__",json.dumps(PAGES)))
