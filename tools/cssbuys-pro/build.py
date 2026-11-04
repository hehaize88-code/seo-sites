#!/usr/bin/env python3
"""Update the existing static CSSBuys.pro site. No other site is written."""
import json
import re
from copy import deepcopy
from html import escape as esc
from pathlib import Path
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from ui import UI, LANGS, NAMES, DATE, DOMAIN, HOME_CONTROLS

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1] / 'cssbuys-pro'
NEW = ['cssbuy-returns-refunds', 'cssbuy-shipping-deposit-final-cost', 'cssbuy-warehouse-storage-deadlines']
PRIORITY = NEW + ['qc-guide', 'cssbuy-pro-calculator-route-fees-guide', 'cssbuy-pro-qc-lab-photo-video-extra-fee', 'w2c', 'cssbuy-pro-coupon-exchange-rate-reward-guide']
def read(path): return BeautifulSoup(path.read_text(), 'html.parser')
def fragment(html): return BeautifulSoup(html, 'html.parser')
def append_html(node, html):
    for child in list(fragment(html).contents): node.append(child)
def prefix(lang): return '' if lang == 'en' else '/' + lang
def route(lang, path): return prefix(lang) + path
def file_for(lang, name): return ROOT / ('' if lang == 'en' else lang) / name
def set_meta(s, name, value, prop=False):
    key = 'property' if prop else 'name'
    t = s.find('meta', attrs={key:name})
    if not t:
        t=s.new_tag('meta',attrs={key:name});s.head.append(t)
    t['content']=value
def jsonld(s, data):
    t=s.new_tag('script',type='application/ld+json');t.string=json.dumps(data,ensure_ascii=False);s.head.append(t)
def metadata(s, lang, path, title, desc, typ='WebPage'):
    s.html['lang']=lang
    if not s.title:s.head.append(s.new_tag('title'))
    s.title.string=title
    set_meta(s,'description',desc)
    for key,val in [('og:title',title),('og:description',desc),('og:url',DOMAIN+path),('og:type','article' if typ=='Article' else 'website')]: set_meta(s,key,val,True)
    for el in s.select('link[rel="canonical"],link[rel="alternate"][hreflang],script[type="application/ld+json"]'):el.decompose()
    s.head.append(s.new_tag('link',rel='canonical',href=DOMAIN+path))
    base=path[len(prefix(lang)):] if prefix(lang) else path
    for other in LANGS:
        s.head.append(s.new_tag('link',rel='alternate',hreflang=other,href=DOMAIN+route(other,base)))
    s.head.append(s.new_tag('link',rel='alternate',hreflang='x-default',href=DOMAIN+base))
    data={'@context':'https://schema.org','@type':typ,'name':title,'description':desc,'url':DOMAIN+path,'inLanguage':lang}
    if typ=='Article':
        data.update(headline=title,mainEntityOfPage=DOMAIN+path,dateModified=DATE,author={'@type':'Organization','name':'CSSBuys Pro Editorial'},publisher={'@type':'Organization','name':'CSSBuys Pro'})
    if typ=='Article' and base.rsplit('/',1)[-1] in NEW: data['datePublished']=DATE
    jsonld(s,data)
    if typ=='Article':
        jsonld(s,{'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':UI[lang]['nav'][0],'item':DOMAIN+route(lang,'/')},{'@type':'ListItem','position':2,'name':UI[lang]['nav'][5],'item':DOMAIN+route(lang,'/guides/')},{'@type':'ListItem','position':3,'name':title,'item':DOMAIN+path}]})

