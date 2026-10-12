"""Build the eight-language editorial section and keep static routes in sync."""
from pathlib import Path
import re, json, hashlib, html as esc
from lxml import html, etree
from ui import LANGS, NAMES, UI, NOTES

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]/'hipobuys-store'
SITE='https://hipobuys.store'
STORE='https://cnfanshp.com'
DATE='2026-10-12'
SLUGS={
 'tracking':'hipobuy-order-status-tracking-guide',
 'warehouse':'hipobuy-warehouse-location-forwarding-address',
 'calculator':'hipobuy-shipping-calculator-weight-dimensions',
 'rehearsal':'hipobuy-rehearsal-parcel-volumetric-weight',
 'time':'hipobuy-shipping-time-seller-warehouse-delivery',
 'sizing':'hipobuy-size-guide-clothing-shoes',
 'sneakers':'hipobuy-sneaker-finds-sizing-qc',
}
ORDER=['time','sizing','sneakers','tracking','warehouse','calculator','rehearsal']
NEW={'time','sizing','sneakers'}
LEGACY=json.loads((HERE/'legacy.json').read_text())
PRODUCTS=json.loads((HERE/'products.json').read_text())
DATA={}
E=lambda s:esc.escape(str(s),quote=True)
def parse_content(text):
    result={}
    for chunk in text.split('@@ ')[1:]:
        lines=chunk.strip().splitlines(); key=lines.pop(0)
        title,desc,intro=lines[:3]; sections=[]
        for line in lines[3:]:
            if line.startswith('## '): sections.append({'title':line[3:],'paragraphs':[]})
            elif line.strip(): sections[-1]['paragraphs'].append(line)
        result[key]={'title':title,'desc':desc,'intro':intro,'sections':sections}
    assert set(result)==set(SLUGS)
    return result
for lang in LANGS: DATA[lang]=parse_content((HERE/'content'/f'{lang}.txt').read_text())
def home(lang):return '/' if lang=='en' else f'/{lang}/'
def hub(lang):return '/articles' if lang=='en' else f'/{lang}/articles/'
def route(lang,key):return '/'+SLUGS[key] if lang=='en' else f'/{lang}/{SLUGS[key]}/'
def target(path):return ROOT/('index.html' if path=='/' else path.strip('/')+'/index.html' if path.endswith('/') else path[1:]+'.html')
def write(path,text):
    file=target(path);file.parent.mkdir(parents=True,exist_ok=True);file.write_text(text)
def alts(urls):return ''.join(f'<link rel="alternate" hreflang="{l}" href="{SITE+urls[l]}">' for l in LANGS)+f'<link rel="alternate" hreflang="x-default" href="{SITE+urls["en"]}">'
def langbar(lang,urls):
    return '<nav class="languages" aria-label="Language">'+''.join(f'<a href="{urls[l]}" lang="{l}" hreflang="{l}"'+(' aria-current="page"' if l==lang else '')+f'>{name}</a>' for l,name in zip(LANGS,NAMES))+'</nav>'
