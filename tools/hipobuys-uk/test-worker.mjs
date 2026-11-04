import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
const code=await readFile(new URL('../../hipobuys-uk/_worker.js',import.meta.url),'utf8');
const {default:worker}=await import('data:text/javascript;base64,'+Buffer.from(code).toString('base64'));
const env={ASSETS:{fetch:async r=>new Response(new URL(r.url).pathname,{status:new URL(r.url).pathname==='/missing-test'?404:200,headers:{'Content-Type':new URL(r.url).pathname==='/sitemap.xml'?'application/xml':'text/html'}})}};
const cases=[
 ['/uk-hipobuy-fees-guide-2026.html','/en/hipobuy-fees/'],
 ['/uk-hipobuy-shipping-estimate-guide.html','/en/shipping-from-china/'],
 ['/uk-qc-photos-before-shipping.html','/qc-checklist-uk-buyers'],
 ['/uk-shipping-guide.html','/hipobuy-uk-shipping-line-selection'],
 ['/uk-w2c-links-product-route-guide.html','/en/w2c-links/'],
 ['/w2c-links-guide.html','/en/w2c-links/'],
 ['/en/articles/','/guides'],
 ['/fr/articles/hipobuy-links-not-working/index.html','/fr/articles/hipobuy-links-not-working/'],
 ['/index.html','/'],
];
for(const [from,to] of cases){const r=await worker.fetch(new Request('https://hipobuys.uk'+from+'?utm_source=test'),env);assert.equal(r.status,301,from);assert.equal(r.headers.get('location'),'https://hipobuys.uk'+to+'?utm_source=test');}
for(const p of ['/de/','/de/hipobuy-kosten/','/de/hipobuy-gutschein/','/de/qc-fotos/','/de/w2c-links/','/de/versand-aus-china/']){const r=await worker.fetch(new Request('https://hipobuys.uk'+p),env);assert.equal(r.status,301);assert.equal(r.headers.get('location'),'https://hipobuys.de'+p);}
for(const p of ['/de/uk/','/de/hipobuy-uk-fees/','/de/articles/hipobuy-links-not-working/']){const r=await worker.fetch(new Request('https://hipobuys.uk'+p),env);assert.equal(r.status,200);assert.ok(r.headers.has('Content-Security-Policy'));}
const www=await worker.fetch(new Request('http://www.hipobuys.uk/uk-shipping-guide.html'),env);assert.equal(www.headers.get('location'),'https://hipobuys.uk/hipobuy-uk-shipping-line-selection');
const xml=await worker.fetch(new Request('https://hipobuys.uk/sitemap.xml'),env);assert.equal(xml.headers.get('Content-Type'),'application/xml');
assert.equal((await worker.fetch(new Request('https://hipobuys.uk/missing-test'),env)).status,404);
console.log('21 redirect, German routing, security header and response checks passed');
