"""Rebuild localized editorial pages; preserve product data and existing root articles."""
import html, json, re, sys
from pathlib import Path
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
from config import LANGS, TOPICS, UI, path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'hipobuys-de'
DATE = '2026-11-02'
BASE = 'https://hipobuys.de'
CONTENT = {}
for lang in LANGS:
    chunks = (Path(__file__).parent/'content'/f'{lang}.md').read_text().split('@@@ ')[1:]
    CONTENT[lang] = {}
    for chunk in chunks:
        topic, title, description, body = chunk.strip().split('\n', 3)
        CONTENT[lang][topic] = {'title':title,'description':description,'body':body.strip()}
    assert set(CONTENT[lang]) == set(TOPICS), lang

def esc(s): return html.escape(s, quote=True)
def inline(s, lang):
    s = esc(s)
    return re.sub(r'\[\[([\w/-]+)\|([^\]]+)\]\]', lambda m: f'<a href="{m[1] if m[1].startswith("/") else path(lang,m[1])}">{m[2]}</a>', s)

def body_html(body, lang):
    output, headings = [], []
    for block in body.split('\n\n'):
        if block.startswith('## '):
            title = block[3:].strip(); anchor = f'section-{len(headings)+1}'
            headings.append((anchor,title)); output.append(f'<h2 id="{anchor}">{esc(title)}</h2>')
        elif block.startswith('- '):
            output.append('<ul>'+''.join('<li>'+inline(x[2:],lang)+'</li>' for x in block.splitlines())+'</ul>')
        else: output.append('<p>'+inline(block,lang)+'</p>')
    return '\n'.join(output), headings

def langlinks(lang,topic=None):
    return '<nav class="language-links" aria-label="Language">'+''.join(f'<a href="{path(l,topic)}" lang="{l}" hreflang="{l}"'+(' aria-current="page"' if l==lang else '')+f'>{n}</a>' for l,n in LANGS.items())+'</nav>'

def render(lang, topic=None):
    ui=UI[lang]; canonical=BASE+path(lang,topic)
    data=CONTENT[lang].get(topic,{'title':ui[9],'description':ui[10]})
    title,desc=data['title'],data['description']
    alternates=''.join(f'<link rel="alternate" hreflang="{l}" href="{BASE+path(l,topic)}">' for l in LANGS)+f'<link rel="alternate" hreflang="x-default" href="{BASE+path("en",topic)}">'
    structured={'@context':'https://schema.org','@graph':[{'@type':'Article' if topic else 'CollectionPage','headline':title,'name':title,'description':desc,'url':canonical,'mainEntityOfPage':canonical,'inLanguage':lang,'dateModified':DATE,'author':{'@type':'Organization','name':'HipoBuys.de','url':BASE+'/imprint'},'publisher':{'@type':'Organization','name':'HipoBuys.de','url':BASE+'/'}}]}
    if topic:
        structured['@graph'].append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':ui[0],'item':BASE+path(lang)},{'@type':'ListItem','position':2,'name':title,'item':canonical}]})
    links=''.join(f'<a href="{path(lang,t)}">{esc(CONTENT[lang][t]["title"])}</a>' for t in ['fees','shipping'])
    out=f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}">{alternates}
