"""Rebuild the November 2026 CSSBuys DE editorial release, preserving legacy URLs."""
from pathlib import Path
from bs4 import BeautifulSoup
from html import escape
import re, json, copy
import xml.etree.ElementTree as ET
from config import LANGS, HREFLANG, DATE, UI, SLUGS, TITLES, COPY

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]/'cssbuys-de'
HOST='https://cssbuys.de'
NEW=['cssbuy-tyg-eu-tariffless-express','cssbuy-rehearsal-shipping','cssbuy-hoodies-jackets-spreadsheet']
def prefix(lang): return '' if lang=='en' else '/'+lang
def route(lang,slug=''): return prefix(lang)+'/guides/'+slug
def file_for(url):
    path=url.removeprefix(HOST).split('#')[0]
    return ROOT/(path.lstrip('/')+'index.html' if path.endswith('/') else path.lstrip('/')+'.html')
def soup(path): return BeautifulSoup(path.read_text(),'html.parser')
def fragment(text): return BeautifulSoup(text,'html.parser')
def inline(text,lang):
    text=escape(text,quote=False)
    text=re.sub(r'\[\[([^|]+)\|([^\]]+)\]\]',lambda m:f'<a href="{route(lang,m[1])}">{m[2]}</a>',text)
    return re.sub(r'\[([^\]]+)\]\((https://[^)]+)\)',lambda m:f'<a href="{m[2]}">{m[1]}</a>',text)
def content(lang):
    result={}
    for part in (HERE/'content'/f'{lang}.txt').read_text().split('@@ ')[1:]:
        slug,title,desc,lead,body=part.split('\n',4)
        result[slug]={'title':title,'desc':desc,'lead':lead,'body':body.strip()}
    return result
def shortdesc(text):
    if len(text)<=170:return text
    return text[:166].rsplit(' ',1)[0].rstrip('.,;:')+'…'
CONTENT={l:content(l) for l in LANGS}
def setmeta(s,title,desc,url,lang,published=None):
    s.html['lang']=HREFLANG[lang]
    s.title.string=title
    for attr,value in [('name','description'),('property','og:title'),('property','og:description'),('property','og:url')]:
        tag=s.find('meta',attrs={attr:value})
        if tag is None: tag=s.new_tag('meta',attrs={attr:value});s.head.append(tag)
        tag['content']={'description':desc,'og:title':title,'og:description':desc,'og:url':url}[value]
    canonical=s.find('link',rel='canonical');canonical['href']=url
    for tag in s.select('link[hreflang]'):tag.decompose()
    tail=url.removeprefix(HOST+prefix(lang))
    for l in LANGS+['x-default']:
        k='en' if l=='x-default' else l
        s.head.append(s.new_tag('link',attrs={'rel':'alternate','hreflang':l if l=='x-default' else HREFLANG[l],'href':HOST+prefix(k)+tail}))
    for tag in s.select('script[type="application/ld+json"]'):
        try:data=json.loads(tag.string or tag.get_text())
        except (ValueError,TypeError):continue
        entries=data if isinstance(data,list) else [data]
        for d in entries:
            if d.get('@type')=='Article':
                d.update(headline=title,description=desc,inLanguage=HREFLANG[lang],mainEntityOfPage=url,dateModified=DATE)
                if published:d['datePublished']=published
            elif d.get('@type')=='BreadcrumbList':
                items=d.get('itemListElement',[])
                if items:items[-1].update(name=title,item=url)
        tag.string=json.dumps(data,ensure_ascii=False)
    for attr in ['og:locale']:
        existing=s.find('meta',property=attr)
        if existing:existing.decompose()
def language_nav(s,lang,tail):
    nav=s.new_tag('nav',attrs={'class':'language-links','aria-label':UI[lang][9]})
    for l in LANGS:
        a=s.new_tag('a',href=prefix(l)+tail,attrs={'hreflang':HREFLANG[l]});a.string=l.upper()
        if l==lang:a['aria-current']='page'
        nav.append(a)
    return nav