def common(s,lang,path):
    u=UI[lang];base=path[len(prefix(lang)):] if prefix(lang) else path
    links=list(zip(u['nav'],[route(lang,'/'),route(lang,'/guides/cssbuy-spreadsheet'),route(lang,'/guides/qc-guide'),route(lang,'/guides/cssbuy-pro-calculator-route-fees-guide'),route(lang,'/faq'),route(lang,'/guides/'),'https://cnfanshp.com/AllProducts/']))
    anchors=''.join(f'<a href="{href}"'+(' class="btn"' if i==6 else '')+f'>{esc(label)}</a>' for i,(label,href) in enumerate(links))
    logo=f'<a class="brand" href="{route(lang,"/")}" aria-label="CSSBuys Pro"><img class="site-logo" src="/assets/cssbuy-logo-20261007.png" alt="CSSBuy" width="145" height="39"></a>'
    for x in list(s.body.find_all(['header','aside','footer'],recursive=False)): x.decompose()
    for x in s.select('.overlay,.locale-bar,.site-breadcrumbs'):
        if x.parent and x.parent.name=='div' and x.parent.get('class')==['wrap'] and len(x.parent.find_all(recursive=False))==1:x.parent.decompose()
        else:x.decompose()
    header=f'<header class="nav"><div class="wrap nav-inner">{logo}<nav class="nav-links" aria-label="{esc(u["nav"][0])}">{anchors}</nav><a class="menu-btn" href="#drawer" aria-label="{esc(u["nav"][5])}">☰</a></div></header><aside class="drawer" id="drawer"><div class="drawer-head">{logo}<a class="close" href="#" aria-label="×">×</a></div><nav class="drawer-links">{anchors}</nav></aside><a class="overlay" href="#" tabindex="-1" aria-label="×"></a>'
    locales=''.join(f'<a href="{route(x,base)}" lang="{x}" hreflang="{x}"'+(' aria-current="page"' if x==lang else '')+f'>{name}</a>' for x,name in zip(LANGS,NAMES))
    for child in reversed(list(fragment(header+f'<div class="wrap"><nav class="locale-bar" aria-label="Language">{locales}</nav></div>').contents)):s.body.insert(0,child)
    append_html(s.body,f'<footer class="footer"><div class="wrap foot-grid"><div>{logo}<p>{esc(u["footer"])}</p></div><div><b>{esc(u["nav"][5])}</b>'+''.join(f'<a href="{href}">{esc(label)}</a>' for label,href in links[1:4])+f'</div><div><b>{esc(u["related"])}</b>'+''.join(f'<a href="{href}">{esc(label)}</a>' for label,href in links[4:])+ '</div></div></footer>')
    for href in ['/assets/seo-content.css?v=20261007','/assets/site-update.css?v=20261104']:
        if not s.find('link',href=href):s.head.append(s.new_tag('link',rel='stylesheet',href=href))
    for x in s.select('script[src*="planning-tools"],script[src*="site-events"]'):x.decompose()
    s.head.append(s.new_tag('script',src='/assets/site-events.js?v=20261104',defer=''))
    s.head.append(s.new_tag('script',src='/assets/planning-tools.mjs?v=20261104',type='module'))

def weight_tool(lang):
    u=UI[lang];fields=''
    for name,label,val in zip(['actual','length','width','height','divisor','increment'],u['weight_labels'],['3','40','30','25','6000','0.5']):
        fields+=f'<label for="weight-{name}">{esc(label)}<input id="weight-{name}" name="{name}" type="number" step="any" min="0.0001" max="1000000" value="{val}" required></label>'
    fields+=f'<label for="weight-rule">{esc(u["weight_labels"][6])}<select id="weight-rule" name="rule"><option value="max">{esc(u["rules"][0])}</option><option value="actual">{esc(u["rules"][1])}</option></select></label>'
    outputs=''.join(f'<div><dt>{esc(label)}</dt><dd data-weight-result="{name}">—</dd></div>' for name,label in zip(['volume','basis','billed'],u['weight_results']))
    return f'<section class="planning-tool" data-update-block="weight" id="weight-calculator"><h2>{esc(u["weight_title"])}</h2><p>{esc(u["weight_note"])}</p><form data-weight-form data-error="{esc(u["invalid"])}"><div class="tool-fields">{fields}</div><button class="btn" type="submit">{esc(u["calculate"])}</button><p class="tool-error" role="alert"></p><dl class="tool-results" aria-live="polite">{outputs}</dl></form><p class="tool-privacy">{esc(u["privacy"])}</p><p><a href="https://www.cssbuy.com/estimates">{esc(u["official"])}</a></p></section>'

