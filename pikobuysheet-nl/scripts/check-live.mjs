import assert from 'node:assert/strict';
import {load} from 'cheerio/slim';
import {languages,pathFor,routes} from '../src/lib/i18n.mjs';
import {editorial} from '../src/lib/editorial.mjs';
import {landingCategories} from '../src/lib/catalog-routes.mjs';

const origin='https://pikobuysheet.nl';
const headers={'User-Agent':'PikobuySheet-Release-Verification/1.0'};
async function read(path){
  const response=await fetch(origin+path,{headers,signal:AbortSignal.timeout(20000)});
  assert.equal(response.status,200,path+' HTTP status');
  assert.equal(response.headers.get('x-robots-tag'),null,path+' must be indexable');
  return response.text();
}
const queue=Object.keys(languages).flatMap(lang=>[
  ...editorial(lang).articles.slice(-3).map(a=>({lang,route:'articles/'+a.slug,expectedTitle:a.title})),
  ...landingCategories.map(key=>({lang,route:'spreadsheet/'+key,expectedTitle:editorial(lang).growth.categories[key].title})),
  ...['qc','shipping'].map(key=>({lang,route:key,expectedTitle:editorial(lang).growth.hubs[key].title}))
]);
let completed=0;
async function checkPages(){
  while(queue.length){
    const {lang,route,expectedTitle}=queue.shift(),path=pathFor(lang,route);
    const $=load(await read(path));
    assert.equal($('html').attr('lang'),lang,path);
    assert.equal($('title').text(),expectedTitle,path+' title');
    assert.equal($('h1').length,1,path+' heading');
    assert.equal($('link[rel="canonical"]').attr('href'),origin+path,path+' canonical');
    assert.equal($('link[hreflang]').length,25,path+' language alternatives');
    if(route.startsWith('spreadsheet/'))assert.equal($('.product-card').length,20,path+' server-rendered products');
    if(route.startsWith('articles/'))assert.equal($('.article-body>section').length,11,path+' complete article');
    if(++completed%24===0)console.log(`Verified ${completed} published pages`);
  }
}
await Promise.all([checkPages(),checkPages(),checkPages()]);
const sitemap=await read('/sitemap.xml');
assert.equal((sitemap.match(/<loc>/g)||[]).length,24*routes.length);
for(const category of landingCategories){
  const response=await fetch(origin+'/api/catalog/?category='+category,{headers,signal:AbortSignal.timeout(20000)});
  assert.equal(response.status,200,'live catalog API '+category);
  const data=await response.json();assert.equal(data.category,category);assert.equal(data.products.length,20);
}
const productResponse=await fetch(origin+'/api/product/?id=6045',{headers,signal:AbortSignal.timeout(20000)});
assert.equal(productResponse.status,200,'live product API');
const product=await productResponse.json();assert.notEqual(product.id,product.productId);
assert.equal(new URL(new URL(product.buyUrl).searchParams.get('productUrl')).searchParams.get('itemID'),product.productId);
console.log(`PASS: ${completed} live translated article/category/hub pages, ${24*routes.length} sitemap URLs, live category APIs and the real purchase ID.`);
