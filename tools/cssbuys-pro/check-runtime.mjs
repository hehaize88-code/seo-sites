import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {parcelWeight,parcelBudget} from '../../cssbuys-pro/assets/planning-math.mjs';
const sample={actual:3,length:40,width:30,height:25,divisor:6000,increment:0.5};
assert.deepEqual(parcelWeight(sample),{volume:5,basis:5,billed:5});
assert.equal(parcelWeight({...sample,actual:5.01}).billed,5.5);
assert.equal(parcelWeight({...sample,rule:'actual'}).billed,3);
assert.equal(parcelWeight({...sample,divisor:5000}).billed,6);
for(const bad of [0,-1,Infinity,NaN])assert.throws(()=>parcelWeight({...sample,divisor:bad}),RangeError);
assert.equal(parcelBudget([100,10,5,2,3,80,0,20]),180);
assert.equal(parcelBudget([0.1,0.2,0,0,0,0,0,0]),0.3);
assert.throws(()=>parcelBudget([1,0,0,0,0,0,0,2]),/credit/);
assert.throws(()=>parcelBudget([1,0,0,0,0,0,0,-1]),/invalid/);
const code=await fs.readFile(new URL('../../cssbuys-pro/_worker.js',import.meta.url),'utf8');
const worker=(await import('data:text/javascript;base64,'+Buffer.from(code).toString('base64'))).default;
const cache=new Map();globalThis.caches={default:{async match(r){return cache.get(r.url)?.clone()},async put(r,v){cache.set(r.url,v)}}};
let fetches=0;const pending=[];
const ctx={waitUntil(p){pending.push(p)}};
const env={ASSETS:{async fetch(r){fetches++;return new Response(r.url.includes('missing')?'Missing':'<html>static</html>',{status:r.url.includes('missing')?404:200,headers:{'content-type':'text/html'}})}}};
for(const [input,want]of [
  ['http://www.cssbuys.pro/de/guides.html?src=x','https://cssbuys.pro/de/guides/?src=x'],
  ['https://cssbuys.pro/it','https://cssbuys.pro/it/'],
  ['https://cssbuys.pro/fr/guides/test.html','https://cssbuys.pro/fr/guides/test'],
  ['https://cssbuys.pro/index.html','https://cssbuys.pro/']]){
  const r=await worker.fetch(new Request(input),env,ctx);assert.equal(r.status,308);assert.equal(r.headers.get('location'),want);
}
let r=await worker.fetch(new Request('https://cssbuys.pro/sitemap.xml'),env,ctx);
assert.match(r.headers.get('content-type'),/application\/xml/);await Promise.all(pending);
await worker.fetch(new Request('https://cssbuys.pro/sitemap.xml'),env,ctx);assert.equal(fetches,1);
r=await worker.fetch(new Request('https://cssbuys.pro/missing'),env,ctx);assert.equal(r.status,404);assert.equal(r.headers.get('cache-control'),'no-store');
assert.equal(await (await worker.fetch(new Request('https://cssbuys.pro/'),env,ctx)).text(),'<html>static</html>');
console.log('PASS: calculator boundaries, currency sums, canonical redirects, MIME, caching, 404 and no duplicate tracker injection.');
