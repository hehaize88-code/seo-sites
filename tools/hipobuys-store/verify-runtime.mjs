import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
import vm from 'node:vm';
const root=new URL('../../hipobuys-store/',import.meta.url);
const source=await readFile(new URL('_worker.js',root),'utf8');
const m=await import('data:text/javascript;base64,'+Buffer.from(source+'\nexport {canonicalPath,rewriteHref,SECURITY_HEADERS};').toString('base64'));
const tests={'/index.html':'/','/en/':'/','/de/index.html':'/de/','/de//index.html':'/de/','/categories.html':'/categories','/faq.html':'/faq','/storefront-shipping-guide.html':'/storefront-shipping-guide','/w2c-store-links.html':'/w2c-store-links','/it/hipobuy-size-guide-clothing-shoes':'/it/hipobuy-size-guide-clothing-shoes/','/en/hipobuy-size-guide-clothing-shoes/':'/hipobuy-size-guide-clothing-shoes'};
for(const [from,to] of Object.entries(tests)){assert.equal(m.canonicalPath(from),to);assert.equal(m.canonicalPath(to),to);}
assert.equal(m.rewriteHref('https://hipobuy.com/estimation','https://hipobuys.store/'),'https://hipobuy.com/estimation');
assert.equal(m.rewriteHref('https://cnfanssp.com/AllProducts/3400.html?x=1','https://hipobuys.store/'),'https://cnfanshp.com/AllProducts/3400.html?x=1');
assert.match(m.SECURITY_HEADERS['Content-Security-Policy'],/connect-src[^;]*https:\/\/\*\.google-analytics\.com/);
let calls=[];
globalThis.HTMLRewriter=class {on(){return this;}transform(r){return r;}};
const env={ASSETS:{fetch:async request=>{const path=new URL(typeof request==='object'&&'url' in request?request.url:request).pathname;calls.push(path);if(path.endsWith('.xml'))return new Response('<urlset/>',{headers:{'content-type':'application/xml'}});return new Response('<html/>',{headers:{'content-type':'text/html'}});}}};
for(const [from,to] of Object.entries(tests)){const r=await m.default.fetch(new Request('https://hipobuys.store'+from+'?audit=1'),env);assert.equal(r.status,301);assert.equal(r.headers.get('location'),'https://hipobuys.store'+to+'?audit=1');}
for(const path of ['/','/de/','/it/hipobuy-size-guide-clothing-shoes/','/google-sitemap.xml']){const r=await m.default.fetch(new Request('https://hipobuys.store'+path),env);assert.equal(r.status,200);assert.ok(r.headers.get('content-security-policy'));}
const missing=await m.default.fetch(new Request('https://hipobuys.store/not-a-page'),env);assert.equal(missing.status,404);assert.match(missing.headers.get('x-robots-tag'),/noindex/);

// Exercise the real calculator handler with public example and invalid values.
let handler;const output={textContent:''};let values={length:'40',width:'30',height:'25',weight:'3',divisor:'5000'};const events=[];
const form={dataset:{volume:'Volume',billable:'Billable',invalid:'Invalid'},addEventListener:(event,fn)=>{if(event==='submit')handler=fn;},querySelector:()=>output};
const document={documentElement:{lang:'en'},readyState:'complete',querySelector:()=>null,querySelectorAll:q=>q==='[data-calculator]'?[form]:[],addEventListener:()=>{}};
vm.runInNewContext(await readFile(new URL('site.js',import.meta.url),'utf8'),{document,location:{href:'https://hipobuys.store/',pathname:'/'},URL,Intl,FormData:class{get(k){return values[k];}},window:{gtag:(...args)=>events.push(args)}});
handler({preventDefault(){}});assert.match(output.textContent,/Volume: 6 kg · Billable: 6 kg/);
values.height='20';handler({preventDefault(){}});assert.match(output.textContent,/4.8 kg/);
values.weight='10';handler({preventDefault(){}});assert.match(output.textContent,/Billable: 10 kg/);
values.divisor='0';handler({preventDefault(){}});assert.equal(output.textContent,'Invalid');assert.equal(events.length,3);
console.log('PASS: canonical redirects, official links, sitemap alias, CSP, 404 handling and calculator examples/invalid input.');
