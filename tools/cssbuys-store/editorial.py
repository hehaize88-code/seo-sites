"""Reviewed multilingual copy and the first-screen content for priority guides."""
import json
from html import escape
from pathlib import Path

from bs4 import BeautifulSoup

BASE = Path(__file__).resolve().parent
UPDATED = '2026-11-05'
PARCEL = 'cssbuy-submit-parcel-checklist'
TRACKING = 'cssbuy-tracking-not-updating'
QC = 'qc-guide'
SHEET = 'cssbuy-spreadsheet'
SHIPPING = 'cssbuy-shipping-calculator-estimate'
POINTS = 'cssbuy-points-rewards-guide'
SHOES = 'cssbuy-shoe-sizing-qc-checklist'
NEW_ARTICLES = {PARCEL: 'parcel', TRACKING: 'tracking'}
REVISED = {QC, SHEET, SHIPPING, POINTS, SHOES, PARCEL, TRACKING}
COPY = json.loads((BASE / 'editorial' / 'refresh.json').read_text())


def add_reviewed_articles(meta, lang):
    additions = json.loads((BASE / 'editorial' / f'{lang}.json').read_text())
    for slug, key in NEW_ARTICLES.items():
        meta[slug] = dict(additions[key], published=UPDATED, status='new')
    for slug, key in [(QC, 'qc'), (SHEET, 'sheet'), (SHIPPING, 'ship')]:
        meta[slug].update(title=COPY[lang][key + 'Title'],
                          description=COPY[lang][key + 'Description'])


def article_body(lang, slug, meta):
    if slug not in NEW_ARTICLES:
        return BeautifulSoup((BASE / 'articles' / lang / f'{slug}.html').read_text(), 'html.parser')
    fragments = [f'<p class="dek">{escape(meta["lead"])}</p>']
    for heading, *paragraphs in meta['sections']:
        fragments.append(f'<h2>{escape(heading)}</h2>')
        fragments.extend(f'<p>{escape(p)}</p>' for p in paragraphs)
    return BeautifulSoup(''.join(fragments), 'html.parser')


def first_screen(lang, slug, body, product_rows, guide_url):
    copy = COPY[lang]
    if slug == QC:
        heading = body.find(id='decision')
        outcomes = heading.find_next_siblings('p', limit=3)
        heading.extract()
        for paragraph in outcomes:
            paragraph.extract()
        actions = ''.join(f'<li><strong>{escape(label)}</strong> {escape(action)}</li>'
                          for label, action in copy['qcOutcomes'])
        return (f'<section class="guide-answer decision" id="decision"><h2>{escape(copy["qcDecision"])}</h2>'
                f'<ul>{actions}</ul></section>')
    if slug == SHEET:
        old = body.find(id='dated-finds')
        for node in old.find_next_siblings():
            if node.name == 'h2':
                break
            node.extract()
        old.extract()
        headers = ''.join(f'<th scope="col">{escape(copy[key])}</th>'
                          for key in ('productLabel', 'priceLabel', 'qcLabel'))
        rows = []
        for (name, href, price), check in zip(product_rows, copy['checks'], strict=True):
            rows.append(f'<tr><th scope="row"><a href="{href}">{escape(name)}</a></th>'
                        f'<td>USD {escape(price)}</td><td>{escape(check)}</td></tr>')
        return (f'<section class="guide-answer" id="dated-finds"><h2>{escape(copy["sheetHeading"])}</h2>'
                f'<p>{escape(copy["priceDate"])}</p><div class="table-wrap"><table>'
                f'<thead><tr>{headers}</tr></thead><tbody>{"".join(rows)}</tbody></table></div></section>')
    if slug == SHIPPING:
        return (f'<div class="guide-answer"><a class="button" href="https://www.cssbuy.com/estimates">'
                f'{escape(copy["calcLink"])} ↗</a><p>{escape(copy["calcExample"])}</p></div>')
    if slug in (POINTS, SHOES):
        target = body.find(id='shipping' if slug == POINTS else 'measurement-example')
        link = body.new_tag('a', href=guide_url(QC))
        link.string = copy['pointLink' if slug == POINTS else 'sizeLink']
        p = body.new_tag('p')
        p.append(link)
        target.find_next_sibling('p').insert_after(p)
    if slug in NEW_ARTICLES:
        return str(body.p.extract())
    return ''


def source_links(lang, slug, buying, shipping):
    links = [('https://m.cssbuy.com/buyforme', buying)]
    if slug == PARCEL:
        links.append(('https://m.cssbuy.com/shipforme', COPY[lang]['sourceShip']))
    if slug in (QC, SHOES):
        links.append(('https://www.cssbuy.com/shop/helpCenter?id=144', COPY[lang]['sourceReturn']))
    if slug != TRACKING:
        links.append(('https://www.cssbuy.com/estimates', shipping))
    citations = ''.join(f'<li><a href="{url}" target="_blank" rel="noopener">CSSBuy · {escape(label)}</a></li>'
                   for url, label in links)

    if slug == TRACKING:
        for carrier, href in (
            ('UPS', 'https://www.ups.com/us/en/support/tracking-support/where-is-my-package/understanding-tracking-status'),
            ('USPS', 'https://faq.usps.com/articles/FAQ/Where-is-my-package'),
        ):
            citations += f'<li><a href="{href}" target="_blank" rel="noopener">{carrier}</a></li>'
    return citations