def budget_tool(lang):
    u=UI[lang]
    fields=''.join(f'<label for="budget-{i}">{esc(label)}<input id="budget-{i}" name="cost{i}" type="number" min="0" max="1000000000" step="0.01" value="0" required></label>' for i,label in enumerate(u['budget_labels']))
    return f'<section class="planning-tool" data-update-block="budget" id="cost-worksheet"><h2>{esc(u["budget_title"])}</h2><p>{esc(u["budget_note"])}</p><form data-budget-form data-error="{esc(u["invalid"])}" data-credit-error="{esc(u["budget_warning"])}"><div class="tool-fields">{fields}</div><button class="btn" type="submit">{esc(u["calculate"])}</button><p class="tool-error" role="alert"></p><dl class="tool-results" aria-live="polite"><div><dt>{esc(u["budget_result"])}</dt><dd data-budget-result>—</dd></div></dl></form><p class="tool-privacy">{esc(u["privacy"])}</p></section>'

def toc(s,article,lang):
    for x in article.select('.toc'):x.decompose()
    headings=[]
    for i,h in enumerate(article.find_all('h2'),1):
        if h.find_parent(class_=['related-links','source-links']):continue
        if not h.get('id'): h['id']='guide-section-'+str(i)
        headings.append(h)
    nav=fragment(f'<nav class="toc" aria-label="{esc(UI[lang]["toc"])}"><strong>{esc(UI[lang]["toc"])}</strong>'+''.join(f'<a href="#{h["id"]}">{esc(h.get_text(" ",strip=True))}</a>' for h in headings)+'</nav>').nav
    intro=next((p for p in article.find_all('p',recursive=False) if 'byline' not in p.get('class',[])),None)
    (intro or article.select_one('.byline') or article.h1).insert_after(nav)

