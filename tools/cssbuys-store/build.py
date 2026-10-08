"""Render the static cssbuys.store site; run after reviewing article translations."""
import html
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

BASE = Path(__file__).resolve().parent
OUT = BASE.parents[1] / 'cssbuys-store'
DOMAIN = 'https://cssbuys.store'
MAIN = 'https://www.cnfanssp.com'
DATE = '2026-10-08'
LOCALES = json.loads((BASE / 'locales.json').read_text())
META = json.loads((BASE / 'articles.json').read_text())
TITLES = json.loads((BASE / 'titles.json').read_text())
UI = json.loads((BASE / 'ui.json').read_text())
OPENINGS = json.loads((BASE / 'reviewed-openings.json').read_text())
PRODUCTS = json.loads((BASE / 'products.json').read_text())
BY_ID = {x['id']: x for x in PRODUCTS}
FEATURED = ['3400', '3401', '3402', '3399']
PRIORITY = ['cssbuy-shoe-sizing-qc-checklist', 'qc-guide', 'cssbuy-spreadsheet', 'cssbuy-shipping-calculator-estimate', 'cssbuy-fees-payment-total-cost', 'cssbuy-shoe-finds-price-sizing', 'cssbuy-hoodie-finds-sizing-fabric']
ORDER = PRIORITY + [s for s in META if s not in PRIORITY]
CATEGORY_PATHS = ['shoes', 't-shirts', 'hoodies-sweaters', 'jackets', 'pants-shorts', 'Jersey', 'headwear', 'accessories', 'electronics', 'short-sets', 'other-stuff']
SITEMAP = []

def esc(x): return html.escape(str(x), quote=True)
def prefix(lang): return '' if lang == 'en' else '/' + lang
def path(lang, suffix='/'): return prefix(lang) + suffix
def url(lang, suffix='/'): return DOMAIN + path(lang, suffix)
def data(x): return json.dumps(x, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
def sentences(s): return re.split(r'(?<=[.!?])\s+(?=[A-Z“"0-9])', s)

def translator(lang):
    cache = {} if lang == 'en' else json.loads((BASE / f'ui.{lang}.json').read_text())
    def t(s):
        if lang == 'en': return s
        if s not in cache: raise ValueError(f'Missing {lang} translation: {s}')
        return cache[s]
    return t

def language_links(lang, suffix):
    return '<nav class="language-switch" aria-label="'+esc(LOCALES[lang]['languages'])+'">' + ''.join(f'<a href="{path(code, suffix)}" lang="{code}" hreflang="{code}"'+(' aria-current="page"' if code == lang else '')+f'>{esc(info["name"])}</a>' for code, info in LOCALES.items()) + '</nav>'

def alternates(suffix):
    return ''.join(f'<link rel="alternate" hreflang="{code}" href="{url(code,suffix)}">' for code in LOCALES) + f'<link rel="alternate" hreflang="x-default" href="{url("en",suffix)}">'

def head(lang, suffix, title, description, schemas, image=None, index=True):
    return f'''<!doctype html><html lang="{lang}"><head data-store-tracking="inline">
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(description)}">
<meta name="robots" content="{'index' if index else 'noindex'},follow"><link rel="canonical" href="{url(lang,suffix)}">
{alternates(suffix) if index else ''}<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{url(lang,suffix)}"><meta property="og:type" content="{'article' if '/guides/' in suffix and not suffix.endswith('/') else 'website'}">
{f'<meta property="og:image" content="{DOMAIN}{image}">' if image else ''}<meta name="twitter:card" content="{'summary_large_image' if image else 'summary'}">
<link rel="stylesheet" href="/assets/store.css"><script type="application/ld+json">{data(schemas)}</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-K66FDYFQEX"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-K66FDYFQEX');</script><script defer src="/assets/site-tracking.js"></script>
</head><body><a class="skip-link" href="#main">{esc(LOCALES[lang]['skip'])}</a>'''

def header(lang, suffix):
    l = LOCALES[lang]
    return f'''<header class="site-header"><div class="wrap header-row"><a class="brand" href="{path(lang)}">CSSBuys<span> Store</span></a><nav class="main-nav" aria-label="{esc(l['navLabel'])}"><a href="{path(lang)}">{l['home']}</a><a href="{path(lang) }#products">{l['products']}</a><a href="{path(lang,'/guides/')}">{l['guides']}</a><a href="{path(lang,'/faq')}">{l['faq']}</a></nav></div><div class="wrap">{language_links(lang,suffix)}</div></header>'''

def footer(lang):
    l = LOCALES[lang]
    return f'''<footer class="site-footer"><div class="wrap"><a class="brand" href="{path(lang)}">CSSBuys<span> Store</span></a><p>{l['footer']}</p><p class="disclosure">{l['independent']}</p><div class="footer-links"><a href="{path(lang,'/guides/')}">{l['guides']}</a><a href="{path(lang,'/faq')}">{l['faq']}</a><a href="/languages">{l['languages']}</a><a href="/sitemap.xml">Sitemap</a></div></div></footer></body></html>'''

def page_file(lang, suffix):
    local = path(lang,suffix).lstrip('/')
    return OUT / (local + 'index.html' if suffix.endswith('/') else local + '.html')

def write(lang, suffix, content, index=True):
    target = page_file(lang,suffix);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content)
    if index: SITEMAP.append((url(lang,suffix),suffix))

