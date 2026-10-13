#!/usr/bin/env python3
"""Build the nine-language editorial set without runtime translation dependencies.

Run from any directory. Only writes hoobuys-shop pages and its generated assets.
Unchanged specialist articles keep their original URLs and translation widget.
"""
import csv
import html
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
SITE = HERE.parents[1] / 'hoobuys-shop'
DATA = HERE / 'content'
DATE = '2026-10-13'
VERSION = '20261013-seo-v1'
HOST = 'https://hoobuys.shop'
LANGS = {'en':'English', 'zh-CN':'简体中文', 'de':'Deutsch', 'fr':'Français', 'es':'Español', 'it':'Italiano', 'pl':'Polski', 'nl':'Nederlands', 'pt':'Português'}
SLUGS = {
    'qc':'hoobuy-qc-photos-find-check-guide',
    'pending':'hoobuy-process-pending-order-checklist',
    'cost':'hoobuy-shipping-cost-volumetric-weight',
    'extra':'hoobuy-extra-qc-photos-when-new-angle-is-worth-requesting-2026',
    'sheet':'hoobuy-spreadsheet-guide',
    'shipping':'shipping-guide',
    'alignment':'hoobuy-alignment-symmetry-print-placement-qc-2026',
}
PUBLISHED = {'alignment':'2026-08-14', 'extra':'2026-09-12'}
UI = json.loads((DATA / 'ui.json').read_text())
ARTICLES = {lang:json.loads((DATA / f'{lang}.json').read_text()) for lang in LANGS}
PRODUCT_IDS = ['5974','6037','5976','5983','5975','6045','5970','5919','5822','5931']
PRODUCT_IMAGES = ['20260417/1-26041G1101D39','20260417/1-26041G12323411','20260417/1-26041G1121Q55','20260417/1-26041G1212V39','20260417/1-26041G11119217','20260417/1-26041G1193O56','20260417/1-26041G04523609','20260328/1-26032Q40Z2R6','20260402/1-260402111049305','20260326/1-260326112201519']
CATEGORIES = ['shoes','hoodies-sweaters','t-shirts','jackets','pants-shorts','accessories','electronics','AllProducts']
GENERATED = {}
E = html.escape

def path(lang, slug=''):
    prefix = '' if lang == 'en' else '/' + lang.lower()
    return prefix + '/' + slug if slug else prefix + '/'

def url(lang, slug=''):
    return HOST + path(lang, slug)

def alternate_links(slug):
    return ''.join(f'<link rel="alternate" hreflang="{lang}" href="{url(lang,slug)}">' for lang in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{url("en",slug)}">'

def language_menu(lang, slug):
    links = ''.join(f'<a href="{path(code,slug)}" lang="{code}" hreflang="{code}"{(" aria-current=\"page\"" if code == lang else "")}>{name}</a>' for code,name in LANGS.items())
    return f'<details class="language-menu"><summary aria-label="{E(UI[lang]["language"],quote=True)}">{LANGS[lang]} ▾</summary><div>{links}</div></details>'

def header(lang, slug):
    u = UI[lang]
    routes = ['', 'guides', 'products', SLUGS['sheet'], SLUGS['shipping'], 'faq']
    nav = ''.join(f'<a href="{path(lang,p)}"{(" aria-current=\"page\"" if p == slug else "")}>{E(label)}</a>' for p,label in zip(routes,u['nav']))
    return f'''<header class="top site-header"><div class="wrap bar"><a class="site-brand" href="{path(lang)}" aria-label="{E(u['nav'][0])}"><img class="site-logo" src="/assets/hoobuy-logo-20261012.png" width="225" height="60" alt="Hoobuy" decoding="async"></a>{language_menu(lang,slug)}<button class="menu" id="menuBtn" type="button" aria-controls="nav" aria-expanded="false" aria-label="{E(u['menu'])}">☰</button><nav class="nav" id="nav" aria-label="{E(u['menu'])}">{nav}<a class="hot" href="https://cnfanssp.com/AllProducts/">{E(u['open'])}</a></nav></div></header>'''

def shell(lang, slug, title, description, content, schema=None, article=False):
    u = UI[lang]
    kind = 'article' if article else 'website'
    objects = [schema] if schema else []
    if slug:
        objects.append({'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[
            {'@type':'ListItem','position':1,'name':u['nav'][0],'item':url(lang)},
            {'@type':'ListItem','position':2,'name':title,'item':url(lang,slug)}]})
    structured = ''.join('<script type="application/ld+json">'+json.dumps(obj,ensure_ascii=False).replace('<','\\u003c')+'</script>' for obj in objects)
    return f'''<!doctype html>
<html lang="{lang}" data-static-locale="true"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(description,quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{url(lang,slug)}">{alternate_links(slug)}<meta property="og:type" content="{kind}"><meta property="og:site_name" content="hoobuys.shop"><meta property="og:title" content="{E(title,quote=True)}"><meta property="og:description" content="{E(description,quote=True)}"><meta property="og:url" content="{url(lang,slug)}"><meta name="twitter:card" content="summary"><link rel="stylesheet" href="/assets/styles.css"><link rel="stylesheet" href="/assets/compact.css?v={VERSION}"><link rel="stylesheet" href="/assets/seo.css?v={VERSION}"><script defer src="/assets/compact.js?v={VERSION}"></script><script defer src="/assets/seo.js?v={VERSION}"></script><script async src="https://www.googletagmanager.com/gtag/js?id=G-X7V92TETF6"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-X7V92TETF6');</script>{structured}<noscript><style>.site-header .bar{{flex-wrap:wrap}}.site-compact .site-header .nav{{display:flex;flex-wrap:wrap;position:static;max-height:none}}.site-compact .site-header .menu{{display:none}}</style></noscript></head><body class="site-compact seo-page">{header(lang,slug)}{content}<footer class="foot">hoobuys.shop · {E(u['footer'])}<div class="footer-links"><a href="{path(lang,'languages')}">{E(u['language'])}</a><a href="/privacy">{E(u['legal'][0])}</a><a href="/terms">{E(u['legal'][1])}</a></div></footer></body></html>
'''

