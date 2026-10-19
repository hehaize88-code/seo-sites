import assert from 'node:assert/strict';
import{getCatalog,getProduct,apiResponse}from'../src/lib/source.mjs';
import{languages,routes,pathFor,t}from'../src/lib/i18n.mjs';import{content}from'../src/lib/content.mjs';
for(const l of Object.keys(languages)){assert.equal(t(l).categoryLabels.length,12);assert.equal(content[l].length,5);for(const r of routes)assert.ok(pathFor(l,r).endsWith('/'));}
const first=await getCatalog(),second=await getCatalog({page:2});assert.equal(first.products.length,20);assert.equal(second.products.length,20);assert.ok(!first.products.some(a=>second.products.some(b=>a.id===b.id)));
const a=await getCatalog({q:'shoes',sort:'price-asc'}),b=await getCatalog({q:'shoes',sort:'price-asc',page:2});const list=[...a.products,...b.products];assert.ok(!list.some(p=>['519','520'].includes(p.id)),'Regression: unrelated socks/poker entries must not leak from the upstream global sort');assert.ok(list.every((p,i)=>!i||list[i-1].price<=p.price));
const last=await getCatalog({q:'shoes',page:Math.ceil(a.total/20)});assert.equal(last.hasNext,false);
const p=await getProduct('6045');assert.notEqual(p.id,p.productId);assert.equal(new URL(new URL(p.buyUrl).searchParams.get('productUrl')).searchParams.get('itemID'),p.productId);assert.ok(p.images.every(x=>new URL(x).hostname.endsWith('cnfanshp.com')));
const invalid=await apiResponse(new URL('https://pikobuysheet.nl/api/product/?id=../bad'));assert.equal(invalid.status,400);
console.log('PASS: 24 locales; pagination; complete matching-result price sort; last-page handling; real purchase ID; invalid-ID rejection.');