def rebuild_toc(s,lang):
    a=s.select_one('article');old=a.select_one('.toc')
    if old:old.decompose()
    headings=a.find_all('h2');nav=s.new_tag('nav',attrs={'class':'toc','aria-label':UI[lang][9]})
    for i,h in enumerate(headings):
        h['id']=f'section-{i+1}'
        link=s.new_tag('a',href='#'+h['id']);link.string=h.get_text(' ',strip=True);nav.append(link)
    anchor=a.select_one('.answer-panel') or a.select_one('.meta') or a.h1
    anchor.insert_after(nav)
def related(s,lang,slugs):
    a=s.select_one('article')
    for old in a.select('.related-release'):old.decompose()
    block=s.new_tag('aside',attrs={'class':'related-release'})
    h=s.new_tag('h2');h.string=UI[lang][10];block.append(h)
    nav=s.new_tag('nav',attrs={'class':'related','aria-label':UI[lang][10]})
    for slug in slugs:
        title=CONTENT[lang][slug]['title'] if slug in NEW else TITLES[lang][SLUGS.index(slug)] if slug in SLUGS else soup(file_for(HOST+route(lang,slug))).h1.get_text(' ',strip=True)
        link=s.new_tag('a',href=route(lang,slug));link.string=title;nav.append(link)
    block.append(nav);a.append(block)
def shell(s,lang,tail):
    u=UI[lang];home=prefix(lang)+'/'
    links=[(home,u[0]),(route(lang,'cssbuy-spreadsheet'),u[1]),(route(lang,'qc-guide'),u[2]),(route(lang,'cssbuy-shipping-fees-weight-route-planning'),u[3]),(route(lang),u[4]),(prefix(lang)+'/faq',u[5]),('https://cnfanshp.com/AllProducts/',u[6])]
    for nav in s.select('.nav-links,.drawer-links'):
        nav.clear()
        for href,label in links:
            link=s.new_tag('a',href=href);link.string=label
            if href.startswith('https:'):link['class']='btn';link['data-outbound-placement']='navigation'
            nav.append(link)
    for a in s.select('a.brand'):a['href']=home
    for old in list(s.select('.language-links')):old.replace_with(language_nav(s,lang,tail))
    for a in s.select('a[href="/faq"]'):a['href']=prefix(lang)+'/faq'
    for x in s.select('script[src="/assets/site-events.js"]'):x['src']='/assets/site-events.js?v=20261102'
    if not s.select('script[src^="/assets/site-events.js"]'):
        s.head.append(s.new_tag('script',src='/assets/site-events.js?v=20261102',defer=''))
    if not s.select('link[href="/assets/seo-update.css"]'):
        s.head.append(s.new_tag('link',rel='stylesheet',href='/assets/seo-update.css'))
    for table in s.select('table'):
        heads=[t.get_text(' ',strip=True) for t in table.select('thead th')]
        for row in table.select('tbody tr'):
            for i,td in enumerate(row.find_all('td',recursive=False)):
                if i<len(heads):td['data-label']=heads[i]
    for a in s.select('a[href^="https://cnfanshp.com/"]'):
        if not a.get('data-outbound-placement'):a['data-outbound-placement']='article' if a.find_parent('article') else 'catalogue'
def write(path,s):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(str(s).rstrip()+'\n')