def write(lang, slug, document):
    dest = SITE / ('' if lang == 'en' else lang.lower()) / ((slug or 'index')+'.html')
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(document,encoding='utf-8')
    GENERATED[path(lang,slug)] = {'lang':lang,'slug':slug}

def card(lang,key):
    a = ARTICLES[lang][key]
    return f'<a class="card" href="{path(lang,SLUGS[key])}"><h3>{E(a["title"])}</h3><p>{E(a["description"])}</p></a>'

def search(lang):
    u = UI[lang]['search']
    return f'<form class="product-search" action="https://cnfanssp.com/search.html" method="get" data-product-search><label for="product-query">{E(u[0])}</label><div><input id="product-query" type="search" name="keywords" required maxlength="150" placeholder="{E(u[1])}"><input type="hidden" name="channelid" value="2"><button type="submit">{E(u[2])}</button></div></form>'

def categories(lang):
    links = ''.join(f'<a class="category-link" href="https://cnfanssp.com/{category}/">{E(name)}</a>' for category,name in zip(CATEGORIES,UI[lang]['categoryNames']))
    return f'<section><h2>{E(UI[lang]["categories"])}</h2><div class="category-grid">{links}</div></section>'

def products(lang):
    u = UI[lang]
    cards = ''.join(f'<article class="product card"><a class="pic" href="https://cnfanssp.com/AllProducts/{pid}.html"><img src="https://cnfanshp.com/uploads/allimg/{img}.webp" alt="{E(name)}" width="240" height="180" loading="lazy" decoding="async" referrerpolicy="no-referrer"></a><h3>{E(name)}</h3><p>ID {pid}</p><a class="product-route" href="https://cnfanssp.com/AllProducts/{pid}.html">{E(u["route"])} →</a></article>' for pid,img,name in zip(PRODUCT_IDS,PRODUCT_IMAGES,u['productNames']))
    return f'<section><h2>{E(u["finds"])}</h2><div class="grid5">{cards}</div></section>'

def faq(lang):
    u = UI[lang]
    items = ''.join(f'<details class="compact-faq"><summary><h3>{E(q)}</h3></summary><p>{E(a)}</p></details>' for q,a in zip(u['faqQuestions'],u['faqAnswers']))
    return f'<section class="faq-list"><h2>{E(u["faqTitle"])}</h2>{items}</section>'

def calculator(lang):
    u = UI[lang]
    fields = ''.join(f'<label>{E(label)}<input name="{name}" type="number" inputmode="decimal" step="any" min="0.000001" required></label>' for name,label in zip(['weight','length','width','height','divisor'],u['calcLabels']))
    return f'<section class="interactive-tool" id="weight-calculator"><h2>{E(u["calculator"])}</h2><form data-weight-calculator data-error="{E(u["invalid"])}" data-volume="{E(u["results"][0])}" data-billed="{E(u["results"][1])}"><div class="calculator-fields">{fields}</div><button type="submit">{E(u["calculate"])}</button><output aria-live="polite"></output></form><p class="tool-note">{E(u["calcNote"])}</p></section>'

def tracker(lang):
    u = UI[lang]
    return f'<aside class="download-panel"><a class="btn" data-tracker-download href="/assets/hoobuy-tracker-{lang.lower()}.csv" download>{E(u["download"])}</a><p>{E(u["downloadNote"])}</p></aside>'

def diagram(lang):
    return f'<figure class="qc-diagram"><img src="/assets/qc-alignment.svg" width="620" height="240" alt="{E(UI[lang]["diagram"])}" loading="lazy"><figcaption>{E(UI[lang]["diagram"])}</figcaption></figure>'