def main_url(p, location, lang):
    return f'{MAIN}/AllProducts/{p["id"]}.html?utm_source=cssbuys.store&utm_medium=referral&utm_campaign={location}&utm_content={lang}_{p["id"]}'

def product_name(p, lang, t):
    # Names identify the source catalogue. Translate descriptive words only.
    return t(p['title'])

def product_card(p, lang, t, featured=False, location='product_grid'):
    l=LOCALES[lang];name=product_name(p,lang,t)
    return f'''<article class="product-card{' compact' if featured else ''}"><a class="product-link" href="{esc(main_url(p,location,lang))}" target="_blank" rel="noopener" data-location="{location}" data-product-id="{p['id']}"><img src="/assets/products/{p['id']}.webp" alt="{esc(name)}" width="600" height="600" {'fetchpriority="high"' if featured and p['id']=='3400' else 'loading="lazy"'} decoding="async"><div class="product-copy"><h3>{esc(name)}</h3><span class="price">US${p['price']}</span><span class="product-cta">{l['open']} <span aria-hidden="true">↗</span></span></div></a>{'' if featured else f'<a class="detail-link" href="{path(lang,"/products/"+p["id"])}">{l["productGuide"]}</a>'}</article>'''

def article_meta(lang):
    m = META if lang=='en' else json.loads((BASE / f'articles.{lang}.json').read_text())
    for slug,title in TITLES.get(lang,{}).items():m[slug]['title']=title
    return m

def guide_card(slug,lang,meta):
    l=LOCALES[lang];m=meta[slug]
    return f'''<a class="guide-card" href="{path(lang,'/guides/'+slug)}"><span class="eyebrow">{l['new'] if m['status']=='new' else l['guides']}</span><h3>{esc(m['title'])}</h3><p>{esc(m['description'])}</p><span class="text-link">{l['read']} →</span></a>'''

