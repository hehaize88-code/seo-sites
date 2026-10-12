"""Build complete static language editions. No network or translation fallback."""
from pathlib import Path
from bs4 import BeautifulSoup,Comment,Doctype,Tag
from urllib.parse import urlsplit,urlunsplit
from html import escape
import json,re,hashlib,argparse

S=Path(__file__).parent; B=S.parent
ORIGIN='https://hoobuys.net'; DATE='2026-10-12'; RELEASE='multilingual-guides-20261012-logo-v2'
LANGS={'en':('','English'),'zh-CN':('zh-cn','简体中文'),'de':('de','Deutsch'),'fr':('fr','Français'),'es':('es','Español'),'it':('it','Italiano'),'pl':('pl','Polski'),'nl':('nl','Nederlands'),'pt':('pt','Português')}
CAT=json.loads((S/'catalog.json').read_text()); PAGES=json.loads((S/'pages.json').read_text()); UPDATES=json.loads((S/'updates.json').read_text()); DATES=json.loads((S/'dates.json').read_text())
INLINE=json.loads((S/'inline_translations.json').read_text())
ARTICLES=set(PAGES['articles']); SLUGS=set(PAGES['strings']); NS='http://www.sitemaps.org/schemas/sitemap/0.9'

def path(lang,slug):
    prefix=LANGS[lang][0]
    if slug=='index':return '/'+(prefix+'/' if prefix else '')
    return '/'+(prefix+'/' if prefix else '')+slug

def local_url(value,lang):
    u=urlsplit(value)
    if (u.netloc and u.netloc!='hoobuys.net') or u.scheme not in ['','https','http'] or not u.path.startswith('/'):return value
    slug=u.path.strip('/') or 'index'
    if slug.endswith('.html'):slug=slug[:-5]
    if slug not in SLUGS:return value
    return urlunsplit(('', '',path(lang,slug),u.query,u.fragment))

def tr(text,translations,override=None):
    normalized=text.strip();key=hashlib.sha256(normalized.encode()).hexdigest()[:12]
    if key not in CAT:return text
    if key not in translations:raise ValueError('Missing translation '+key)
    translated=translations[key] if override is None else override
    if not translated:return ''
    left=text[:len(text)-len(text.lstrip())]
    if translated[0] in '.,;:!?。；，、！：？':left=''
    return left+translated+text[len(text.rstrip()):]

def add_meta(s,attrs):s.head.append(s.new_tag('meta',attrs=attrs))
def add_link(s,attrs):s.head.append(s.new_tag('link',attrs=attrs))

