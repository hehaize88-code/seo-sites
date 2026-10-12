import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
const code = await readFile(new URL('../_worker.js', import.meta.url), 'utf8');
const {default: worker} = await import('data:text/javascript;base64,' + Buffer.from(code).toString('base64'));
let fetched;
const env = {ASSETS: {fetch: async (request) => {
  fetched = request.url;
  const status = new URL(request.url).pathname.endsWith('/missing') ? 404 : 200;
  return new Response('<!doctype html><h1>Fixture</h1>', {status, headers: {'Content-Type':'text/html'}});
}}};
const cases = [
  ['https://www.hoobuys.net/index.html','https://hoobuys.net/'],
  ['http://hoobuys.net/shipping-guide.html?x=1','https://hoobuys.net/shipping-guide?x=1'],
  ['https://hoobuys.net/de','https://hoobuys.net/de/'],
  ['https://hoobuys.net/de/index.html','https://hoobuys.net/de/'],
  ['https://hoobuys.net/zh-CN/shipping-guide.html','https://hoobuys.net/zh-cn/shipping-guide'],
  ['https://hoobuys.net/fr/shipping-guide/','https://hoobuys.net/fr/shipping-guide'],
  ['https://hoobuys.net/hoobuy-net-shipping-cost-parcel-route-2026?x=1','https://hoobuys.net/shipping-guide?x=1'],
  ['https://hoobuys.net/pl/hoobuy-net-shipping-cost-parcel-route-2026','https://hoobuys.net/pl/shipping-guide'],
  ['https://hoobuys.net/hoobuy-qc-request-sheet-w2c-shipping-decision-2026-07-16','https://hoobuys.net/hoobuy-order-status-purchase-dispatch-qc-storage-2026#qc-and-storage'],
];
for (const [from,to] of cases) {
  fetched=null;
  const r=await worker.fetch(new Request(from),env);
  assert.equal(r.status,301,from);assert.equal(r.headers.get('location'),to,from);assert.equal(fetched,null);
  const next=await worker.fetch(new Request(to),env);
  assert.equal(next.status,200,'Redirect loop: '+to);
}
for (const path of ['/', '/de/', '/fr/shipping-guide', '/zh-cn/hoobuy-process-pending-guide']) {
  const r=await worker.fetch(new Request('https://hoobuys.net'+path),env);
  assert.equal(r.status,200);assert.equal(fetched,'https://hoobuys.net'+path);
  assert.equal(r.headers.get('link'),`<https://hoobuys.net${path}>; rel="canonical"`);
  assert.equal(r.headers.get('x-hoobuys-release'),'multilingual-guides-20261012-logo-v2');
}
for (const path of ['/_src/en/index.html','/%5fsrc/catalog.json','/.git/config']) {
  fetched=null;const r=await worker.fetch(new Request('https://hoobuys.net'+path),env);
  assert.equal(r.status,404);assert.equal(fetched,null);
}
const missing=await worker.fetch(new Request('https://hoobuys.net/missing'),env);
assert.equal(missing.status,404);assert.equal(missing.headers.get('link'),null);assert.equal(missing.headers.get('cache-control'),'no-store');
const frenchMissing=await worker.fetch(new Request('https://hoobuys.net/fr/missing'),env);
assert.equal(frenchMissing.status,404);assert.equal(fetched,'https://hoobuys.net/fr/404');assert.equal(frenchMissing.headers.get('link'),null);
console.log('PASS: canonical redirects, language roots, legacy paths, source protection and 404 handling');