# New, fully localized articles; no English body fallback.
for lang in LANGS:
    template=soup(file_for(HOST+route(lang,'qc-guide')))
    for slug,item in CONTENT[lang].items():
        s=copy.deepcopy(template);a=s.select_one('article');a.clear();a['data-content-revision']=DATE
        a.append(fragment(f'<span class="eyebrow">{UI[lang][7]}</span>'))
        a.append(language_nav(s,lang,'/guides/'+slug))
        a.append(fragment(f'<h1>{escape(item["title"])}</h1><p class="lead">{escape(item["lead"])}</p><p class="meta">{UI[lang][8]}</p>'))
        for block in item['body'].split('\n\n'):
            if block.startswith('## '):
                heading,_,paragraph=block[3:].partition('\n')
                a.append(fragment('<h2>'+escape(heading)+'</h2>'))
                if paragraph:a.append(fragment('<p>'+inline(paragraph,lang)+'</p>'))
            else:a.append(fragment('<p>'+inline(block,lang)+'</p>'))
        setmeta(s,item['title'],item['desc'],HOST+route(lang,slug),lang,DATE)
        others={'cssbuy-tyg-eu-tariffless-express':['cssbuy-tracking-last-mile-germany-eu','cssbuy-rehearsal-shipping'], 'cssbuy-rehearsal-shipping':['cssbuy-shipping-fees-weight-route-planning','cssbuy-tyg-eu-tariffless-express'], 'cssbuy-hoodies-jackets-spreadsheet':['cssbuy-spreadsheet','qc-guide']}[slug]
        related(s,lang,others);rebuild_toc(s,lang);shell(s,lang,'/guides/'+slug);write(file_for(HOST+route(lang,slug)),s)

# Clean irrelevant publishing advice and add direct, localized answers to priority old guides.
for lang in LANGS:
    c=COPY[lang]
    for n,slug in enumerate(SLUGS):
        path=file_for(HOST+route(lang,slug));s=soup(path);a=s.select_one('article')
        if a.get('data-content-revision')!=DATE:
            ps=a.find_all('p',recursive=False)
            replacements={
              'w2c':{7:c[7],12:c[12],15:c[10],19:c[13]},
              'qc-guide':{15:c[10],17:c[9]},
              'cssbuy-shipping-fees-weight-route-planning':{6:c[12],11:c[11],17:c[13]},
              'cssbuy-spreadsheet':{6:c[7],7:c[8],9:c[10],11:c[9]}
            }.get(slug,{})
            for i,text in replacements.items():ps[i].clear();ps[i].append(text)
            if slug=='cssbuy-spreadsheet':
                heads=a.find_all('h2',recursive=False)
                # Remove four sections aimed at publishers rather than buyers.
                for h in heads[6:]:
                    node=h.next_sibling
                    while node and not (getattr(node,'name',None)=='h2'):
                        nxt=node.next_sibling
                        if getattr(node,'name',None) in ['div','aside','nav']:break
                        node.extract();node=nxt
                    h.decompose()
                labels={'en':['Choose by clothing or shoe requirements','Record the exact variant','Decide before packing'], 'de':['Nach Kleidung oder Schuhen auswählen','Die genaue Variante festhalten','Vor dem Verpacken entscheiden'], 'fr':['Choisir selon le type de produit','Noter la variante exacte','Décider avant l’emballage'], 'es':['Elegir según el producto','Anotar la variante exacta','Decidir antes de embalar'], 'it':['Scegliere secondo il prodotto','Annotare la variante esatta','Decidere prima di imballare'], 'pl':['Wybierz według rodzaju produktu','Zapisz dokładny wariant','Zdecyduj przed pakowaniem']}[lang]
                heads[2].string=labels[0]
                for label,txt in [(labels[1],c[8]),(labels[2],c[11]+' '+c[13])]:
                    a.append(fragment(f'<h2>{escape(label)}</h2><p>{escape(txt)}</p>'))
            if slug=='qc-guide' and lang=='de':
                ps[12].string='Ordnen Sie die Ergebnisse nach Bedeutung ein: falscher Artikel, falsche Größe, falsche Farbe, fehlende Hauptbestandteile oder deutliche Schäden verlangen eine Klärung vor dem Versand. Ein auffälliger Verarbeitungsmangel kann die Kaufentscheidung ändern. Kleine sichtbare Abweichungen können innerhalb Ihrer vorher festgelegten Toleranz liegen.'
            a['data-content-revision']=DATE
        a.h1.string=TITLES[lang][n]
        lead=a.select_one('.lead')
        if lead:lead.string=c[n]
        meta=a.select_one('.meta')
        if meta:meta.string=UI[lang][8]
        setmeta(s,TITLES[lang][n],shortdesc(c[n]),HOST+route(lang,slug),lang)
        # Replace awkward translated introductions in the existing payment answer box.
        if slug=='cssbuy-payment-methods-fees-refunds':
            box=a.select_one('.answer-panel')
            if box:
                box.find('h2').string=TITLES[lang][n]
                if box.find('p'):box.find('p').string=c[n]
        related_map={0:['cssbuy-payment-methods-fees-refunds','cssbuy-shipping-fees-weight-route-planning'],1:['cssbuy-rehearsal-shipping','cssbuy-coupons-2026'],2:['cssbuy-tyg-eu-tariffless-express'],3:['cssbuy-hoodies-jackets-spreadsheet','w2c','qc-guide'],4:['cssbuy-spreadsheet','cssbuy-hoodies-jackets-spreadsheet'],5:['cssbuy-hoodies-jackets-spreadsheet','cssbuy-returns-after-qc'],6:['cssbuy-rehearsal-shipping','cssbuy-tyg-eu-tariffless-express']}
        related(s,lang,related_map[n]);rebuild_toc(s,lang);shell(s,lang,'/guides/'+slug);write(path,s)