<link rel="icon" href="/assets/svg/favicon.svg"><link rel="stylesheet" href="/assets/css/buyer-guide.css?v={DATE}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:type" content="{'article' if topic else 'website'}"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-Y2VLGD300R"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-Y2VLGD300R');</script>
<script type="application/ld+json">{json.dumps(structured,ensure_ascii=False)}</script></head><body>
<header class="top"><div class="top-inner"><a class="brand" href="{path(lang)}">HipoBuys.de</a><nav class="nav"><a href="{path(lang)}">{ui[0]}</a><a href="{path(lang,'w2c')}">W2C</a><a href="{path(lang,'qc')}">QC</a><a href="https://www.cnfanshp.com/AllProducts/?utm_source=hipobuys.de&amp;utm_medium=referral&amp;utm_campaign=guide_nav" target="_blank" rel="noopener">{ui[6]}</a></nav></div></header>
<main><section class="hero"><div class="hero-inner"><span class="eyebrow">HipoBuys.de · {LANGS[lang]}</span><h1>{esc(title)}</h1><p>{esc(desc)}</p><div class="meta">HipoBuys.de · {ui[3]} <time datetime="{DATE}">{DATE}</time></div>{langlinks(lang,topic)}</div></section><article class="article">'''
    if topic:
        body,headings=body_html(data['body'],lang)
        out+='<nav class="toc"><strong>'+ui[1]+'</strong><ol>'+''.join(f'<li><a href="#{a}">{esc(h)}</a></li>' for a,h in headings)+'</ol></nav>'+body
        labels=ui[5].split('|')
        sources=['https://hipobuy.com/','https://hipobuy.com/notice/1740653781924810754']
        if topic in ('safety','links'): sources.append('https://hipobuy.com/goods/details?channel=WEIDIAN&id=7797612745')
        out+='<aside class="note"><h2>'+ui[4]+'</h2><ul>'+''.join(f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{labels[i]}</a></li>' for i,u in enumerate(sources))+'</ul></aside>'
    out+='<section class="related"><h2>'+ui[2]+'</h2><div class="guide-cards">'+''.join(f'<a class="guide-card" href="{path(lang,t)}"><strong>{esc(CONTENT[lang][t]["title"])}</strong><span>{esc(CONTENT[lang][t]["description"])}</span></a>' for t in TOPICS if t!=topic)+'</div></section>'
    if lang=='de' and not topic:
        extras=[]
        for p in sorted((SITE/'de').glob('*/index.html')):
            url='/'+str(p.relative_to(SITE).parent)+'/'
            if url in [path(lang,t) for t in TOPICS]: continue
            soup=BeautifulSoup(p.read_text(),'html.parser'); h=soup.find('h1')
            if h: extras.append(f'<li><a href="{url}">{esc(h.get_text(" ",strip=True))}</a></li>')
        out+='<section class="related"><h2>Weitere Anleitungen für Deutschland</h2><ul>'+''.join(extras)+'</ul></section>'
    legal=''.join(f'<a href="/{p}">{label}</a>' for p,label in zip(['imprint','privacy','disclaimer'],ui[8].split('|')))
    out+=f'</article></main><footer class="footer"><div class="footer-inner"><strong>HipoBuys.de</strong><p>{ui[7]}</p>{legal}</div></footer><script defer src="/assets/js/main.js?v={DATE}"></script></body></html>\n'
    return out

changed_urls=set()
for lang in LANGS:
    for topic in [None]+TOPICS:
        url=path(lang,topic); target=SITE/url.strip('/')/'index.html';target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(render(lang,topic));changed_urls.add(BASE+url)

# Provide crawlable entry points on root pages without replacing their product content.
for name in ['index.html','guides.html','languages.html']:
    p=SITE/name;soup=BeautifulSoup(p.read_text(),'html.parser')
    for old in soup.select('#localized-guides-update'):old.decompose()
    section=soup.new_tag('section',id='localized-guides-update',attrs={'class':'section'})
    section.append(BeautifulSoup('<h2>Buyer guides in your language</h2><p>Shipping costs, delivery, product links and buying checks.</p><div class="localized-grid">'+''.join(f'<div class="localized-card" lang="{lang}"><h3><a href="/{lang}/">{name}</a></h3><p>{esc(UI[lang][10])}</p><ul>'+''.join(f'<li><a href="{path(lang,t)}">{esc(CONTENT[lang][t]["title"])}</a></li>' for t in ['safety','links'])+'</ul></div>' for lang,name in LANGS.items())+'</div>','html.parser'))
    soup.find('main').append(section)
    if not soup.select_one('#localized-guide-styles'):
        style=soup.new_tag('style',id='localized-guide-styles')
        style.string='#localized-guides-update{max-width:1120px;margin:auto;padding:36px 18px}.localized-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.localized-card{background:#fffdf8;border:1px solid #e2d8ca;border-radius:18px;padding:20px}.localized-card h3{margin:0 0 10px}.localized-card a{color:#0f766e}.localized-card p,.localized-card li{font-size:15px;line-height:1.6}.localized-card li{margin:10px 0}@media(max-width:700px){.localized-grid{grid-template-columns:1fr}}'
        soup.head.append(style)
    # Replace remaining layout instructions in customer-facing root copy.
    replacements={
        'Send the visitor to the matching product or category route on the linked product index.':'Open the current product listing and confirm the selected variant.',
        'Compact catalog cards with uniform image size, clean labels and direct outbound product paths.':'Browse the selected items, then check current variants, availability and prices on the product page.',
        'Buyer questions answered before they click':'Questions to check before ordering',
        'These questions explain the site’s role, QC flow, category routing and Germany/EU shipping preparation.':'Understand product links, warehouse checks and shipping preparation before placing an order.'}
    for node in soup.find_all(string=True):
        if node.parent.name not in ['script','style'] and node.strip() in replacements:node.replace_with(replacements[node.strip()])
    p.write_text(str(soup));changed_urls.add(BASE+('/' if name=='index.html' else '/'+name[:-5]))

# Remove domain names from visible prose only, preserving all product destination URLs.
for p in SITE.rglob('*.html'):
    soup=BeautifulSoup(p.read_text(),'html.parser');changed=False
    lang=soup.html.get('lang','en') if soup.html else 'en'
    replacement={'de':'dem separaten Produktindex','fr':'le catalogue de produits','es':'el catálogo de productos','it':'il catalogo prodotti','pl':'katalog produktów','pt':'o catálogo de produtos','nl':'de productindex'}.get(lang,'the product index')
    for node in soup.find_all(string=re.compile(r'cnfans(?:hp|sp)\.com',re.I)):
        if node.parent.name in ['script','style']:continue
        node.replace_with(re.sub(r'(?:https?://)?(?:www\.)?cnfans(?:hp|sp)\.com',replacement,str(node),flags=re.I));changed=True
    if changed:
        p.write_text(str(soup));canonical=soup.find('link',rel='canonical')
        if canonical:changed_urls.add(canonical['href'])

ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
tree=ET.parse(SITE/'sitemap.xml');root=tree.getroot();existing={e.find(f'{{{ns}}}loc').text:e for e in root}
for url in sorted(changed_urls):
    entry=existing.get(url)
    if entry is None:
        entry=ET.SubElement(root,f'{{{ns}}}url');ET.SubElement(entry,f'{{{ns}}}loc').text=url
    mod=entry.find(f'{{{ns}}}lastmod')
    if mod is None:mod=ET.SubElement(entry,f'{{{ns}}}lastmod')
    mod.text=DATE
ET.indent(tree,space='  ');tree.write(SITE/'sitemap.xml',encoding='utf-8',xml_declaration=True)
print(f'Built {len(LANGS)*8} localized pages; sitemap contains {len(root)} URLs.')
