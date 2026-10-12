"""Structural validation of published routes, metadata and language equivalence."""
from pathlib import Path
from lxml import html, etree
from urllib.parse import urlsplit
import json,re
ROOT=Path(__file__).resolve().parents[2]/'hipobuys-store'
meta=json.loads((Path(__file__).parent/'routes.json').read_text())
pages=set(meta['pages']);articles=set(meta['article_urls']);docs={}
def file(path):return ROOT/('index.html' if path=='/' else path.strip('/')+'/index.html' if path.endswith('/') else path[1:]+'.html')
for path in pages:
    text=file(path).read_text();d=html.fromstring(text);docs[path]=d
    assert len(d.xpath('//h1'))==1,path+' H1'
    assert d.xpath('//link[@rel="canonical"]/@href')==['https://hipobuys.store'+path],path+' canonical'
    assert len(d.xpath('//title'))==1 and d.xpath('string(//title)').strip(),path+' title'
    assert d.xpath('//meta[@name="description"]/@content'),path+' description'
    tracking_scripts=''.join((s.get('src') or '')+(s.text or '') for s in d.xpath('//script'))
    assert tracking_scripts.count('G-N31DJZNW37')==2,path+' GA tag must initialize once'
    for script in d.xpath('//script[@type="application/ld+json"]'):json.loads(script.text)
    for a in d.xpath('//a[@href] | //form[@action]'):
        raw=a.get('href') or a.get('action');u=urlsplit(raw)
        assert u.hostname not in ['cnfanssp.com','www.cnfanssp.com'],path+' old conversion domain'
        if u.hostname=='hipobuys.store' or raw.startswith('/') and not raw.startswith('//'):
            p=u.path
            if p.endswith('.html'):p=p[:-5]
            if p and p not in ['/en/']:
                assert p in pages or (ROOT/p.lstrip('/')).is_file(),(path,raw,'broken link')
        if raw.startswith('#') and len(raw)>1:assert d.xpath('//*[@id=$v]',v=raw[1:]),(path,raw,'missing anchor')
    for node in d.xpath('//script[@src] | //link[@rel="stylesheet"] | //img[@src]'):
        src=node.get('src') or node.get('href')
        if src.startswith('/'):assert (ROOT/src.lstrip('/')).is_file(),(path,src,'asset')
    if path in articles:
        assert len(d.xpath('//article//section[starts-with(@id,"s")]'))>=6,path+' full sections'
        assert len(d.xpath('//article')[0].text_content().split())>=350,path+' article content'
        assert not d.xpath('//details') and 'FAQPage' not in text,path+' unwanted FAQ'
        assert len(d.xpath('//link[@hreflang]'))==9,path+' language set'
        assert len(d.xpath('//nav[@class="languages"]/a'))==8,path+' language switch'
        assert len(d.xpath('//script[contains(@src,"/assets/site-")]'))==1,path+' tracker'
for path,d in docs.items():
    alts={x.get('hreflang'):urlsplit(x.get('href')).path for x in d.xpath('//link[@hreflang]')}
    if not alts:continue
    assert len(alts)==9 and alts['x-default']==alts['en'],path+' alternates'
    assert alts[d.get('lang')]==path,path+' self hreflang'
    for lang,p in alts.items():
        assert p in docs,(path,p,'hreflang target')
        back={x.get('hreflang'):urlsplit(x.get('href')).path for x in docs[p].xpath('//link[@hreflang]')}
        assert back==alts,(path,p,'reciprocity')
        if lang!='x-default':assert docs[p].get('lang')==lang,(p,lang,'lang')
sitemap=etree.parse(str(ROOT/'sitemap.xml'))
urls={urlsplit(x).path for x in sitemap.xpath('//*[local-name()="loc"]/text()')}
assert urls==pages,('sitemap coverage',urls^pages)
for name in ['google-sitemap.xml','sitemap-extra.xml']:assert (ROOT/name).read_bytes()==(ROOT/'sitemap.xml').read_bytes()
assert len(articles)==56
print(f'PASS: {len(pages)} routes, {len(articles)} full articles, reciprocal eight-language metadata, internal links, sitemap and analytics installation.')
