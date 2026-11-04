"""Build all eight static editions while keeping established canonical URLs."""
import html,json,re,shutil
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
from xml.sax.saxutils import escape
BASE=Path(__file__).resolve().parent
SITE=BASE.parents[1]/'hipobuys-uk'
ORIGIN='https://hipobuys.uk'
DATE='2026-11-04'
UI=json.loads((BASE/'ui.json').read_text());SOURCE=json.loads((BASE/'source.json').read_text())
ORDER=['broken','rehearsal','fees','hipobuy-uk-shipping-line-selection']+[k for k in SOURCE if k not in ['broken','rehearsal','fees','hipobuy-uk-shipping-line-selection','faq']]
SLUGS={
'fees':['hipobuy-fees','hipobuy-uk-fees','frais-hipobuy','tarifas-hipobuy','costi-hipobuy','koszty-hipobuy','taxas-hipobuy','hipobuy-kosten'],
'coupon':['hipobuy-coupon','hipobuy-uk-coupons','coupon-hipobuy','cupon-hipobuy','coupon-hipobuy','kupon-hipobuy','cupom-hipobuy','hipobuy-korting'],
'qc':['qc-photos','hipobuy-uk-qc','photos-qc','fotos-qc','foto-qc','zdjecia-qc','fotos-qc','qc-fotos'],
'w2c':['w2c-links','hipobuy-uk-links','liens-w2c','enlaces-w2c','link-w2c','linki-w2c','links-w2c','w2c-links'],
'shipping':['shipping-from-china','hipobuy-uk-shipping','livraison-depuis-la-chine','envio-desde-china','spedizione-dalla-cina','wysylka-z-chin','envio-da-china','verzending-uit-china']}
LANGS=list(UI)
def route(lang,key):
    if key=='languages':return '/languages'
    if key=='home':return '/de/uk/' if lang=='de' else '/'+lang+'/'
    if key=='index':return '/guides' if lang=='en' else '/'+lang+'/articles/'
    if key=='faq':return '/faq' if lang=='en' else '/'+lang+'/faq/'
    if key in SLUGS:return '/'+lang+'/'+SLUGS[key][LANGS.index(lang)]+'/'
    if lang=='en':return SOURCE[key]['path']
    return '/'+lang+'/articles/'+({'broken':'hipobuy-links-not-working','rehearsal':'hipobuy-rehearsal-parcel-uk'}.get(key,key))+'/'
ROUTES={l:{k:route(l,k) for k in [*SOURCE,'home','index']} for l in LANGS}
REVERSE={v['path']:k for k,v in SOURCE.items()}
ALIASES={'@fees':'fees','@lines':'hipobuy-uk-shipping-line-selection','@rehearsal':'rehearsal','@broken':'broken','@qc':'qc'}
def e(s):return html.escape(str(s),quote=True)
def links(lang,key):
    if key=='languages':return ''
    return ''.join(f'<link rel="alternate" hreflang="{UI[l]["lang"]}" href="{ORIGIN}{route(l,key)}">' for l in LANGS)+f'<link rel="alternate" hreflang="x-default" href="{ORIGIN}{route("en",key)}">'
def language_nav(lang,key):
    if key=='languages':key='home'
    return '<nav class="locale-nav" aria-label="'+e(UI[lang]['language'])+'">'+''.join(f'<a href="{route(l,key)}" lang="{UI[l]["lang"]}" hreflang="{UI[l]["lang"]}"'+(' aria-current="page"' if l==lang else '')+'>'+UI[l]['name']+'</a>' for l in LANGS)+'</nav>'
def header(lang):
    u=UI[lang]
    return '<header class="top"><a class="brand" href="'+route(lang,'home')+'"><img src="/assets/images/hipobuy-logo.png" alt="HipoBuys UK" width="488" height="112"></a><nav class="nav">'+''.join(f'<a href="{href}">{e(label)}</a>' for href,label in [(route(lang,'home'),u['home']),('/products',u['products']),(route(lang,'qc'),u['qc']),(route(lang,'shipping'),u['shipping']),(route(lang,'fees'),u['fees']),(route(lang,'faq'),u['faq']),(route(lang,'index'),u['articles'])])+'</nav></header>'