def breadcrumb(lang,suffix,name):
    nodes=[{'@type':'ListItem','position':1,'name':LOCALES[lang]['home'],'item':url(lang)}]
    if '/guides/' in suffix and suffix!='/guides/':nodes.append({'@type':'ListItem','position':2,'name':LOCALES[lang]['guides'],'item':url(lang,'/guides/')})
    nodes.append({'@type':'ListItem','position':len(nodes)+1,'name':name,'item':url(lang,suffix)})
    return {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':nodes}

def home(lang,t,meta):
    l=LOCALES[lang];suffix='/'
    schemas=[{'@context':'https://schema.org','@type':'WebSite','url':url(lang),'name':'CSSBuys Store','inLanguage':lang},{'@context':'https://schema.org','@type':'ItemList','name':l['products'],'itemListElement':[{'@type':'ListItem','position':i+1,'name':product_name(p,lang,t),'url':url(lang,'/products/'+p['id'])} for i,p in enumerate(PRODUCTS)]}]
    content=head(lang,suffix,l['homeTitle'],l['homeLead'],schemas,'/assets/products/3400.webp')+header(lang,suffix)
    content+=f'''<main id="main"><section class="hero"><div class="wrap hero-grid"><div><p class="eyebrow">CSSBuys Store</p><h1>{l['homeTitle']}</h1><p class="lead">{l['homeLead']}</p><form class="hero-search" action="{MAIN}/search.html" method="get" role="search" aria-label="{esc(l['searchLabel'])}" data-main-search><label for="product-keywords">{l['searchLabel']}</label><div class="search-row"><input type="search" id="product-keywords" name="keywords" placeholder="{esc(l['placeholder'])}" required maxlength="120"><input type="hidden" name="channelid" value="2"><button type="submit">{l['search']}</button></div><p class="hint">{l['searchHint']}</p></form></div><aside class="featured-panel"><h2>{l['featured']}</h2><div class="featured-grid">{''.join(product_card(BY_ID[i],lang,t,True,'hero_products') for i in FEATURED)}</div></aside></div></section>
<section class="section" id="categories"><div class="wrap"><h2>{l['categories']}</h2><p>{t(UI['categoryIntro'])}</p><div class="category-grid">{''.join(f'<a href="{MAIN}/{route}/" target="_blank" rel="noopener" data-location="categories">{esc(t(name))} ↗</a>' for name,route in zip(UI['categories'],CATEGORY_PATHS))}</div></div></section>
<section class="section" id="products"><div class="wrap"><h2>{l['products']}</h2><p class="hint">{l['checked']}</p><div class="product-grid">{''.join(product_card(p,lang,t) for p in PRODUCTS)}</div><p class="hint">{l['productNote']}</p></div></section>
<section class="section guide-section"><div class="wrap"><h2>{l['guides']}</h2><div class="guide-grid">{''.join(guide_card(s,lang,meta) for s in PRIORITY)}</div><a class="button secondary" href="{path(lang,'/guides/')}">{l['allGuides']}</a></div></section>
<section class="section"><div class="wrap"><h2>{t(UI['howTitle'])}</h2><ol class="steps"><li>{t(UI['how1'])}</li><li>{t(UI['how2'])}</li><li>{t(UI['how3'])}</li></ol><a class="text-link" href="{path(lang,'/faq')}">{l['faq']} →</a></div></section></main>'''
    write(lang,suffix,content+footer(lang))

def hub(lang,t,meta):
    l=LOCALES[lang];suffix='/guides/'
    content=head(lang,suffix,l['guideTitle'],l['guideLead'],[breadcrumb(lang,suffix,l['guides'])])+header(lang,suffix)
    content+=f'<main id="main" class="wrap"><section class="page-intro"><p class="eyebrow">CSSBuys Store</p><h1>{l["guideTitle"]}</h1><p class="lead">{l["guideLead"]}</p></section><div class="guide-grid all-guides">'+''.join(guide_card(s,lang,meta) for s in ORDER)+'</div></main>'
    write(lang,suffix,content+footer(lang))

def article(lang,slug,t,meta):
    l=LOCALES[lang];m=meta[slug];suffix='/guides/'+slug
    body=BeautifulSoup((BASE/'articles'/lang/f'{slug}.html').read_text(),'html.parser')
    if body.h1:body.h1.decompose()
    for p in list(body.select('.meta,.eyebrow,.toc,.related')):p.decompose()
    for a in body.select('a[href]'):
        href=a['href']
        if href.startswith(DOMAIN):href=href[len(DOMAIN):]
        if href.startswith('/'):
            if href.endswith('.html'):href=href[:-5]
            if href=='/guides':href='/guides/'
            a['href']=prefix(lang)+href
    if lang in OPENINGS.get(slug, {}) and body.p:
        body.p.string = OPENINGS[slug][lang]
    toc=[]
    for i,h in enumerate(body.select('h2')):
        if not h.get('id'):h['id']='section-'+str(i+1)
        toc.append(f'<a href="#{esc(h["id"])}">{esc(h.get_text(" ",strip=True))}</a>')
    # Correct the earlier generic QA blocks and retain a single local related section.
    refs=['cssbuy-spreadsheet','qc-guide','cssbuy-shipping-calculator-estimate','cssbuy-fees-payment-total-cost']
    if 'shoe' in slug:refs=['cssbuy-shoe-finds-price-sizing','cssbuy-shoe-sizing-qc-checklist','qc-guide','cssbuy-fees-payment-total-cost']
    if 'hoodie' in slug:refs=['cssbuy-spreadsheet','cssbuy-size-measurement-qc-photo-limits','qc-guide','cssbuy-fees-payment-total-cost']
    refs=[s for s in refs if s!=slug]
    schema={'@context':'https://schema.org','@type':'Article','headline':m['title'],'description':m['description'],'datePublished':m['published'],'dateModified':DATE,'inLanguage':lang,'mainEntityOfPage':{'@type':'WebPage','@id':url(lang,suffix)},'author':{'@type':'Organization','name':'CSSBuys Store Editorial'},'publisher':{'@type':'Organization','name':'CSSBuys Store'}}
    product_ids=['3400','3394'] if 'shoe' in slug else ['3401','3396'] if 'hoodie' in slug else ['3400','3401','3402'] if slug in ['cssbuy-spreadsheet','cssbuy-fees-payment-total-cost'] else []
    content=head(lang,suffix,m['title'],m['description'],[schema,breadcrumb(lang,suffix,m['title'])])+header(lang,suffix)
    content+=f'<main id="main" class="article-wrap"><article id="article-content"><p class="eyebrow">{l["guides"]} · {l["updated"]} <time datetime="{DATE}">{DATE}</time></p><h1>{esc(m["title"])}</h1><nav class="toc" aria-label="{esc(l["toc"])}">'+''.join(toc)+'</nav>'+str(body)
    if product_ids:content+=f'<section class="article-products"><h2>{l["featured"]}</h2><p>{l["checked"]}</p><div class="article-product-grid">'+''.join(product_card(BY_ID[i],lang,t,False,'article_products') for i in product_ids)+f'</div><p class="hint">{l["productNote"]}</p></section>'
    content+=f'<section class="source-box"><h2>{l["references"]}</h2><p>{t(UI["sourceNote"])}</p><ul><li><a href="https://new.cssbuy.com/buyforme" target="_blank" rel="noopener">CSSBuy: {t(UI["buyingSource"])}</a></li><li><a href="https://new.cssbuy.com/estimates" target="_blank" rel="noopener">CSSBuy: {t(UI["shippingSource"])}</a></li></ul></section></article><section class="related-guides"><h2>{l["related"]}</h2><div class="guide-grid">'+''.join(guide_card(s,lang,meta) for s in refs)+'</div></section></main>'
    write(lang,suffix,content+footer(lang))

def product(lang,p,t,meta):
    l=LOCALES[lang];name=product_name(p,lang,t);suffix='/products/'+p['id'];desc=t(UI['productIntro'])
    schemas=[{'@context':'https://schema.org','@type':'Product','name':name,'image':DOMAIN+'/assets/products/'+p['id']+'.webp','description':desc,'url':url(lang,suffix),'category':t(p['category'])},breadcrumb(lang,suffix,name)]
    content=head(lang,suffix,name+' | '+l['productGuide'],desc,schemas,'/assets/products/'+p['id']+'.webp')+header(lang,suffix)
    content+=f'''<main id="main" class="article-wrap product-detail"><article><p class="eyebrow">{l['productGuide']}</p><h1>{esc(name)}</h1><p class="lead">{desc}</p><div class="product-detail-grid"><img src="/assets/products/{p['id']}.webp" alt="{esc(name)}" width="900" height="900" fetchpriority="high"><div><p>{l['priceLabel']}</p><strong class="price">US${p['price']}</strong><p>{t(p['note'])}</p><a class="button" href="{esc(main_url(p,'product_detail',lang))}" target="_blank" rel="noopener" data-product-id="{p['id']}" data-location="product_detail">{l['open']} ↗</a><p class="hint">{l['checked']}</p></div></div><h2>{l['qc']}</h2><ul class="checklist">{''.join('<li>'+esc(t(s))+'</li>' for s in p['checks'])}</ul><p>{t(UI['record'])}</p><p>{t(UI['decision'])}</p><p>{t(UI['limit'])}</p><p class="hint">{l['productNote']}</p><h2>{l['source']}</h2><p>{t(UI['productSources'])}</p><p><a href="{esc(main_url(p,'product_source',lang))}" target="_blank" rel="noopener" data-product-id="{p['id']}" data-location="product_source">cnfanssp.com · {p['id']} ↗</a></p></article><section class="related-guides"><h2>{l['related']}</h2><p>{t(UI['productRelated'])}</p><div class="guide-grid">{''.join(guide_card(s,lang,meta) for s in ['qc-guide','cssbuy-shoe-sizing-qc-checklist' if p['category']=='Shoes' else 'cssbuy-hoodie-finds-sizing-fabric' if p['category']=='Hoodies & Sweaters' else 'cssbuy-size-measurement-qc-photo-limits','cssbuy-fees-payment-total-cost'])}</div></section></main>'''
    write(lang,suffix,content+footer(lang))

def faq(lang,t):
    l=LOCALES[lang];suffix='/faq';pairs=['price','qc','size','shipping','return','fee','official','search']
    content=head(lang,suffix,l['faqTitle'],t(UI['faqIntro']),[breadcrumb(lang,suffix,l['faq'])])+header(lang,suffix)
    content+=f'<main id="main" class="article-wrap"><h1>{l["faqTitle"]}</h1><p class="lead">{t(UI["faqIntro"])}</p><div class="faq-list">'+''.join(f'<section><h2>{t(UI[k+"Question"])}</h2><p>{t(UI[k+"Answer"])}</p></section>' for k in pairs)+f'</div><a class="button" href="{path(lang,"/guides/")}">{l["allGuides"]}</a></main>'
    write(lang,suffix,content+footer(lang))

def language_hub():
    l=LOCALES['en'];content=head('en','/languages',l['languages']+' | CSSBuys Store',UI['languageIntro'],[],index=False)+header('en','/')
    content+='<main id="main" class="wrap"><section class="page-intro"><h1>Languages</h1><p class="lead">'+UI['languageIntro']+'</p></section><div class="guide-grid">'+''.join(f'<a class="guide-card" href="{path(code)}" lang="{code}" hreflang="{code}"><h2>{loc["name"]}</h2><p>{loc["homeLead"]}</p></a>' for code,loc in LOCALES.items())+'</div></main>'
    write('en','/languages',content+footer('en'),index=False)

def build():
    for lang in LOCALES:
        t=translator(lang);meta=article_meta(lang)
        home(lang,t,meta);hub(lang,t,meta);faq(lang,t)
        for slug in META:article(lang,slug,t,meta)
        for p in PRODUCTS:product(lang,p,t,meta)
        print(lang, '30 pages', flush=True)
    language_hub()
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    ET.register_namespace('xhtml','http://www.w3.org/1999/xhtml')
    ns='{http://www.sitemaps.org/schemas/sitemap/0.9}';x='{http://www.w3.org/1999/xhtml}'
    root=ET.Element(ns+'urlset')
    for address,suffix in SITEMAP:
        entry=ET.SubElement(root,ns+'url');ET.SubElement(entry,ns+'loc').text=address;ET.SubElement(entry,ns+'lastmod').text=DATE
        for code in list(LOCALES)+['x-default']:
            ET.SubElement(entry,x+'link',{'rel':'alternate','hreflang':code,'href':url('en' if code=='x-default' else code,suffix)})
    ET.indent(root,space='  ')
    (OUT/'sitemap.xml').write_bytes(ET.tostring(root,encoding='utf-8',xml_declaration=True))
    print('Sitemap:',len(SITEMAP),'URLs')

if __name__=='__main__':build()
