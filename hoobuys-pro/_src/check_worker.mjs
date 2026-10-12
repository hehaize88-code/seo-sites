import assert from 'node:assert/strict';
import fs from 'node:fs';
const src=fs.readFileSync(new URL('../_worker.js',import.meta.url),'utf8');
const {default:worker,canonicalPath}=await import('data:text/javascript;base64,'+Buffer.from(src).toString('base64'));
const cases={'/products.html':'/products','/products/':'/products','/products.html/':'/products','/index.html':'/','/index':'/','/languages':'/','/languages.html':'/','/de':'/de/','/de/index.html':'/de/','/de/products.html':'/de/products','/fr/guides/':'/fr/guides','/en/products.html':'/products','/hoobuy-pro-europe-parcel-ledger-w2c-qc-2026-07-14.html':'/shipping-guide'};
let hits=0;const env={ASSETS:{fetch:async request=>{hits++;assert(!new URL(request.url).pathname.endsWith('.html'));return new Response('<!doctype html><title>Fixture</title>',{headers:{'Content-Type':'text/html'}})}}};
for(const [input,expected] of Object.entries(cases)){
 assert.equal(canonicalPath(input),expected);
 const r=await worker.fetch(new Request('https://www.hoobuys.pro'+input+'?utm_source=test'),env);
 assert.equal(r.status,301);assert.equal(r.headers.get('location'),'https://hoobuys.pro'+expected+'?utm_source=test');
 const canonical=await worker.fetch(new Request(r.headers.get('location')),env);assert.equal(canonical.status,200);assert.equal(canonical.headers.get('location'),null);
}
assert.equal((await worker.fetch(new Request('https://hoobuys.pro/_src/original.json'),env)).status,404);
const missing=await worker.fetch(new Request('https://hoobuys.pro/missing'),{ASSETS:{fetch:async()=>new Response('Missing',{status:404})}});assert.equal(missing.status,404);assert.equal(missing.headers.get('X-Robots-Tag'),'noindex');
const locales=['de','es','fr','it'];for(const l of locales)assert.equal(canonicalPath('/'+l+'/hoobuy-size-guide.html'),'/'+l+'/hoobuy-size-guide');
console.log('PASS: canonical aliases, one-hop host normalization, query preservation, locale roots, assets pass-through and 404 headers.');