def build_page(lang,slug,translations):
    s=BeautifulSoup((S/'en'/f'{slug}.html').read_text(),'html.parser')
    if lang!='en':
        inline_nodes=[]
        for text in list(s.find_all(string=True)):
            if text.parent.name not in ['script','style'] and not isinstance(text,(Comment,Doctype)):
                # Shared fragments need the noun's gender/case; mathematical A remains A.
                following=text.next_sibling
                context=None
                if isinstance(following,Tag):
                    first=hashlib.sha256(str(text).strip().encode()).hexdigest()[:12]
                    second=hashlib.sha256(following.get_text().strip().encode()).hexdigest()[:12]
                    context=INLINE.get(lang,{}).get(first+':'+second)
                if isinstance(context,dict):
                    if 'inline' in context:inline_nodes.append((following,context['inline']))
                    context=context.get('prefix')
                text.replace_with(tr(str(text),translations,context))
        for node,value in inline_nodes:node.clear();node.append(value)
        for el in s.find_all(True):
            for attr in ['alt','title','placeholder','aria-label']:
                if el.get(attr):el[attr]=tr(el[attr],translations)
            if el.name=='meta' and el.get('name')=='description':el['content']=tr(el['content'],translations)
    s.html['lang']=lang;s.html['data-release']=RELEASE
    for a in s.select('a[href]'):a['href']=local_url(a['href'],lang)
    # Server-independent, crawlable links work without JavaScript or cookies.
    box=s.select_one('[data-language-links]')
    for code,(_,label) in LANGS.items():
        a=s.new_tag('a',href=path(code,slug),hreflang=code,lang=code);a.string=label
        if code==lang:a['aria-current']='page'
        box.append(a)
    current=LANGS[lang][1]
    s.select_one('.language-menu summary').string=current
    for a in s.select('.site-header nav a'):
        if a.get('href')==path(lang,slug):a['aria-current']='page'
    title=s.title.get_text(strip=True);desc=s.find('meta',attrs={'name':'description'})['content'];url=ORIGIN+path(lang,slug)
    add_meta(s,{'name':'robots','content':'noindex,follow' if slug=='404' else 'index,follow,max-image-preview:large'})
    if slug!='404':
        add_link(s,{'rel':'canonical','href':url})
        for code in LANGS:add_link(s,{'rel':'alternate','hreflang':code,'href':ORIGIN+path(code,slug)})
        add_link(s,{'rel':'alternate','hreflang':'x-default','href':ORIGIN+path('en',slug)})
    for key,val in {'og:type':'article' if slug in ARTICLES else 'website','og:title':title,'og:description':desc,'og:url':url,'og:site_name':'HooBuys.net','og:locale':{'en':'en_US','zh-CN':'zh_CN','de':'de_DE','fr':'fr_FR','es':'es_ES','it':'it_IT','pl':'pl_PL','nl':'nl_NL','pt':'pt_PT'}[lang]}.items():add_meta(s,{'property':key,'content':val})
    for key,val in {'twitter:card':'summary','twitter:title':title,'twitter:description':desc}.items():add_meta(s,{'name':key,'content':val})
    graph=[{'@type':'WebSite','@id':ORIGIN+path(lang,'index')+'#website','url':ORIGIN+path(lang,'index'),'name':'HooBuys.net','inLanguage':lang},{'@type':'Organization','@id':ORIGIN+'/#organization','name':'HooBuys.net Editorial','url':ORIGIN+'/'}]
    page={'@type':'Article' if slug in ARTICLES else 'WebPage','@id':url+'#page','url':url,'name':title,'description':desc,'inLanguage':lang,'isPartOf':{'@id':ORIGIN+path(lang,'index')+'#website'}}
    if slug in ARTICLES:
        page.update({'headline':s.h1.get_text(' ',strip=True),'datePublished':DATES.get(slug,{}).get('datePublished',DATE),'dateModified':DATE,'mainEntityOfPage':{'@id':url},'author':{'@id':ORIGIN+'/#organization'},'publisher':{'@id':ORIGIN+'/#organization'},'isAccessibleForFree':True})
    graph.append(page)
    if slug in ARTICLES:
        home=s.select_one('.site-header nav a').get_text(strip=True)
        graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':home,'item':ORIGIN+path(lang,'index')},{'@type':'ListItem','position':2,'name':s.h1.get_text(' ',strip=True),'item':url}]})
    # Only visible FAQ answers are represented; no invented ratings or reviews.
    faq=[]
    for d in s.select('.faq-list details'):
        q=d.find('summary');p=d.find('p')
        if q and p:faq.append({'@type':'Question','name':q.get_text(' ',strip=True),'acceptedAnswer':{'@type':'Answer','text':p.get_text(' ',strip=True)}})
    if faq:graph.append({'@type':'FAQPage','mainEntity':faq,'inLanguage':lang})
    ld=s.new_tag('script',type='application/ld+json');ld.string=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('</',r'<\/');s.head.append(ld)
    ga=s.new_tag('script',src='https://www.googletagmanager.com/gtag/js?id=G-8SQR76WR85');ga['async']='';s.head.append(ga)
    ga=s.new_tag('script');ga.string="window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-8SQR76WR85');";s.head.append(ga)
    js=s.new_tag('script',src='/assets/site.js');js['defer']='';s.body.append(js)
    for table in list(s.find_all('table')):
        wrapper=s.new_tag('div',attrs={'class':'table-scroll','tabindex':'0','role':'region','aria-label':s.h1.get_text(' ',strip=True)})
        table.wrap(wrapper)
    out=B/(LANGS[lang][0] or '.')/f'{slug}.html';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(str(s)+'\n')
    return url

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--english-only',action='store_true');args=ap.parse_args()
    active=['en'] if args.english_only else list(LANGS)
    urls=[]
    for lang in active:
        if lang=='en':translations=CAT
        else:
            translations=json.loads((S/'i18n'/f'{lang}.json').read_text())
            if translations.keys()!=CAT.keys():raise ValueError(f'{lang}: translation key coverage differs')
            if any(not isinstance(v,str) or not v.strip() for v in translations.values()):raise ValueError(f'{lang}: invalid translation')
        for slug in sorted(SLUGS):
            url=build_page(lang,slug,translations)
            if slug!='404':urls.append((lang,slug,url))
    if not args.english_only:
        xml=['<?xml version="1.0" encoding="UTF-8"?>',f'<urlset xmlns="{NS}" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
        for lang,slug,url in urls:
            xml.append('<url><loc>'+escape(url)+'</loc><lastmod>'+DATE+'</lastmod>')
            for code in LANGS:xml.append(f'<xhtml:link rel="alternate" hreflang="{code}" href="{ORIGIN+path(code,slug)}"/>')
            xml.append(f'<xhtml:link rel="alternate" hreflang="x-default" href="{ORIGIN+path("en",slug)}"/></url>')
        xml.append('</urlset>');(B/'sitemap.xml').write_text('\n'.join(xml)+'\n');(B/'sitemap.txt').write_text('\n'.join(u for _,_,u in urls)+'\n')
    print(f'Built {len(active)*len(SLUGS)} HTML pages, {len(urls)} indexable URLs')

if __name__=='__main__':main()