# Dedicated FAQ pages in every language, matching visible answers in structured data.
QUESTIONS={
'en':['How do I use a CSSBuy spreadsheet?','What should I check in QC photos?','How do I compare shipping costs?','How do CSSBuy payments and refunds differ?','Is there a verified universal coupon?','What does tracking without updates mean?'],
'de':['Wie nutze ich ein CSSBuy Spreadsheet?','Was prüfe ich auf QC-Fotos?','Wie vergleiche ich Versandkosten?','Wie unterscheiden sich Zahlung, Guthaben und Erstattung?','Gibt es einen bestätigten allgemeinen Gutscheincode?','Was bedeutet Tracking ohne Aktualisierung?'],
'fr':['Comment utiliser un spreadsheet CSSBuy ?','Que vérifier sur les photos QC ?','Comment comparer les frais de livraison ?','Comment distinguer paiement, solde et remboursement ?','Existe-t-il un code universel vérifié ?','Que faire sans mise à jour du suivi ?'],
'es':['¿Cómo uso un spreadsheet CSSBuy?','¿Qué reviso en las fotos QC?','¿Cómo comparo gastos de envío?','¿Cómo distingo pago, saldo y reembolso?','¿Existe un código universal verificado?','¿Qué hago si el seguimiento no cambia?'],
'it':['Come uso uno spreadsheet CSSBuy?','Cosa controllo nelle foto QC?','Come confronto i costi di spedizione?','Come distinguo pagamento, saldo e rimborso?','Esiste un codice universale verificato?','Cosa fare senza aggiornamenti del tracking?'],
'pl':['Jak korzystać z tabeli CSSBuy?','Co sprawdzić na zdjęciach QC?','Jak porównać koszty wysyłki?','Jak odróżnić płatność, saldo i zwrot?','Czy jest potwierdzony kod uniwersalny?','Co zrobić bez aktualizacji śledzenia?']}
for lang in LANGS:
    s=soup(file_for(HOST+route(lang,'qc-guide')));a=s.select_one('article');a.clear()
    title='CSSBuy FAQ';a.append(language_nav(s,lang,'/faq'));a.append(fragment(f'<h1>{title}</h1><p class="meta">{UI[lang][8]}</p>'))
    data=[]
    for q,i in zip(QUESTIONS[lang],[3,5,6,1,0,2]):
        a.append(fragment(f'<h2>{escape(q)}</h2><p>{escape(COPY[lang][i])}</p><p><a href="{route(lang,SLUGS[i])}">{escape(TITLES[lang][i])}</a></p>'))
        data.append({'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':COPY[lang][i]}})
    setmeta(s,title,' '.join(QUESTIONS[lang][:3]),HOST+prefix(lang)+'/faq',lang)
    for tag in s.select('script[type="application/ld+json"]'):tag.decompose()
    script=s.new_tag('script',type='application/ld+json');script.string=json.dumps({'@context':'https://schema.org','@type':'FAQPage','inLanguage':HREFLANG[lang],'mainEntity':data},ensure_ascii=False);s.head.append(script)
    rebuild_toc(s,lang);shell(s,lang,'/faq');write(file_for(HOST+prefix(lang)+'/faq'),s)