def faqs_html(rows): return '<div class="faq-grid">'+''.join(f'<details class="faq-card"><summary>{esc(q["q"])}</summary><p>{q["a"]}</p></details>' for q in rows)+'</div>'
def faq_schema(s,rows):jsonld(s,{'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q['q'],'acceptedAnswer':{'@type':'Answer','text':fragment(q['a']).get_text(' ',strip=True)}}for q in rows]})

def run():
    catalog=json.loads((HERE/'editorial/catalog.json').read_text())
    faq=json.loads((HERE/'editorial/faq.json').read_text())
    bodies={}
    for p in (HERE/'content').glob('*.json'):
        data=json.loads(p.read_text());assert set(data['locales'])==set(LANGS),f'Incomplete translations: {p}'
        bodies[data['slug']]=data['locales'];catalog[data['slug']]=data['locales']
    assert all(x in bodies for x in NEW)
    assert len(catalog)==25,len(catalog)
    assert all(len(faq[l])>=24 for l in LANGS)
    cleanup=HERE/'editorial/body-cleanup.json'
    if cleanup.exists():
        for x in json.loads(cleanup.read_text()):
            p=ROOT/x['path'];text=p.read_text()
            if x['old'] in text:text=text.replace(x['old'],x['new'],1);p.write_text(text)
            elif fragment(x['old']).get_text(' ',strip=True) in fragment(text).get_text(' ',strip=True) and fragment(x['new']).get_text(' ',strip=True) not in fragment(text).get_text(' ',strip=True):
                raise ValueError(f'Cleanup source changed: {x["path"]}: {x["old"][:90]}')
    order=PRIORITY+[x for x in catalog if x not in PRIORITY]
    for lang in LANGS:
        u=UI[lang];template=read(file_for(lang,'guides/qc-guide.html'))
        for slug,variants in catalog.items():
            v=variants[lang];p=file_for(lang,f'guides/{slug}.html');s=read(p) if p.exists() else deepcopy(template)
            a=s.article
            for el in a.select('[data-update-block],.related-links,.source-links,.site-breadcrumbs'):el.decompose()
            if slug in bodies:
                a.clear();append_html(a,f'<span class="eyebrow">{esc(u["independent"])}</span><h1>{esc(v["title"])}</h1><p class="byline">CSSBuys Pro Editorial · {esc(u["date"])}</p>'+v['body'])
            else:
                a.h1.string=v['title']
                if a.select_one('.lead'):a.select_one('.lead').string=v['description']
                by=a.select_one('.byline')
                if by:by.string='CSSBuys Pro Editorial · '+u['date']
                else:a.h1.insert_after(fragment(f'<p class="byline">CSSBuys Pro Editorial · {esc(u["date"])}</p>').p)
                if a.select_one('.eyebrow'):a.select_one('.eyebrow').string=u['independent']
                for el in a.select('.source-note'):el.decompose()
            if slug=='qc-guide':
                a.select_one('.byline').insert_after(fragment('<section data-update-block="qc" class="answer-box"><h2>'+esc(u['quick_title'])+'</h2><ul>'+''.join('<li>'+esc(x)+'</li>'for x in u['quick_items'])+'</ul></section>').section)
            if slug=='cssbuy-restricted-items-shipping':
                append_html(a,'<section data-update-block="battery"><h2>'+esc(u['battery_title'])+'</h2><ul>'+''.join('<li>'+esc(x)+'</li>'for x in u['battery_items'])+'</ul></section>')
            if slug=='cssbuy-pro-calculator-route-fees-guide':a.select_one('.byline').insert_after(fragment(weight_tool(lang)).section)
            if slug=='cssbuy-total-landed-cost-worksheet':a.select_one('.byline').insert_after(fragment(budget_tool(lang)).section)
            related=[x for x in PRIORITY if x!=slug][:6]
            append_html(a,f'<aside class="related-links"><h2>{esc(u["related"])}</h2>'+''.join(f'<p><a href="{route(lang,"/guides/"+x)}">{esc(catalog[x][lang]["title"])}</a></p>' for x in related)+'</aside>')
            if slug not in bodies:
                append_html(a,f'<section class="source-links"><h2>{esc(u["sources"])}</h2><ul><li><a href="https://m.cssbuy.com/buyforme">CSSBuy — Buy For Me</a></li><li><a href="https://www.cssbuy.com/estimates">CSSBuy — {esc(u["weight_title"])}</a></li><li><a href="https://www.cssbuy.com/shop/helpCenter?id=51">CSSBuy — QC</a></li></ul></section>')
            toc(s,a,lang)
            path=route(lang,'/guides/'+slug);metadata(s,lang,path,v['title'],v['description'],'Article');common(s,lang,path)
            p.parent.mkdir(parents=True,exist_ok=True);p.write_text(str(s))
        # Rebuild the article hub with the same 25 destinations in all six languages.
        p=file_for(lang,'guides/index.html');s=read(p);main=s.main
        cards=''.join(f'<a class="guide-card" href="{route(lang,"/guides/"+x)}"><div class="num">{i+1:02}</div><h3>{esc(catalog[x][lang]["title"])}</h3><p>{esc(catalog[x][lang]["description"])}</p></a>' for i,x in enumerate(order))
        main.clear();append_html(main,f'<section class="hero"><div class="wrap"><h1>{esc(u["hub_title"])}</h1><p class="lead">{esc(u["hub_intro"])}</p><div class="guide-grid">{cards}</div></div></section>')
        path=route(lang,'/guides/');metadata(s,lang,path,u['hub_title'],u['hub_intro'],'CollectionPage');common(s,lang,path);p.write_text(str(s))
        # FAQ and homepage share the verified buyer-focused answers.
        p=file_for(lang,'faq.html');s=read(p);s.article.clear()
        append_html(s.article,f'<h1>{esc(u["faq_title"])}</h1><p class="lead">{esc(u["faq_intro"])}</p>'+faqs_html(faq[lang]))
        path=route(lang,'/faq');metadata(s,lang,path,u['faq_title'],u['faq_intro']);faq_schema(s,faq[lang]);common(s,lang,path);p.write_text(str(s))
        p=file_for(lang,'index.html');s=read(p)
        s.h1.string=u['home_title'];s.select_one('.hero .lead').string=u['home_intro']
        controls=HOME_CONTROLS[lang];form=s.select_one('form[role="search"]')
        form.label.string=controls[0];form.select_one('input[type="search"]')['placeholder']=controls[1]
        form.button.string=controls[2];form.select_one('.search-hint').string=controls[3]
        s.select_one('#categories h2').string=controls[4]
        for node in s.select('#categories .card p'):node.string=controls[5]
        s.select_one('.hero .eyebrow').string=controls[7]
        guides=s.find(id='guides');grid=guides.select_one('.guide-grid');grid.clear();append_html(grid,''.join(str(x)for x in fragment(cards).select('.guide-card')[:6]))
        if guides.h2:guides.h2.string=u['latest']
        for x in guides.select('.all-guides'):x.decompose()
        append_html(guides.select_one('.wrap') or guides,f'<a class="btn all-guides" href="{route(lang,"/guides/")}">{esc(u["all"])}</a>')
        fg=s.select_one('.faq-grid');fg.find_parent('section').h2.string=controls[6];fg.replace_with(fragment(faqs_html(faq[lang][:8])).div)
        for x in s.select('[data-update-block="home-tools"]'):x.decompose()
        tools=f'<section class="section" data-update-block="home-tools"><div class="wrap"><div class="answer-box"><h2>{esc(u["tools_title"])}</h2><p>{esc(u["tools_text"])}</p><div class="actions"><a class="btn" href="{route(lang,"/guides/cssbuy-pro-calculator-route-fees-guide#weight-calculator")}">{esc(u["weight_cta"])}</a><a class="btn alt" href="{route(lang,"/guides/cssbuy-total-landed-cost-worksheet#cost-worksheet")}">{esc(u["budget_cta"])}</a></div></div></div></section>'
        s.select_one('.hero').insert_after(fragment(tools).section)
        path=route(lang,'/');metadata(s,lang,path,u['home_title'],u['home_intro'],'WebSite');common(s,lang,path);p.write_text(str(s))
        # Update the shared navigation on existing product pages, without changing their data or destinations.
        for p in file_for(lang,'products').glob('*.html'):
            s=read(p);common(s,lang,route(lang,'/products/'+p.stem));p.write_text(str(s))
    make_sitemap()
    print('Built 25 guides × 6 languages; 6 FAQs, 6 homepages, shared navigation and sitemaps.')

def make_sitemap():
    ns='http://www.sitemaps.org/schemas/sitemap/0.9';xh='http://www.w3.org/1999/xhtml'
    ET.register_namespace('',ns);ET.register_namespace('xhtml',xh)
    urlset=ET.Element('{'+ns+'}urlset');urls=[]
    for p in sorted(ROOT.rglob('*.html')):
        rel=p.relative_to(ROOT)
        if rel.as_posix()=='guides.html' or 'categories' in rel.parts or p.name=='404.html':continue
        s=read(p);c=s.find('link',rel='canonical');r=s.find('meta',attrs={'name':'robots'})
        if not c or not c.get('href','').startswith(DOMAIN) or (r and 'noindex' in r.get('content','')):continue
        url=c['href']
        if url in urls:continue
        urls.append(url);node=ET.SubElement(urlset,'{'+ns+'}url');ET.SubElement(node,'{'+ns+'}loc').text=url
        # Product and language pages retain their old substantive modification date.
        ET.SubElement(node,'{'+ns+'}lastmod').text=DATE if '/guides/' in url or url.endswith('/faq') or p.name=='index.html' else '2026-10-07'
        for a in s.select('link[rel="alternate"][hreflang]'):
            ET.SubElement(node,'{'+xh+'}link',{'rel':'alternate','hreflang':a['hreflang'],'href':a['href']})
    ET.indent(urlset);ET.ElementTree(urlset).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    (ROOT/'sitemap.txt').write_text('\n'.join(urls)+'\n')
    print('Sitemap URLs:',len(urls))

if __name__=='__main__':run()
