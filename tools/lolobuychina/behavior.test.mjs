import fs from 'node:fs';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import path from 'node:path';
const root=path.resolve('lolobuychina');
const code=fs.readFileSync(path.join(root,'_worker.js'),'utf8');
const worker=(await import('data:text/javascript;base64,'+Buffer.from(code).toString('base64'))).default;
const env={ASSETS:{fetch:async request=>{
 let p=new URL(request.url).pathname;
 let f=path.join(root,p.endsWith('/')?p+'index.html':p);
 if(!fs.existsSync(f) && !path.extname(p))f+='.html';
 if(!fs.existsSync(f)||!fs.statSync(f).isFile())return new Response('Missing',{status:404});
 return new Response(request.method==='HEAD'?null:fs.readFileSync(f),{headers:{'Content-Type':f.endsWith('.html')?'text/html':f.endsWith('.xml')?'application/xml':'text/plain'}});
}}};
let checks=0;
for(const locale of ['','de','fr','es','it','pt','ja','ko','zh']){
 const pre=locale?'/'+locale:'';
 for(const [old,target] of Object.entries({'/index.html':'/','/seo-guide.html':'/articles/','/guides':'/articles/','/articles':'/articles/','/qc.html':'/qc','/articles/qc-photos-before-shipping.html':'/guides/lolobuy-qc-photo-checklist-2026','/articles/lolobuy-w2c-qc-shipping-checklist':'/guides/lolobuy-w2c-qc-shipping-2026','/guides/lolobuychina-w2c-qc-route-notes-2026-07-09.html':'/guides/lolobuy-w2c-qc-shipping-2026'})){
  const r=await worker.fetch(new Request('https://lolobuychina.com'+pre+old+'?utm_source=test'),env);
  assert.equal(r.status,301);assert.equal(r.headers.get('location'),'https://lolobuychina.com'+pre+target+'?utm_source=test');checks++;
 }
 for(const route of ['/','/articles/','/w2c','/qc','/articles/lolobuy-link-not-working','/articles/lolobuy-returns-refunds']){
  const r=await worker.fetch(new Request('https://lolobuychina.com'+pre+route),env);assert.equal(r.status,200);assert.equal(r.headers.get('content-language'),locale||'en');checks++;
 }
 const missing=await worker.fetch(new Request('https://lolobuychina.com'+pre+'/not-a-real-page'),env);assert.equal(missing.status,404);assert.equal(missing.headers.get('x-robots-tag'),'noindex');checks++;
}
const www=await worker.fetch(new Request('http://www.lolobuychina.com/fr/qc.html'),env);assert.equal(www.headers.get('location'),'https://lolobuychina.com/fr/qc');checks++;
const sandbox={window:{},URL};vm.runInNewContext(fs.readFileSync(root+'/catalog-links.js','utf8'),sandbox);
const resolve=sandbox.window.LBC.resolve;
assert.equal(resolve('https://weidian.com/item.html?itemID=7777852466'),'https://cnfanshm.com/AllProducts/6078.html');
assert.equal(resolve('7777852466'),'https://cnfanshm.com/AllProducts/6078.html');
assert.equal(resolve('https://item.taobao.com/item.htm?id=7777852466'),'https://cnfanshm.com/search.html?keywords=7777852466&channelid=2');
assert.equal(resolve('https://detail.1688.com/offer/123456.html'),'https://cnfanshm.com/search.html?keywords=123456&channelid=2');
assert.equal(resolve('hoodie'),'https://cnfanshm.com/search.html?keywords=hoodie&channelid=2');
assert.equal(resolve(''),null);
console.log(`PASS: ${checks} redirect, locale, real-404 and canonical checks; source-ID mapping, unknown-source search and keyword behavior.`);