def shell(lang,key,title,desc,body,kind='Article'):
    u=UI[lang];canonical=ORIGIN+route(lang,key)
    schema={'@context':'https://schema.org','@graph':[{'@type':kind,'headline':title,'name':title,'description':desc,'inLanguage':u['lang'],'url':canonical,'mainEntityOfPage':canonical,'dateModified':DATE,'publisher':{'@type':'Organization','name':'HipoBuys UK'}},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':u['home'],'item':ORIGIN+route(lang,'home')},{'@type':'ListItem','position':2,'name':u['articles'] if key!='home' else title,'item':canonical}]}]}
    if key in ['broken','rehearsal']:schema['@graph'][0]['datePublished']=DATE
    if key=='faq':
        soup=BeautifulSoup(body,'html.parser'); schema['@graph'].append({'@type':'FAQPage','mainEntity':[{'@type':'Question','name':h.get_text(' ',strip=True),'acceptedAnswer':{'@type':'Answer','text':h.find_next_sibling('p').get_text(' ',strip=True)}} for h in soup.find_all('h2') if h.find_next_sibling('p')]})
    return f'''<!doctype html><html lang="{u['lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}">{links(lang,key)}<link rel="icon" href="/assets/svg/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/css/editorial.css?v=20261104"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:type" content="{'article' if kind=='Article' else 'website'}"><meta property="og:site_name" content="HipoBuys UK"><meta name="twitter:card" content="summary"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace('</','<\\/')}</script><script async src="https://www.googletagmanager.com/gtag/js?id=G-GYK9GRD9N8"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-GYK9GRD9N8');</script></head><body>{header(lang)}{language_nav(lang,key)}<main><section class="hero"><div class="hero-inner"><h1>{e(title)}</h1><p>{e(desc)}</p><div class="meta">{e(u['updated'])} <time datetime="{DATE}">{DATE}</time> · HipoBuys UK</div></div></section>{body}</main><footer class="footer"><div class="footer-inner"><strong>HipoBuys UK</strong><p>{e(u['notice'])}</p><nav><a href="{route(lang,'index')}">{e(u['articles'])}</a><a href="{route(lang,'faq')}">{e(u['faq'])}</a><a href="/privacy">Privacy</a><a href="/disclaimer">Disclaimer</a></nav></div></footer><script defer src="/assets/js/analytics.js?v=20261104"></script></body></html>'''
def save(path,content):
    file=SITE/(path.strip('/')+'/index.html' if path.endswith('/') else path.lstrip('/')+'.html')
    file.parent.mkdir(parents=True,exist_ok=True);file.write_text(content)
generated=[]
for lang in LANGS:
    content=SOURCE if lang=='en' else json.loads((BASE/f'content.{lang}.json').read_text())
    if set(content)!=set(SOURCE):raise ValueError((lang,'missing translations'))
    u=UI[lang]
    for k,label in [('fees','fees_title'),('hipobuy-uk-shipping-line-selection','lines_title'),('broken','broken_title'),('rehearsal','rehearsal_title')]:content[k]['title']=u[label]
    for key,item in content.items():
        soup=BeautifulSoup(item['body'],'html.parser')
        for a in soup.find_all('a',href=True):
            href=a['href'];parts=urlsplit(href)
            if href in ALIASES:a['href']=route(lang,ALIASES[href])
            elif parts.netloc in ['', 'hipobuys.uk','www.hipobuys.uk']:
                p=parts.path.removesuffix('.html')
                if p in REVERSE:a['href']=route(lang,REVERSE[p])+('#'+parts.fragment if parts.fragment else '')
                elif p in ['/guides','/en/articles/']:a['href']=route(lang,'index')
                elif p in ['/faq']:a['href']=route(lang,'faq')
            if urlsplit(a['href']).netloc:a['rel']='noopener noreferrer'
        toc=[]
        for i,h in enumerate(soup.find_all('h2')):
            if not h.get('id'):h['id']='section-'+str(i+1)
            toc.append('<li><a href="#'+h['id']+'">'+e(h.get_text(' ',strip=True))+'</a></li>')
        for table in soup.find_all('table'):
            if 'table-wrap' not in table.parent.get('class',[]):
                wrapper=soup.new_tag('div',attrs={'class':'table-wrap'});table.wrap(wrapper)
        intro='<details class="toc"><summary>'+e(u['contents'])+'</summary><ol>'+''.join(toc)+'</ol></details>'
        related=[k for k in ['fees','hipobuy-uk-shipping-line-selection','broken','rehearsal','qc'] if k!=key]
        tail='<h2>'+e(u['related'])+'</h2><div class="related">'+''.join('<a data-article-link href="'+route(lang,k)+'">'+e(content[k]['title'])+'</a>' for k in related)+'</div>'
        tail+='<aside class="cta-box"><p>'+e(u['notice'])+'</p><a class="button" href="https://cnfanshp.com/AllProducts/?utm_source=hipobuys.uk&amp;utm_medium=referral&amp;utm_campaign=buyer_guides" rel="noopener" target="_blank">'+e(u['browse'])+'</a></aside>'
        body='<article class="article">'+intro+str(soup)+tail+'</article>'
        save(route(lang,key),shell(lang,key,item['title'],item['description'],body,'WebPage' if key=='faq' else 'Article'));generated.append(route(lang,key))
    cards='<div class="cards">'+''.join('<article class="card"><h2><a data-article-link href="'+route(lang,k)+'">'+e(content[k]['title'])+'</a></h2><p>'+e(content[k]['description'])+'</p><a data-article-link href="'+route(lang,k)+'">'+e(u['read'])+' →</a></article>' for k in ORDER)+'</div>'
    for key,title in [('home',u['title']),('index',u['all']+' | HipoBuys UK')]:
        save(route(lang,key),shell(lang,key,title,u['intro'],'<section class="catalogue"><h2>'+e(u['all'])+'</h2>'+cards+'</section>','CollectionPage'));generated.append(route(lang,key))

shutil.copyfile(BASE/'editorial.css',SITE/'assets/css/editorial.css')
(BASE/'routes.json').write_text(json.dumps(ROUTES,ensure_ascii=False,indent=2))
# Root landing page keeps its products and layout, gaining visible new articles and all language entries.
root=BeautifulSoup((SITE/'index.html').read_text(),'html.parser')
for old in root.select('#november-guides'):old.decompose()
block=BeautifulSoup('<section id="november-guides" class="section"><h2>New Hipobuy UK guides</h2><p>Fix a product link, check your packed parcel and compare the full cost before shipping.</p>'+language_nav('en','index')+'<div class="grid">'+''.join('<article class="guide-tile"><h3><a href="'+route('en',k)+'">'+e(UI['en'][label])+'</a></h3><p>'+e(SOURCE[k]['description'])+'</p></article>' for k,label in [('broken','broken_title'),('rehearsal','rehearsal_title'),('fees','fees_title'),('hipobuy-uk-shipping-line-selection','lines_title')])+'</div></section>','html.parser')
root.main.insert(1,block)
for a in root.find_all('a',href=True):
    if a['href']=='https://hipobuys.de/de/':a['href']=route('de','home')
nav=root.find('nav')
if nav and not nav.find('a',string='Articles'):
    a=root.new_tag('a',href='/guides');a.string='Articles';nav.append(a)
(SITE/'index.html').write_text(str(root))
# A standalone, crawlable language directory.
save('/languages',shell('en','languages','Hipobuy UK language editions','The same buyer guides in eight languages.','<section class="catalogue">'+language_nav('en','home')+'</section>','CollectionPage'))
# Sitemap includes only canonical local URLs, excluding legacy redirects and stale aliases.
urls={ORIGIN+'/',ORIGIN+'/languages'}
for p in SITE.rglob('*.html'):
    soup=BeautifulSoup(p.read_text(),'html.parser');canonical=soup.find('link',rel='canonical');robots=soup.find('meta',attrs={'name':'robots'})
    if not canonical or (robots and 'noindex' in robots.get('content','')):continue
    c=canonical.get('href','');path=urlsplit(c).path
    if c.startswith(ORIGIN+'/') and not path.endswith('.html') and path not in ['/hipobuy-uk-qc-w2c-shipping-check-2026-07-10','/daily-seo/hipobuy-uk-vat-qc-parcel-guide-2026-07-09']:urls.add(c)
xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('<url><loc>'+escape(x)+'</loc>'+('<lastmod>'+DATE+'</lastmod>' if urlsplit(x).path in generated or x==ORIGIN+'/' else '')+'</url>\n' for x in sorted(urls))+'</urlset>\n'
(SITE/'sitemap.xml').write_text(xml);(SITE/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n')
print('Built',len(ORDER),'articles per language;',len(generated),'localized pages;',len(urls),'sitemap URLs')
