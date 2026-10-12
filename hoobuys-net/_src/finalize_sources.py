"""Prepare shared English layouts and a deduplicated translation catalogue."""
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment
from html import escape as e
import json,re,hashlib
S=Path(__file__).parent; EN=S/'en'
U=json.loads((S/'updates.json').read_text())
names=['hoobuy-product-spreadsheet-links-guide','hoobuy-qc-photos-measurements-guide','hoobuy-process-pending-guide','shipping-guide']
docs={f.stem:BeautifulSoup(f.read_text(),'html.parser') for f in EN.glob('*.html')}
article_slugs=[n for n,s in docs.items() if s.select_one('article.article, article.guide') or n.startswith(('hoobuy-','modify-hoobuy-')) or n=='shipping-guide']
article_slugs=names+sorted(n for n in article_slugs if n not in names)
titles={n:docs[n].h1.get_text(' ',strip=True) for n in article_slugs}
descs={n:docs[n].find('meta',attrs={'name':'description'})['content'] for n in article_slugs}

def card(n):
    return f'<a class="guide-card" href="/{n}"><h3>{e(titles[n])}</h3><p>{e(descs[n])}</p></a>'
def replace_contents(tag,html):tag.clear();tag.append(BeautifulSoup(html,'html.parser'))

s=docs['index']
s.title.string='Hoobuy Spreadsheet, QC Photos & Shipping Guides | HooBuys.net'
s.find('meta',attrs={'name':'description'})['content']='Find Hoobuy product links, understand QC photos, prepare shipping estimates and resolve order-status questions with practical independent guides.'
s.h1.string='Hoobuy Spreadsheet, QC & Shipping Guides'
s.select_one('.hero .eyebrow').string='Find products · Check your item · Plan your parcel'
s.select_one('.hero p').string='Choose useful product links, read warehouse QC photos and understand the next order step. Start with a practical guide, then confirm prices, options and service rules in the live account.'
replace_contents(s.select_one('.hero .actions'),'<a class="btn" href="/hoobuy-product-spreadsheet-links-guide">Find product links</a><a class="btn secondary" href="/shipping-guide">Plan shipping costs</a>')
section=s.select_one('section[aria-labelledby="guides-title"]')
replace_contents(section,'<div class="section-head"><div><h2 id="guides-title">Latest guides and useful updates</h2><p>Choose the next decision you need to make.</p></div><a class="link" href="/articles">All articles →</a></div><div class="grid2 latest-grid">'+''.join(card(n) for n in names)+'</div>')
s.select_one('#products-title').string='Product discovery examples'
s.select_one('#products-title').parent.find('p').string='Previously selected product examples. Recheck the destination, selected option and live price before ordering; the figures below are historical estimates, not current quotes.'

for hub in ['articles','guides']:
    s=docs[hub]
    title='Hoobuy Articles: Spreadsheet, QC, Shipping & Order Status' if hub=='articles' else 'Hoobuy Guides: Choose Your Next Step'
    s.title.string=title
    s.find('meta',attrs={'name':'description'})['content']='Browse complete Hoobuy guides for product discovery, QC photos, shipping calculations, order status, warehouse intake and parcel decisions.'
    if hub=='articles':
        content='<section class="hero"><div class="eyebrow">Independent buyer library</div><h1>'+title+'</h1><p>Read the guide that matches your current task. The complete collection covers product research through parcel tracking.</p></section><section class="section"><div class="grid2">'+''.join(card(n) for n in article_slugs)+'</div></section>'
    else:
        groups=[('Find and compare products',['hoobuy-product-spreadsheet-links-guide','hoobuy-qc-photos-measurements-guide','hoobuy-spreadsheet-guide']),('Purchase and resolve order messages',['hoobuy-process-pending-guide','hoobuy-order-status-purchase-dispatch-qc-storage-2026','hoobuy-pending-for-confirmation-status-2026','hoobuy-paid-order-outstanding-balance-2026','modify-hoobuy-order-after-submission-2026','hoobuy-purchase-failed-order-cancelled-status-2026']),('Follow the warehouse handoff',[n for n in article_slugs if any(x in n for x in ['seller-sent','delivered-but','forwarding-order','split-domestic','receipt-mismatch','order-id','returns-exchanges'])]),('Prepare and follow the international parcel',[])]
        used={n for _,ls in groups for n in ls};groups[-1][1].extend(n for n in article_slugs if n not in used)
        content='<section class="hero"><div class="eyebrow">Discovery · Warehouse · International parcel</div><h1>'+title+'</h1><p>Start at the last event you can verify, then choose the guide that explains the missing information or next decision.</p></section>'
        for label,slugs in groups:content+='<section class="section"><h2>'+label+'</h2><div class="grid2">'+''.join(card(n) for n in slugs)+'</div></section>'
    replace_contents(s.find('main'),content)

s=docs['languages'];s.title.string='Languages | HooBuys.net'
replace_contents(s.find('main'),'''<section class="hero"><div class="eyebrow">Nine complete editions</div><h1>Choose your reading language</h1><p>Read the full guides in English, Chinese, German, French, Spanish, Italian, Polish, Dutch or Portuguese. The language menu opens the matching page in your chosen language.</p></section><section class="section box"><h2>Keep exact operational labels</h2><p>Translated guides explain the same workflows and examples. When contacting support, preserve the status wording, product variant and identifiers from your own account. Check current service conditions before acting.</p><h2>Read the complete article collection</h2><p><a href="/articles">Browse all articles</a> or use the language menu to continue in another edition.</p></section>''')
s.find('meta',attrs={'name':'description'})['content']='Read the complete HooBuys.net guides in nine languages and switch directly to the matching article.'