def build_articles(lang):
    u = UI[lang]
    for key,a in ARTICLES[lang].items():
        slug = SLUGS[key]
        toc = ''.join(f'<a href="#step-{i}">{E(s[0])}</a>' for i,s in enumerate(a['sections'],1))
        sections = ''.join(f'<details class="reading-section" open><summary><h2 id="step-{i}">{E(s[0])}</h2></summary><div class="reading-content">'+''.join(f'<p>{E(p)}</p>' for p in s[1:])+'</div></details>' for i,s in enumerate(a['sections'],1))
        tools = tracker(lang) if key == 'sheet' else calculator(lang) if key == 'cost' else diagram(lang) if key == 'alignment' else ''
        related_keys = {'qc':['extra','alignment','sheet'],'pending':['sheet','qc','shipping'],'cost':['shipping','sheet','qc'],'extra':['alignment','qc','shipping'],'sheet':['pending','qc','cost'],'shipping':['qc','extra','cost'],'alignment':['extra','qc','shipping']}[key]
        body = f'<main class="wrap article"><nav class="crumb" aria-label="{E(u["nav"][1])}"><a href="{path(lang)}">{E(u["nav"][0])}</a> / <a href="{path(lang,"guides")}">{E(u["nav"][1])}</a></nav><article><header class="article-head"><p class="meta">{E(u["updated"])} <time datetime="{DATE}">{DATE}</time> · Hoobuys Shop</p><h1>{E(a["title"])}</h1><p class="lede">{E(a["lead"])}</p></header>{tools}<div class="reading-tools"><details class="reading-toc"><summary>{E(u["toc"])}</summary><nav>{toc}</nav></details><button type="button" class="reading-toggle" data-expand="{E(u["expand"])}" data-collapse="{E(u["collapse"])}">{E(u["expand"])}</button></div>{sections}<p class="source">{E(u["sourceNote"])}</p></article><section><h2>{E(u["related"])}</h2><div class="grid3">'+''.join(card(lang,r) for r in related_keys)+f'</div></section><aside class="note">{E(u["notice"])}</aside></main>'
        schema = {'@context':'https://schema.org','@type':'Article','headline':a['title'],'description':a['description'],'mainEntityOfPage':url(lang,slug),'url':url(lang,slug),'inLanguage':lang,'dateModified':DATE,'datePublished':PUBLISHED.get(key,DATE) if lang == 'en' else DATE,'author':{'@type':'Organization','name':'Hoobuys Shop','url':HOST+'/'},'publisher':{'@type':'Organization','name':'Hoobuys Shop','logo':{'@type':'ImageObject','url':HOST+'/assets/hoobuy-logo-20261012.png'}}}
        if lang == 'en' and key in {'sheet','shipping'}: schema.pop('datePublished')
        write(lang,slug,shell(lang,slug,a['title'],a['description'],body,schema,True))

def get_archive():
    result = []
    for f in sorted(SITE.glob('hoobuy-*.html')):
        if f.stem in SLUGS.values(): continue
        source = f.read_text()
        title = html.unescape(re.search(r'<title>(.*?)</title>',source,re.S).group(1))
        lang = re.search(r'<html[^>]+lang=["\']([^"\']+)',source).group(1)
        result.append({'slug':f.stem,'title':title,'lang':lang})
    return result