CSS=(HERE/'editorial.css').read_text()
BASECSS=(ROOT/'assets/seo-article.css').read_text()
# The original stylesheet remains available for historical pages.
combined=BASECSS+'\n'+CSS
css_name='editorial-'+hashlib.sha256(combined.encode()).hexdigest()[:12]+'.css'
(ROOT/'assets'/css_name).write_text(combined)
JS=(HERE/'site.js').read_text()
js_name='site-'+hashlib.sha256(JS.encode()).hexdigest()[:12]+'.js'
(ROOT/'assets'/js_name).write_text(JS)
TAG='<script async src="https://www.googletagmanager.com/gtag/js?id=G-N31DJZNW37"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag("js",new Date());gtag("config","G-N31DJZNW37");</script>'
def frame(lang,path,title,desc,body,urls=None,schema=None):
    u=UI[lang]
    alternates=alts(urls) if urls else ''
    switch=langbar(lang,urls) if urls else ''
    data=json.dumps(schema or {'@context':'https://schema.org','@type':'WebPage','name':title,'url':SITE+path,'inLanguage':lang},ensure_ascii=False).replace('</','<\\/')
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{SITE+path}">{alternates}<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{SITE+path}"><link rel="stylesheet" href="/assets/{css_name}"><link rel="stylesheet" href="/assets/brand-logo.css">{TAG}<script defer src="/assets/{js_name}"></script><script type="application/ld+json">{data}</script></head><body><header class="topbar"><a class="brand brand-logo" href="{home(lang)}" aria-label="HipoBuys Store"><img src="/assets/hipobuy-logo.png" alt="HipoBuys Store" width="488" height="112"></a><button class="menu" aria-expanded="false" aria-controls="nav">{u['menu']}</button><nav class="nav" id="nav"><a href="{home(lang)}">{u['home']}</a><a href="{hub(lang)}">{u['articles']}</a><a href="{STORE}/AllProducts/" target="_blank" rel="nofollow sponsored noopener">{u['products']}</a></nav></header><main>{switch}{body}</main><footer class="footer"><div class="footer-inner"><div><h2>HipoBuys Store</h2><p>{u['independent']}</p></div><div><h3>{u['related']}</h3><a href="{hub(lang)}">{u['all']}</a><a href="https://hipobuy.com/" target="_blank" rel="noopener">{u['official']}</a></div><div><h3>{u['privacy']}</h3><a href="/privacy">{u['privacy']} (English)</a><p>{u['external']}</p></div></div></footer></body></html>'''
def cards(lang,keys):
    u=UI[lang]
    return '<div class="article-grid">'+''.join(f'<a class="article-card" href="{route(lang,k)}"><h2>{E(DATA[lang][k]["title"])}</h2><p>{E(DATA[lang][k]["desc"])}</p><b>{u["read"]} →</b></a>' for k in keys)+'</div>'
def source_box(lang,key):
    u=UI[lang]
    links=[('https://hipobuy.com/',u['official'])]
    if key in ('calculator','rehearsal','time'):links.append(('https://hipobuy.com/estimation',u['estimator']))
    if key in ('calculator','rehearsal'):links.append(('https://www.dhl.com/discover/en-gb/ship-with-dhl/products-and-services/weight-and-dimensions','DHL — '+u['volume']))
    if key in ('sizing','sneakers'):links.append(('https://www.nike.com/size-fit/mens-footwear','Nike — '+DATA[lang]['sizing']['title'].split(':')[0]))
    return f'<section class="source-note"><h2>{u["sources"]}</h2><p>{u["independent"]}</p><ul>'+''.join(f'<li><a href="{E(url)}" target="_blank" rel="noopener">{E(label)}</a></li>' for url,label in links)+'</ul></section>'
def calculator(lang):
    u=UI[lang]
    fields=[('length',40),('width',30),('height',25),('weight',3),('divisor',5000)]
    return f'<section class="callout weight-tool"><h2>{u["calc"]}</h2><p>{u["calc_note"]}</p><form data-calculator data-volume="{E(u["volume"])}" data-billable="{E(u["billable"])}" data-invalid="{E(u["invalid"])}"><div class="calc-fields">'+''.join(f'<label>{u[k]}<input type="number" name="{k}" min="0.01" step="any" value="{v}" required inputmode="decimal"></label>' for k,v in fields)+f'</div><button type="submit">{u["calculate"]}</button><output aria-live="polite"></output></form></section>'
def article(lang,key):
    u=UI[lang];d=DATA[lang][key];path=route(lang,key)
    contents='<nav class="toc" aria-label="'+u['contents']+'"><strong>'+u['contents']+'</strong><ol>'+''.join(f'<li><a href="#s{i}">{E(s["title"])}</a></li>' for i,s in enumerate(d['sections'],1))+'</ol></nav>'
    sections=''.join(f'<section id="s{i}"><h2>{E(s["title"])}</h2>'+''.join(f'<p>{E(p)}</p>' for p in s['paragraphs'])+'</section>' for i,s in enumerate(d['sections'],1))
    tool=calculator(lang) if key=='calculator' else ''
    direct=f'<p><a href="{route(lang,"calculator")}">{u["calculator_link"]} →</a></p>' if key=='rehearsal' else ''
    shoes=f'<div class="callout"><a href="{STORE}/shoes/" target="_blank" rel="nofollow sponsored noopener">{u["shoe_category"]} →</a><p>{u["external"]}</p></div>' if key=='sneakers' else ''
    related={'tracking':['time','warehouse','rehearsal'],'warehouse':['tracking','sizing','calculator'],'calculator':['rehearsal','time','sneakers'],'rehearsal':['calculator','warehouse','time'],'time':['tracking','warehouse','calculator'],'sizing':['sneakers','warehouse','tracking'],'sneakers':['sizing','calculator','rehearsal']}[key]
    body=f'<section class="hero"><div class="hero-inner"><p class="eyebrow">{u["updated"]}</p><h1>{E(d["title"])}</h1><p class="dek">{E(d["desc"])}</p></div></section><div class="layout"><article class="article"><p class="quick-answer">{E(d["intro"])}</p>{tool}{contents}{sections}{direct}{shoes}{source_box(lang,key)}</article><aside class="sidebar"><div class="side-card"><h2>{u["related"]}</h2>'+''.join(f'<a href="{route(lang,k)}">{E(DATA[lang][k]["title"])}</a>' for k in related)+f'</div><div class="side-card"><p>{u["external"]}</p><a class="button" href="{STORE}/AllProducts/" target="_blank" rel="nofollow sponsored noopener">{u["browse"]}</a></div></aside></div>'
    schema={'@context':'https://schema.org','@graph':[{'@type':'Article','headline':d['title'],'description':d['desc'],'datePublished':DATE if key in NEW else '2026-09-11','dateModified':DATE,'author':{'@type':'Organization','name':'HipoBuys Store Editorial'},'publisher':{'@type':'Organization','name':'HipoBuys Store'},'mainEntityOfPage':SITE+path,'inLanguage':lang},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':u['home'],'item':SITE+home(lang)},{'@type':'ListItem','position':2,'name':u['articles'],'item':SITE+hub(lang)},{'@type':'ListItem','position':3,'name':d['title'],'item':SITE+path}]}]}
    write(path,frame(lang,path,d['title'],d['desc'],body,{l:route(l,key) for l in LANGS},schema))

# Preserve the existing root catalogue; remove misleading freshness claims from new previews.
def product_cards(lang):
    u=UI[lang]
    return f'<section class="hub"><h2>{u["products"]}</h2><p>{u["product_note"]}</p><div class="product-previews">'+''.join(f'<a class="product-preview" href="{E(p["url"])}" target="_blank" rel="nofollow sponsored noopener"><img src="{E(p["image"])}" alt="{E(p["name"])}" width="600" height="450" loading="lazy"><h3>{E(p["name"])}</h3></a>' for p in PRODUCTS[:4])+'</div></section>'
def search(lang):
    u=UI[lang]
    return f'<form class="product-search" action="{STORE}/search.html" method="get"><label for="keywords">{u["search_label"]}</label><div><input id="keywords" name="keywords" type="search" required maxlength="100"><input name="channelid" type="hidden" value="2"><button type="submit">{u["search"]}</button></div></form>'
def topic_type(path):
    if any(t in path for t in ['w2c','link-w2c','linki-w2c','links-w2c','enlaces-w2c','liens-w2c']):return 0
    if any(t in path for t in ['qc','zdjecia','foto']):return 1
    if any(t in path for t in ['fees','kosten','frais','tarifas','costi','koszty','taxas']):return 2
    if any(t in path for t in ['shipping','versand','livraison','envio','spedizione','wysylka','verzending']):return 3
    return 4
TYPED={lang:{topic_type(d['path']):d for d in LEGACY[lang]} for lang in LANGS}
assert all(len(x)==5 for x in TYPED.values())
def topic_cards(lang):
    return '<div class="article-grid">'+''.join(f'<a class="article-card" href="{d["path"]}"><h2>{E(d["title"])}</h2><p>{E(d["desc"])}</p></a>' for d in LEGACY[lang])+'</div>'

# Keep older English articles reachable without representing them as translated pages.
archive=[]
for p in sorted(ROOT.glob('*.html')):
    if p.stem in SLUGS.values() or p.stem in ['index','articles','404','privacy','disclaimer','imprint','languages','products','categories','guides','faq']:continue
    doc=html.parse(str(p)); heads=doc.xpath('//h1')
    if heads:archive.append((f'/{p.stem}',heads[0].text_content()))
for lang in LANGS:
    u=UI[lang]
    for key in SLUGS: article(lang,key)
    path=home(lang)
    body=f'<section class="hero"><div class="hero-inner"><h1>{u["home_title"]}</h1><p class="dek">{u["home_desc"]}</p>{search(lang)}<p class="meta">{u["external"]}</p></div></section><section class="hub"><h2>{u["latest"]}</h2>{cards(lang,ORDER[:6])}<p><a href="{hub(lang)}">{u["all"]} →</a></p></section>{product_cards(lang)}<section class="hub"><h2>{u["legacy"]}</h2>{topic_cards(lang)}</section>'
    write(path,frame(lang,path,u['home_title'],u['home_desc'],body,{l:home(l) for l in LANGS}))
    path=hub(lang)
    body=f'<section class="hub"><div class="hub-head"><h1>{u["all"]}</h1><p>{u["home_desc"]}</p></div>{cards(lang,ORDER)}<h2>{u["legacy"]}</h2>{topic_cards(lang)}'
    if lang=='en':body+=f'<h2>{u["archive"]}</h2><ul>'+''.join(f'<li><a href="{url}">{E(title)}</a></li>' for url,title in archive)+'</ul>'
    body+='</section>'
    write(path,frame(lang,path,u['articles']+' | HipoBuys Store',u['home_desc'],body,{l:hub(l) for l in LANGS}))
    for t,d in TYPED[lang].items():
        keys={0:['sneakers','sizing','warehouse'],1:['sizing','sneakers','tracking'],2:['calculator','rehearsal','warehouse'],3:['time','calculator','tracking'],4:['calculator','rehearsal','sneakers']}[t]
        body=f'<section class="hero"><div class="hero-inner"><h1>{E(d["title"])}</h1><p class="dek">{E(d["desc"])}</p></div></section><section class="hub"><p class="topic-note">{NOTES[lang][t]}</p><h2>{u["related"]}</h2>{cards(lang,keys)}{source_box(lang,"calculator" if t in [2,3,4] else "sizing")}</section>'
        write(d['path'],frame(lang,d['path'],d['title'],d['desc'],body,{l:TYPED[l][t]['path'] for l in LANGS}))

# /en/ was a different English homepage. It now redirects to the existing English root.
(ROOT/'en/index.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex"><link rel="canonical" href="https://hipobuys.store/"><meta http-equiv="refresh" content="0;url=/"><title>HipoBuys Store</title></head><body><a href="/">HipoBuys Store</a></body></html>')

# Update old root pages too: links, canonical paths, tracking asset and discovery links.
for file in ROOT.rglob('*.html'):
    text=file.read_text()
    text=re.sub(r'(href|action)=("|\')https://(?:www\.)?cnfanssp\.com',r'\1=\2https://cnfanshp.com',text)
    text=re.sub(r'<script[^>]+src=["\']/assets/(?:site-analytics\.js|site-[a-f0-9]+\.js)["\'][^>]*></script>',f'<script defer src="/assets/{js_name}"></script>',text)
    text=re.sub(r'(https://hipobuys\.store/[^"<>]*?)\.html(?=["<])',r'\1',text)
    if not html.fromstring(text).xpath('//link[@rel="canonical"]'):
        rel=file.relative_to(ROOT).as_posix()
        canonical='/' if rel=='index.html' else '/'+rel[:-10] if rel.endswith('/index.html') else '/'+rel[:-5]
        text=re.sub(r'</head>',f'<link rel="canonical" href="{SITE+canonical}"></head>',text,flags=re.I)
    if file.stem=='languages' and not html.fromstring(text).xpath('//meta[@name="description"]'):
        text=re.sub(r'</head>','<meta name="description" content="Read Hipobuy product, warehouse, sizing and shipping guides in English, German, French, Spanish, Italian, Polish, Portuguese and Dutch."></head>',text,flags=re.I)
    if file.parent==ROOT and file.stem not in [*SLUGS.values(),'index','articles','404']:
        text=re.sub(r'<section data-editorial-links>.*?</section>','',text,flags=re.S)
        text=text.replace('</main>',f'<section data-editorial-links class="hub"><h2>{UI["en"]["latest"]}</h2>{cards("en",["time","sizing","sneakers"])}</section></main>')
    file.write_text(text)

# Correct the previous privacy statement, which said analytics might be added in future.
p=ROOT/'privacy.html';text=p.read_text()
text=text.replace('HipoBuys.store is a static informational website. If analytics, forms or tracking tools are added later, this policy should be updated.','HipoBuys Store uses Google Analytics 4 (measurement ID G-N31DJZNW37) to understand page visits and interactions such as product-link clicks and calculator use. Google Analytics can use browser identifiers and cookies. Product links lead to an independent external website and may contain campaign parameters identifying this referring site and page. Our custom search event does not send the words entered in the product search to Analytics; the search form sends them to the external product site so it can return results. Do not enter personal account or payment information into the product search. Browser privacy controls and content blockers may restrict analytics. See Google’s privacy information at https://policies.google.com/privacy for information about Google’s processing. This site does not provide a checkout or collect order payments.')
p.write_text(text)

# Enumerate the deployable HTML rather than maintaining an incomplete hand-written list.
pages=[]
for p in ROOT.rglob('*.html'):
    rel=p.relative_to(ROOT).as_posix()
    if rel in ['404.html','en/index.html']:continue
    path='/' if rel=='index.html' else '/'+rel[:-10] if rel.endswith('/index.html') else '/'+rel[:-5]
    pages.append(path)
pages.sort()
generated={route(l,k) for l in LANGS for k in SLUGS}|{home(l) for l in LANGS}|{hub(l) for l in LANGS}|{x['path'] for a in LEGACY.values() for x in a}
urls_by_path={}
for k in SLUGS:
    mapping={l:route(l,k) for l in LANGS}
    for p in mapping.values():urls_by_path[p]=mapping
for fn in [home,hub]:
    mapping={l:fn(l) for l in LANGS}
    for p in mapping.values():urls_by_path[p]=mapping
for t in range(5):
    mapping={l:TYPED[l][t]['path'] for l in LANGS}
    for p in mapping.values():urls_by_path[p]=mapping
ns='http://www.sitemaps.org/schemas/sitemap/0.9'; xhtml='http://www.w3.org/1999/xhtml'
tree=etree.Element('{'+ns+'}urlset',nsmap={None:ns,'xhtml':xhtml})
for path in pages:
    item=etree.SubElement(tree,'{'+ns+'}url');etree.SubElement(item,'{'+ns+'}loc').text=SITE+path
    if path in generated:etree.SubElement(item,'{'+ns+'}lastmod').text=DATE
    if path in urls_by_path:
        for l,p in {**urls_by_path[path],'x-default':urls_by_path[path]['en']}.items():
            etree.SubElement(item,'{'+xhtml+'}link',rel='alternate',hreflang=l,href=SITE+p)
xml=etree.tostring(tree,encoding='UTF-8',xml_declaration=True,pretty_print=True)
for name in ['sitemap.xml','google-sitemap.xml','sitemap-extra.xml']:(ROOT/name).write_bytes(xml)
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: https://hipobuys.store/sitemap.xml\n')
worker=(HERE/'worker.js').read_text().replace('__PAGES__',json.dumps(pages,separators=(',',':')))
assets=['/'+p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and (p.suffix in ['.css','.js','.png','.webp','.jpg','.svg'] and p.name!='_worker.js' or p.name in ['robots.txt','sitemap.xml','google-sitemap.xml','sitemap-extra.xml'])]
worker=worker.replace('__ASSETS__',json.dumps(sorted(assets),separators=(',',':'))).replace('__SLUGS__',json.dumps(list(SLUGS.values())))
(ROOT/'_worker.js').write_text(worker)
(HERE/'routes.json').write_text(json.dumps({'pages':pages,'article_urls':sorted(route(l,k) for l in LANGS for k in SLUGS),'css':css_name,'js':js_name},indent=2))
print(f'Built {len(SLUGS)*len(LANGS)} articles across {len(LANGS)} languages; {len(pages)} canonical routes.')
