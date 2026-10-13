#!/usr/bin/env python3
"""Independent output audit: links, language reciprocity, schema and sitemap coverage."""
import csv
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2] / 'hoobuys-shop'
HOST = 'https://hoobuys.shop'
LANGS = {'en','zh-CN','de','fr','es','it','pl','nl','pt'}

class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.tags=[]; self.schemas=[]; self.json=False; self.buffer=''
        self.feed(source)
    def handle_starttag(self, tag, pairs):
        attrs=dict(pairs); self.tags.append((tag,attrs))
        if tag=='script' and attrs.get('type')=='application/ld+json':
            self.json=True;self.buffer=''
    def handle_endtag(self,tag):
        if tag=='script' and self.json:
            self.schemas.append(json.loads(self.buffer));self.json=False
    def handle_data(self,data):
        if self.json:self.buffer+=data
    def attrs(self,tag):return [a for t,a in self.tags if t==tag]

def route(file):
    value='/'+file.relative_to(ROOT).as_posix()[:-5]
    return value[:-5] if value.endswith('/index') else value

def main():
    pages={route(p):Page(p.read_text()) for p in ROOT.rglob('*.html')}
    generated={r:p for r,p in pages.items() if p.attrs('html')[0].get('data-static-locale')=='true'}
    errors=[];articles=0
    for current,p in generated.items():
        prefix=current+': '
        lang=p.attrs('html')[0].get('lang')
        if lang not in LANGS:errors.append(prefix+'invalid language')
        canonical=[a.get('href') for a in p.attrs('link') if a.get('rel')=='canonical']
        if canonical != [HOST+current]:errors.append(prefix+'non-self canonical')
        alternates={a.get('hreflang'):a.get('href') for a in p.attrs('link') if a.get('rel')=='alternate'}
        if set(alternates)!=LANGS|{'x-default'}:errors.append(prefix+'incomplete alternates')
        if len(p.attrs('h1'))!=1:errors.append(prefix+'requires one h1')
        if not any(a.get('name')=='description' and a.get('content') for a in p.attrs('meta')):errors.append(prefix+'missing description')
        for code,target in alternates.items():
            other=pages.get(urlparse(target).path)
            if not other:errors.append(prefix+'missing language target '+target);continue
            if code!='x-default' and other.attrs('html')[0].get('lang')!=code:errors.append(prefix+'language mismatch')
            back={a.get('hreflang'):a.get('href') for a in other.attrs('link') if a.get('rel')=='alternate'}
            if back.get(lang)!=HOST+current:errors.append(prefix+'nonreciprocal hreflang')
        for schema in p.schemas:
            if schema.get('@type')=='Article':
                articles+=1
                if schema.get('inLanguage')!=lang or schema.get('url')!=HOST+current:errors.append(prefix+'schema mismatch')
                if any(x.get('@type')=='FAQPage' for x in p.schemas):errors.append(prefix+'article has FAQ schema')
                sections=[a for a in p.attrs('details') if a.get('class')=='reading-section']
                if len(sections)!=5 or any('open' not in s for s in sections):errors.append(prefix+'primary sections unavailable without JS')
            if schema.get('@type')=='CollectionPage':
                listing=schema['mainEntity'];items=listing['itemListElement']
                if listing['numberOfItems']!=len(items):errors.append(prefix+'wrong catalogue count')
                if [x['position'] for x in items]!=list(range(1,len(items)+1)):errors.append(prefix+'wrong catalogue positions')
        for tag,attrs in p.tags:
            key='href' if tag in {'a','link'} else 'src' if tag in {'img','script'} else None
            address=attrs.get(key,'') if key else ''
            if not address:continue
            parsed=urlparse(address)
            if parsed.netloc and parsed.netloc!='hoobuys.shop':continue
            target=unquote(parsed.path)
            if not target:target=current
            if target.startswith('/assets/'):
                if not (ROOT/target.lstrip('/')).is_file():errors.append(prefix+'missing asset '+target)
            elif target not in pages and target.removesuffix('.html') not in pages:
                errors.append(prefix+'missing internal link '+target)
            if parsed.fragment and target in pages:
                ids={a.get('id') for _,a in pages[target].tags}
                if parsed.fragment not in ids:errors.append(prefix+'missing anchor '+address)
    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
    sitemap=ET.parse(ROOT/'sitemap.xml').getroot()
    xml_urls=[x.find('s:loc',ns).text for x in sitemap]
    expected={HOST+r for r in pages if r!='/404'}
    if set(xml_urls)!=expected or len(xml_urls)!=len(expected):errors.append('XML sitemap incomplete or duplicated')
    if set((ROOT/'sitemap.txt').read_text().splitlines())!=expected:errors.append('TXT sitemap coverage differs')
    for node in sitemap:
        loc=node.find('s:loc',ns).text
        if urlparse(loc).path in generated and len(node.findall('x:link',ns))!=10:errors.append(loc+' sitemap language links incomplete')
    for lang in LANGS:
        file=ROOT/'assets'/f'hoobuy-tracker-{lang.lower()}.csv'
        rows=list(csv.reader(file.read_text(encoding='utf-8-sig').splitlines()))
        if len(rows)!=2 or any(len(row)!=22 for row in rows):errors.append(str(file)+' invalid CSV')
    assert len(generated)==108 and articles==63,(len(generated),articles)
    if errors:
        print('\n'.join(errors));raise SystemExit(1)
    print(json.dumps({'passed':True,'static_pages':len(generated),'article_pages':articles,'languages':len(LANGS),'sitemap_urls':len(xml_urls),'checks':['internal links and anchors','reciprocal language URLs','canonical and schema','full HTML section content','XML/TXT coverage','localized CSV structure']}))

if __name__=='__main__':main()
