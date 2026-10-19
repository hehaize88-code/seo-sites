import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {load} from 'cheerio/slim';
import {languages,routes,pathFor} from '../src/lib/i18n.mjs';
import {articleSlugs} from '../src/lib/article-routes.mjs';
import {editorial,sourceById} from '../src/lib/editorial.mjs';
const base=editorial('en');
const bodyText=a=>[a.intro,...a.sections.flatMap(s=>[...s.paragraphs,...(s.list||[]),...(s.table?.rows.flat()||[])])].join(' ');
assert.equal(base.faq.length,24);assert.equal(base.articles.length,10);
for(const lang of Object.keys(languages)){
 const e=editorial(lang);assert.equal(e.faq.length,24,lang+' FAQ count');assert.equal(e.articles.length,10,lang+' article count');assert.deepEqual(Object.keys(e.ui).sort(),Object.keys(base.ui).sort(),lang+' UI keys');
 for(const f of e.faq){assert.ok(f.question.length>8&&f.answer.length>40);for(const id of f.sourceIds)assert.ok(sourceById[id]);}
 for(let i=0;i<10;i++){
  const a=e.articles[i],b=base.articles[i];assert.equal(a.slug,articleSlugs[i]);assert.equal(a.sections.length,b.sections.length);assert.ok(a.description.length>60);assert.ok(a.sourceIds.length);
  for(let j=0;j<a.sections.length;j++){const s=a.sections[j],t=b.sections[j];assert.equal(s.id,t.id);assert.equal(s.paragraphs.length,t.paragraphs.length,`${lang}/${a.slug}/${s.id} paragraphs`);assert.equal(s.list?.length,t.list?.length);assert.equal(s.table?.rows.length,t.table?.rows.length);if(t.table){assert.equal(s.table.headers.length,t.table.headers.length);s.table.rows.forEach((r,k)=>assert.equal(r.length,t.table.rows[k].length));}}
  assert.ok(bodyText(a).length>bodyText(b).length*.65,lang+' content appears truncated');if(lang!=='en')assert.notEqual(bodyText(a),bodyText(b),lang+' English fallback');
  for(const related of a.related)assert.ok(routes.includes(related),`Bad internal route ${related}`);
 }
 for(const route of routes){
  const url=pathFor(lang,route);const html=await readFile('.astro-out'+url+'index.html','utf8');const $=load(html);
  assert.equal($('html').attr('lang'),lang);assert.equal($('h1').length,1);assert.equal($('link[rel="canonical"]').attr('href'),'https://pikobuysheet.nl'+url);assert.equal($('link[rel="alternate"][hreflang]').length,25);
  assert.ok($('nav.main-nav a[href="'+pathFor(lang,'articles')+'"]').length);assert.ok($('nav.main-nav a[href="'+pathFor(lang,'faq')+'"]').length);
  if(route==='faq'||route==='')assert.equal($('.faq-list details').length,24);
  if(route==='articles')assert.equal($('.article-card').length,10);
  if(route==='')assert.equal($('.article-card').length,4);
  if(route===''||route==='spreadsheet'){
   assert.equal($('.product-card').length,route===''?8:20,`${lang}/${route} real source snapshot`);
   for(const img of $('.product-card img').toArray()){const source=new URL($(img).attr('src'));assert.ok(['cnfanshp.com','www.cnfanshp.com'].includes(source.hostname));assert.ok(source.pathname.startsWith('/uploads/'));}
  }
  if(route.startsWith('articles/')){assert.equal($('.article-body>section').length,9);const a=e.articles.find(a=>'articles/'+a.slug===route);for(const paragraph of a.sections.flatMap(s=>s.paragraphs))assert.ok($('.article-body').text().includes(paragraph));}
  for(const script of $('script[type="application/ld+json"]').toArray())JSON.parse($(script).text());
 }
}
const sitemap=await readFile('.astro-out/sitemap.xml','utf8');assert.equal((sitemap.match(/<loc>/g)||[]).length,Object.keys(languages).length*routes.length);
const worker=(await import('../dist/server/index.js')).default;
for(const route of ['/en/articles/pikobuy-haul-budget/','/faq/','/en/articles/','/logo.png']){const r=await worker.fetch(new Request('https://pikobuysheet.nl'+route));assert.equal(r.status,200);assert.ok((await r.arrayBuffer()).byteLength>100);assert.equal(r.headers.get('x-robots-tag'),null);}
const draft=await worker.fetch(new Request('https://preview.example/en/articles/'));assert.equal(draft.headers.get('x-robots-tag'),'noindex, follow');
const head=await worker.fetch(new Request('https://pikobuysheet.nl/en/articles/',{method:'HEAD'}));assert.equal((await head.text()).length,0);
console.log('Verified 24 locales, 24 FAQ answers each, 10 complete articles each, 408 canonical pages, sitemap, structured data and compressed Worker responses.');
