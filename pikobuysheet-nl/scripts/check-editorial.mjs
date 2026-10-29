import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {load} from 'cheerio/slim';
import {languages,routes,pathFor} from '../src/lib/i18n.mjs';
import {landingCategories} from '../src/lib/catalog-routes.mjs';
import {articleSlugs} from '../src/lib/article-routes.mjs';
import {editorial,sourceById} from '../src/lib/editorial.mjs';
const worker=(await import('../dist/server/index.js')).default;
const base=editorial('en');
const bodyText=a=>[a.intro,...a.sections.flatMap(s=>[...s.paragraphs,...(s.list||[]),...(s.table?.rows.flat()||[])])].join(' ');
assert.equal(base.faq.length,24);assert.equal(base.articles.length,13);
for(const lang of Object.keys(languages)){
 const e=editorial(lang);assert.equal(e.faq.length,24,lang+' FAQ count');assert.equal(e.articles.length,13,lang+' article count');assert.deepEqual(Object.keys(e.ui).sort(),Object.keys(base.ui).sort(),lang+' UI keys');
 for(const f of e.faq){assert.ok(f.question.length>8&&f.answer.length>40);for(const id of f.sourceIds)assert.ok(sourceById[id]);}
 for(let i=0;i<articleSlugs.length;i++){
  const a=e.articles[i],b=base.articles[i];assert.equal(a.slug,articleSlugs[i]);assert.equal(a.sections.length,b.sections.length);assert.ok(a.description.length>60);assert.ok(a.sourceIds.length);
  for(let j=0;j<a.sections.length;j++){const s=a.sections[j],t=b.sections[j];assert.equal(s.id,t.id);assert.equal(s.paragraphs.length,t.paragraphs.length,`${lang}/${a.slug}/${s.id} paragraphs`);assert.equal(s.list?.length,t.list?.length);assert.equal(s.table?.rows.length,t.table?.rows.length);if(t.table){assert.equal(s.table.headers.length,t.table.headers.length);s.table.rows.forEach((r,k)=>assert.equal(r.length,t.table.rows[k].length));}}
  if(i>=10&&lang!=='en'){
   assert.notEqual(a.intro,b.intro,`${lang}/${a.slug}: English intro`);
   a.sections.forEach((section,j)=>section.paragraphs.forEach((paragraph,k)=>{assert.notEqual(paragraph,b.sections[j].paragraphs[k],`${lang}/${a.slug}/${section.id}: English paragraph`);assert.ok(paragraph.length>b.sections[j].paragraphs[k].length*.55,`${lang}/${a.slug}/${section.id}: abbreviated paragraph`);}));
  }
  for(const id of a.sourceIds)assert.ok(sourceById[id],`${lang}/${a.slug}: missing source`);
  assert.ok(bodyText(a).length>bodyText(b).length*.65,lang+' content appears truncated');if(lang!=='en')assert.notEqual(bodyText(a),bodyText(b),lang+' English fallback');
  for(const related of a.related)assert.ok(routes.includes(related),`Bad internal route ${related}`);
 }
 assert.deepEqual(Object.keys(e.growth).sort(),Object.keys(base.growth).sort(),lang+' growth keys');
 for(const key of landingCategories){const copy=e.growth.categories[key];assert.ok(copy.intro.length>180);assert.equal(copy.checks.length,3);if(lang!=='en')assert.notEqual(copy.intro,base.growth.categories[key].intro);}
 for(const key of ['qc','shipping']){assert.equal(e.growth.hubs[key].sections.length,4);for(let i=0;i<4;i++){const a=e.growth.hubs[key].sections[i],b=base.growth.hubs[key].sections[i];assert.equal(a.id,b.id);assert.equal(a.paragraphs.length,b.paragraphs.length);if(lang!=='en')assert.notEqual(a.paragraphs.join(),b.paragraphs.join());}}
 for(const route of routes){
  const url=pathFor(lang,route);const html=await readFile('.astro-out'+url+'index.html','utf8');const $=load(html);
  assert.equal(await (await worker.fetch(new Request('https://pikobuysheet.nl'+url))).text(),html,url+' compressed Worker must reproduce exact HTML');
  assert.equal($('html').attr('lang'),lang);assert.equal($('h1').length,1);assert.equal($('link[rel="canonical"]').attr('href'),'https://pikobuysheet.nl'+url);assert.equal($('link[rel="alternate"][hreflang]').length,25);
  assert.ok($('nav.main-nav a[href="'+pathFor(lang,'articles')+'"]').length);assert.ok($('nav.main-nav a[href="'+pathFor(lang,'faq')+'"]').length);
  if(route==='faq'||route==='')assert.equal($('.faq-list details').length,24);
  if(route==='articles')assert.equal($('.article-card').length,13);
  if(route==='')assert.equal($('.article-card').length,4);
  if(route===''||route==='spreadsheet'||route.startsWith('spreadsheet/')){
   assert.equal($('.product-card').length,route===''?8:20,`${lang}/${route} real source snapshot`);
   for(const img of $('.product-card img').toArray()){const source=new URL($(img).attr('src'));assert.ok(['cnfanshp.com','www.cnfanshp.com'].includes(source.hostname));assert.ok(source.pathname.startsWith('/uploads/'));}
  }
  assert.ok($('meta[name="description"]').attr('content').length>20);
  if(route.startsWith('articles/')){const a=e.articles.find(a=>'articles/'+a.slug===route);assert.equal($('.article-body>section').length,a.sections.length+2);for(const paragraph of a.sections.flatMap(s=>s.paragraphs))assert.ok($('.article-body').text().includes(paragraph));}
  for(const a of $('a[href^="/"]').toArray()){const href=$(a).attr('href').split(/[?#]/)[0];if(href.endsWith('/'))assert.ok(Object.keys(languages).some(l=>routes.some(r=>pathFor(l,r)===href)),`Broken internal route ${lang}/${route}: ${href}`);}
  if(route.startsWith('spreadsheet/')){const key=route.split('/')[1];assert.equal($('.category-list a.selected').attr('data-category'),key);assert.ok($('.catalog-guidance').text().includes(e.growth.categories[key].intro));}
  if(['qc','shipping'].includes(route))assert.equal($('.guide-content>section').length,5);
  for(const script of $('script[type="application/ld+json"]').toArray())JSON.parse($(script).text());
 }
}
const sitemap=await readFile('.astro-out/sitemap.xml','utf8');assert.equal((sitemap.match(/<loc>/g)||[]).length,Object.keys(languages).length*routes.length);
for(const route of ['/en/articles/pikobuy-haul-budget/','/faq/','/en/articles/','/en/articles/pikobuy-shipping-calculator/','/de/spreadsheet/shoes/','/logo.png']){const r=await worker.fetch(new Request('https://pikobuysheet.nl'+route));assert.equal(r.status,200);assert.ok((await r.arrayBuffer()).byteLength>100);assert.equal(r.headers.get('x-robots-tag'),null);}
const draft=await worker.fetch(new Request('https://preview.example/en/articles/'));assert.equal(draft.headers.get('x-robots-tag'),'noindex, follow');
const head=await worker.fetch(new Request('https://pikobuysheet.nl/en/articles/',{method:'HEAD'}));assert.equal((await head.text()).length,0);
for(const query of ['?page=2','?q=shoes','?category=jackets']){const r=await worker.fetch(new Request('https://pikobuysheet.nl/en/spreadsheet/'+query));assert.equal(r.headers.get('x-robots-tag'),'noindex, follow');}
for(const host of ['http://pikobuysheet.nl','https://www.pikobuysheet.nl']){const r=await worker.fetch(new Request(host+'/de/spreadsheet/shoes/?page=2'));assert.equal(r.status,301);assert.equal(r.headers.get('location'),'https://pikobuysheet.nl/de/spreadsheet/shoes/?page=2');}
assert.equal((await worker.fetch(new Request('https://pikobuysheet.nl/en/articles/missing/'))).status,404);
assert.equal((sitemap.match(/hreflang="x-default"/g)||[]).length,Object.keys(languages).length*routes.length);
for(const a of base.articles.slice(-3)){const count=bodyText(a).split(/\s+/).length;assert.ok(count>=1200&&count<=1800,a.slug+' English word count: '+count);}
console.log(`Verified 24 locales, 24 FAQ answers each, ${articleSlugs.length} complete articles each, ${24*routes.length} canonical pages, category snapshots, internal links, sitemap, schema, redirects and Worker indexation headers.`);