s=docs['products'];s.title.string='Hoobuy Product Discovery: Links, Search & QC Notes'
s.h1.string='Product Discovery: Search, Compare and Save'
s.find('meta',attrs={'name':'description'})['content']='Search the linked product catalogue and learn which variant, size and QC details to save before ordering.'
s.select_one('.hero .eyebrow').string='External catalogue · Selected examples · Buyer checks'
s.select_one('.notice p').string='These examples were selected in August 2026. Displayed USD amounts are historical estimates using ¥1 ≈ $0.14. Current prices, availability and seller details must be confirmed at the destination.'
s.select_one('#products-title').string='Eight product discovery examples'
s.select_one('.hero').append(BeautifulSoup('<p><a href="/hoobuy-product-spreadsheet-links-guide">Read the product spreadsheet guide</a> · <a href="/hoobuy-qc-photos-measurements-guide">Learn what QC photos can show</a></p>','html.parser'))

# Remove navigation inconsistencies and all runtime translation scripts.
nav='<a href="/">Home</a><a href="/articles">Articles</a><a href="/guides">Guides</a><a href="/products">Products</a><a href="/faq">FAQ</a>'
header='<a class="skip" href="#content">Skip to content</a><header class="site-header"><div class="wrap header-row"><a class="site-brand" href="/">hoobuys<span>.</span>net<small>Independent buyer guides</small></a><nav aria-label="Main navigation">'+nav+'</nav><details class="language-menu"><summary>Language</summary><div class="language-options" data-language-links></div></details></div></header>'
footer='<footer class="site-footer wrap"><p>HooBuys.net · Independent buyer guides. This website is not Hoobuy.</p><nav aria-label="Footer navigation"><a href="/about">About</a><a href="/editorial-policy">Editorial policy</a><a href="/privacy">Privacy</a><a href="/terms">Terms</a><a href="/languages">Languages</a><a href="/sitemap.xml">Sitemap</a></nav></footer>'
for n,s in docs.items():
    # Old sources use conflicting per-page style and schema; metadata is built consistently later.
    main=s.find('main'); main['id']='content'
    for m in main.select('p.meta'):
        if 'Published' in m.get_text() or 'fact-checked' in m.get_text():
            old=re.search(r'(August|September) \d+, 2026',m.get_text())
            if n in U['new']:m.string='Published: October 12, 2026'
            elif n in U['updated']:m.string='Updated: October 12, 2026'
            elif old:m.string='Published: '+old.group(0)
    if n in article_slugs:
        a=main.find('article');a['class']=['article'];a['id']='main-article'
        # Leave existing body intact, and add task-relevant onward links.
        if n not in U['new']:
            a.append(BeautifulSoup('<section class="related"><h2>Continue with a related guide</h2><p><a href="/hoobuy-product-spreadsheet-links-guide">Product links and spreadsheet checks</a> · <a href="/hoobuy-qc-photos-measurements-guide">QC photos and measurements</a> · <a href="/shipping-guide">Shipping calculator preparation</a> · <a href="/hoobuy-process-pending-guide">Process Pending troubleshooting</a></p></section>','html.parser'))
        if n=='hoobuy-order-status-purchase-dispatch-qc-storage-2026':
            for h in a.find_all('h2'):
                if 'QC' in h.get_text():h['id']='qc-and-storage';break
    title=s.title.get_text();meta=s.find('meta',attrs={'name':'description'});desc=meta['content'] if meta else title
    clean=BeautifulSoup('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title></title><meta name="description" content=""><link rel="stylesheet" href="/assets/styles.css"></head><body></body></html>','html.parser')
    clean.title.string=title;clean.find('meta',attrs={'name':'description'})['content']=desc
    clean.body.append(BeautifulSoup(header,'html.parser'));clean.body.append(main);clean.body.append(BeautifulSoup(footer,'html.parser'))
    for comment in clean.find_all(string=lambda t:isinstance(t,Comment)):comment.extract()
    (EN/(n+'.html')).write_text(str(clean))

def translatable(t):
    return bool(re.search(r'[A-Za-z]',t)) and t not in ['hoobuys','.','net','HooBuys.net','QC','USD','cm','kg'] and not re.fullmatch(r'[\d\W]+',t)
def iter_strings(s):
    for text in s.find_all(string=True):
        if text.parent.name not in ['script','style'] and not isinstance(text,Comment):
            t=str(text).strip()
            if translatable(t):yield t
    for el in s.find_all(True):
        for attr in ['alt','title','placeholder','aria-label']:
            if el.get(attr) and translatable(el[attr]):yield el[attr]
        if el.name=='meta' and el.get('name')=='description':yield el['content']
catalog={}; pages={}
for f in sorted(EN.glob('*.html')):
    strings=list(iter_strings(BeautifulSoup(f.read_text(),'html.parser')))
    pages[f.stem]=[]
    for t in strings:
        k=hashlib.sha256(t.encode()).hexdigest()[:12];catalog[k]=t;pages[f.stem].append(k)
(S/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2))
(S/'pages.json').write_text(json.dumps({'articles':article_slugs,'strings':pages},indent=2))
chunks=S/'chunks';chunks.mkdir(exist_ok=True)
out={};words=0;i=0
for k,t in catalog.items():
    out[k]=t;words+=len(t.split())
    if words>1800:
        (chunks/f'{i:02}.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));out={};words=0;i+=1
if out:(chunks/f'{i:02}.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(len(docs),'pages;',len(article_slugs),'articles;',len(catalog),'unique strings;',sum(len(t.split()) for t in catalog.values()),'words;',i+1,'translation chunks')
