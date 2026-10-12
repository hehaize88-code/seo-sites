"""Validate crawl paths, complete localization and generated metadata."""
from pathlib import Path
from bs4 import BeautifulSoup,Comment
from urllib.parse import urlsplit
from collections import Counter
import json,re,xml.etree.ElementTree as ET
from build import B,S,LANGS,SLUGS,ARTICLES,CAT,ORIGIN,path

errors=[];docs={};checks=0
def check(test,msg):
    global checks
    checks+=1
    if not test:errors.append(msg)

for lang in LANGS:
    if lang!='en':
        f=S/'i18n'/f'{lang}.json'
        check(f.exists(),f'Missing translation asset {lang}')
        if not f.exists():continue
        tr=json.loads(f.read_text());check(tr.keys()==CAT.keys(),f'Key coverage {lang}')
        for k,v in tr.items():
            check(isinstance(v,str) and bool(v.strip()),f'Empty translation {lang}/{k}')
            if len(CAT[k].split())>=12:check(v!=CAT[k],f'English paragraph retained {lang}/{k}')
    for slug in SLUGS:
        file=B/(LANGS[lang][0] or '.')/(slug+'.html')
        check(file.exists(),f'Missing {lang}/{slug}')
        if not file.exists():continue
        s=BeautifulSoup(file.read_text(),'html.parser');docs[path(lang,slug)]=s
        check(s.html.get('lang')==lang,f'HTML language {lang}/{slug}')
        check(len(s.find_all('h1'))==1,f'H1 count {lang}/{slug}')
        check(bool(s.title and s.title.get_text(strip=True)),f'Missing title {lang}/{slug}')
        check(bool(s.select_one('meta[name="description"]').get('content')),f'Description {lang}/{slug}')
        check(len(s.select('script[src*="googletagmanager.com/gtag"]'))==1,f'Analytics duplication {lang}/{slug}')
        check('translate.google.com' not in str(s),f'Runtime translation retained {lang}/{slug}')
        for form in s.select('form.search'):
            check(form.get('action')=='https://cnfanssp.com/search.html',f'Wrong product search destination {lang}/{slug}')
            check(form.select_one('input[name="channelid"]').get('value')=='2',f'Wrong search category {lang}/{slug}')
        for a in s.select('.product-card a[href], .route[href]'):
            check(urlsplit(a['href']).netloc=='cnfanssp.com',f'Wrong commercial destination {lang}/{slug}')
        for img in s.select('.product-card img[src]'):
            check(urlsplit(img['src']).netloc=='cnfanssp.com',f'Wrong product image host {lang}/{slug}')
        if slug!='404':
            c=s.select('link[rel="canonical"]');check(len(c)==1 and c[0].get('href')==ORIGIN+path(lang,slug),f'Canonical {lang}/{slug}')
            links={a['hreflang']:a['href'] for a in s.select('link[hreflang]')}
            expected={code:ORIGIN+path(code,slug) for code in LANGS};expected['x-default']=ORIGIN+path('en',slug)
            check(links==expected,f'Hreflang {lang}/{slug}')
            check('noindex' not in s.select_one('meta[name="robots"]')['content'],f'Unintended noindex {lang}/{slug}')
        else:check('noindex' in s.select_one('meta[name="robots"]')['content'],f'404 indexable {lang}')
        switch={a['hreflang']:a['href'] for a in s.select('[data-language-links] a')}
        check(switch=={code:path(code,slug) for code in LANGS},f'Wrong page language switch {lang}/{slug}')
        ids=[x['id'] for x in s.select('[id]')]
        check(len(ids)==len(set(ids)),f'Duplicate IDs {lang}/{slug}')
        for script in s.select('script[type="application/ld+json"]'):
            try:ld=json.loads(script.string)
            except Exception:errors.append(f'Invalid schema {lang}/{slug}');continue
            page=next(x for x in ld['@graph'] if x.get('@id')==ORIGIN+path(lang,slug)+'#page')
            check(page['inLanguage']==lang,f'Schema language {lang}/{slug}')
            check(page['name']==s.title.get_text(strip=True),f'Schema title {lang}/{slug}')
        source=BeautifulSoup((S/'en'/(slug+'.html')).read_text(),'html.parser')
        for tag in ['p','h1','h2','h3','li','table','th','td','form','img']:
            check(len(s.find_all(tag))==len(source.find_all(tag)),f'Incomplete {tag} body {lang}/{slug}')
        if slug in ARTICLES and lang!='en':
            en=source.find('article').get_text(' ',strip=True);body=s.find('article').get_text(' ',strip=True)
            check(body!=en,f'English article {lang}/{slug}')
            # Character floor catches accidental summaries, while allowing Chinese compression.
            floor=.22 if lang=='zh-CN' else .70
            check(len(body)>len(en)*floor,f'Truncated body {lang}/{slug}')

for route,s in docs.items():
    for a in s.select('a[href]'):
        u=urlsplit(a['href'])
        if u.scheme or u.netloc:continue
        if not u.path and u.fragment:
            check(s.find(id=u.fragment) is not None,f'Broken fragment {route} -> #{u.fragment}');continue
        if not u.path.startswith('/'):continue
        if u.path.startswith('/assets/') or u.path in ['/sitemap.xml','/sitemap.txt']:
            check((B/u.path.lstrip('/')).exists(),f'Missing asset {a["href"]}');continue
        check(u.path in docs,f'Broken internal link {route} -> {a["href"]}')
        if u.fragment and u.path in docs:check(docs[u.path].find(id=u.fragment) is not None,f'Broken fragment {route} -> {a["href"]}')

tree=ET.parse(B/'sitemap.xml');ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
urls=[n.find('s:loc',ns).text for n in tree.getroot()]
expected={ORIGIN+path(lang,slug) for lang in LANGS for slug in SLUGS if slug!='404'}
check(len(urls)==len(set(urls)) and set(urls)==expected,'Sitemap inventory mismatch')
for node in tree.getroot():check(len(node.findall('x:link',ns))==10,'Sitemap hreflang missing')
for lang in LANGS:
    hub=docs.get(path(lang,'articles'))
    if hub:
        links={a['href'] for a in hub.select('main a[href]')}
        check({path(lang,n) for n in ARTICLES}<=links,f'Article hub incomplete {lang}')
    home=docs.get(path(lang,'index'))
    if home:check(len(home.select('.latest-grid .guide-card'))==4,f'Homepage latest four {lang}')

if errors:
    print('\n'.join(errors[:100]));raise SystemExit(f'FAILED: {len(errors)} errors / {checks} checks')
print(f'PASS: {checks} checks; {len(docs)} complete HTML pages; {len(urls)} sitemap URLs; {len(ARTICLES)} articles in {len(LANGS)} languages')