# Refresh hub and six-card homepage feed from actual article metadata.
all_slugs=NEW+SLUGS+['cssbuy-warehouse-storage-deadlines','cssbuy-returns-after-qc','cssbuy-links-not-working','cssbuy-shoes-spreadsheet-sizing-qc','cssbuy-reviews-trustpilot-2026','cssbuy-germany-address-format','cssbuy-germany-customs-tax-planning','cssbuy-germany-restricted-item-screening','cssbuy-germany-w2c-qc-shipping-2026','cssbuy-insurance-claims-germany-eu','cssbuy-parcel-consolidation-germany','cssbuy-shipping-calculator-germany-eu']
assert len(set(all_slugs))==22
def card(lang,slug):
    p=soup(file_for(HOST+route(lang,slug)));title=p.h1.get_text(' ',strip=True);desc=p.find('meta',attrs={'name':'description'})['content']
    return fragment(f'<a class="guide-card" href="{route(lang,slug)}"><h3>{escape(title)}</h3><p>{escape(desc)}</p></a>')
for lang in LANGS:
    for home in [False,True]:
        path=file_for(HOST+(prefix(lang)+'/' if home else route(lang)));s=soup(path)
        target=s.select_one('.latest-guides .guide-grid') if home else s.select_one('.guide-grid')
        target.clear()
        for slug in (NEW+SLUGS[:3] if home else all_slugs):target.append(card(lang,slug))
        if home:
            latest=s.select_one('.latest-guides');latest['class']=['section','latest-guides'];latest['id']='guides'
            for a in s.select('.all-guides-action a'):a.string=UI[lang][11]
        else:
            lead=s.select_one('.lead')
            if lead:lead.string=UI[lang][13]
            desc=s.find('meta',attrs={'name':'description'});desc['content']=UI[lang][13]
        shell(s,lang,'/' if home else '/guides/');write(path,s)

# Apply correct language switching/navigation to all active localized pages.
for path in ROOT.rglob('*.html'):
    rel=path.relative_to(ROOT);parts=rel.parts;lang=parts[0] if parts[0] in LANGS[1:] else 'en'
    s=soup(path)
    if not s.head or not s.body:continue
    robot=s.find('meta',attrs={'name':'robots'})
    if robot and 'noindex' in robot.get('content',''):continue
    can=s.find('link',rel='canonical')
    if not can:continue
    tail=can['href'].removeprefix(HOST+prefix(lang))
    # Only expose language alternates when the counterpart actually exists.
    if not all(file_for(HOST+prefix(l)+tail).exists() for l in LANGS):continue
    shell(s,lang,tail);write(path,s)

# Keep the existing sitemap's valid policy URLs; append all new localized URLs.
sm=ROOT/'sitemap.xml';ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
old=ET.fromstring(sm.read_text());entries={u.find('s:loc',ns).text:(u.findtext('s:lastmod',default='',namespaces=ns)) for u in old.findall('s:url',ns)}
for lang in LANGS:
    for url in [HOST+route(lang,x) for x in NEW+SLUGS]+[HOST+prefix(lang)+'/',HOST+route(lang),HOST+prefix(lang)+'/faq']:entries[url]=DATE
root=ET.Element('urlset',xmlns=ns['s'])
for url,last in sorted(entries.items()):
    node=ET.SubElement(root,'url');ET.SubElement(node,'loc').text=url
    if last:ET.SubElement(node,'lastmod').text=last
ET.indent(root);sm.write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(root,encoding='unicode')+'\n')
(ROOT/'sitemap.txt').write_text('\n'.join(sorted(entries))+'\n')
print(f'Built 18 new articles, refreshed 42 priority articles, 6 FAQs and 12 hubs/homepages; sitemap: {len(entries)} URLs')