def build_hubs(lang,archive):
    u = UI[lang]
    home = f'<main class="wrap"><section class="hero"><p class="eyebrow">HOOBUYS SHOP · QC / W2C / SHIPPING</p><h1>{E(u["homeTitle"])}</h1><p>{E(u["homeLead"])}</p>{search(lang)}</section><section><h2>{E(u["latest"])}</h2><div class="grid2">'+''.join(card(lang,k) for k in ['qc','pending','cost','extra'])+f'</div><a class="text-link" href="{path(lang,"guides")}">{E(u["all"])} →</a></section>'+categories(lang)+products(lang)+faq(lang)+f'<aside class="note">{E(u["notice"])}</aside></main>'
    write(lang,'',shell(lang,'',u['homeTitle'],u['homeLead'],home,{'@context':'https://schema.org','@type':'WebSite','name':'Hoobuys Shop','url':url(lang),'inLanguage':lang}))
    archive_links = ''.join(f'<li><a href="/{a["slug"]}" lang="{a["lang"]}">{E(a["title"])}</a><span class="archive-lang">{E(a["lang"])}</span></li>' for a in archive)
    guides = f'<main class="wrap"><section class="hero"><h1>{E(u["guidesTitle"])}</h1><p>{E(u["homeLead"])}</p></section><section><div class="guide-list">'+''.join(card(lang,k) for k in SLUGS)+f'</div></section><section><details class="archive"><summary>{E(u["archive"])} ({len(archive)})</summary><p>{E(u["archiveNote"])}</p><ul>{archive_links}</ul></details></section><aside class="note">{E(u["notice"])}</aside></main>'
    items = [{'@type':'ListItem','position':i,'name':ARTICLES[lang][key]['title'],'url':url(lang,SLUGS[key])} for i,key in enumerate(SLUGS,1)]
    items += [{'@type':'ListItem','position':len(items)+i,'name':a['title'],'url':HOST+'/'+a['slug']} for i,a in enumerate(archive,1)]
    schema = {'@context':'https://schema.org','@type':'CollectionPage','name':u['guidesTitle'],'url':url(lang,'guides'),'inLanguage':lang,'mainEntity':{'@type':'ItemList','numberOfItems':len(items),'itemListElement':items}}
    write(lang,'guides',shell(lang,'guides',u['guidesTitle'],u['homeLead'],guides,schema))
    product_body = f'<main class="wrap"><section class="hero"><h1>{E(u["productsTitle"])}</h1><p>{E(u["notice"])}</p>{search(lang)}</section>'+categories(lang)+products(lang)+'</main>'
    write(lang,'products',shell(lang,'products',u['productsTitle'],u['notice'],product_body))
    write(lang,'faq',shell(lang,'faq',u['faqTitle']+' | Hoobuys Shop',u['homeLead'],f'<main class="wrap"><section class="hero"><h1>{E(u["faqTitle"])}</h1></section>'+faq(lang)+f'<a class="text-link" href="{path(lang,"guides")}">{E(u["all"])}</a></main>'))
    links = ''.join(f'<a class="card" lang="{code}" href="{path(code)}">{name}</a>' for code,name in LANGS.items())
    write(lang,'languages',shell(lang,'languages',u['languagesTitle'],u['homeLead'],f'<main class="wrap"><section class="hero"><h1>{E(u["languagesTitle"])}</h1></section><div class="grid3">{links}</div></main>'))

def build_sitemaps():
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    xhtml = 'http://www.w3.org/1999/xhtml'
    ET.register_namespace('',ns)
    ET.register_namespace('xhtml',xhtml)
    previous = {}
    old = SITE/'sitemap.xml'
    if old.exists():
        for element in ET.parse(old).getroot():
            loc,modified = element.find(f'{{{ns}}}loc'),element.find(f'{{{ns}}}lastmod')
            if loc is not None and modified is not None: previous[loc.text]=modified.text
    root = ET.Element(f'{{{ns}}}urlset')
    urls = []
    for f in sorted(SITE.rglob('*.html')):
        if f.name == '404.html': continue
        rel = f.relative_to(SITE).as_posix()
        route = '/'+rel[:-5]
        if route.endswith('/index'): route = route[:-5]
        address = HOST+route
        urls.append(address)
        entry = ET.SubElement(root,f'{{{ns}}}url')
        ET.SubElement(entry,f'{{{ns}}}loc').text = address
        modified = DATE if route in GENERATED else previous.get(address)
        if modified: ET.SubElement(entry,f'{{{ns}}}lastmod').text = modified
        if route in GENERATED:
            slug = GENERATED[route]['slug']
            for lang in LANGS:
                ET.SubElement(entry,f'{{{xhtml}}}link',{'rel':'alternate','hreflang':lang,'href':url(lang,slug)})
            ET.SubElement(entry,f'{{{xhtml}}}link',{'rel':'alternate','hreflang':'x-default','href':url('en',slug)})
    ET.indent(root,space='  ')
    ET.ElementTree(root).write(old,encoding='utf-8',xml_declaration=True)
    (SITE/'sitemap.txt').write_text('\n'.join(urls)+'\n')
    (SITE/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: https://hoobuys.shop/sitemap.xml\nSitemap: https://hoobuys.shop/sitemap.txt\n')
    return len(urls)

def main():
    assert set(UI) == set(LANGS)
    archive = get_archive()
    for lang in LANGS:
        assert set(ARTICLES[lang]) == set(SLUGS),lang
        assert len(UI[lang]['csv']) == 22
        for article in ARTICLES[lang].values():
            assert len(article['sections']) == 5
            assert all(len(section) == 3 for section in article['sections'])
        build_articles(lang)
        build_hubs(lang,archive)
        with (SITE/'assets'/f'hoobuy-tracker-{lang.lower()}.csv').open('w',encoding='utf-8-sig',newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(UI[lang]['csv'])
            writer.writerow(['']*22)
    count = build_sitemaps()
    print(json.dumps({'languages':len(LANGS),'core_articles':len(SLUGS),'article_pages':len(LANGS)*len(SLUGS),'generated_pages':len(GENERATED),'legacy_specialist_articles':len(archive),'sitemap_urls':count}))

if __name__ == '__main__': main()
