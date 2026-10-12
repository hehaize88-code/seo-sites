import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const root = new URL('../', import.meta.url);
const workerSource = fs.readFileSync(new URL('_worker.js', root), 'utf8');
const { default: worker } = await import('data:text/javascript;base64,' + Buffer.from(workerSource).toString('base64'));
let assetsCalls = 0;
const env = { ASSETS: { fetch: async (req) => { assetsCalls++; return new Response('<html>' + new URL(req.url).pathname + '</html>', { headers: { 'Content-Type': 'text/html' } }); } } };
for (const [path, status, destination] of [
  ['/',200],['/de/',200],['/zh-CN/hoobuy-qc-photo-checklist',200],
  ['/index.html',301,'/'],['/index',301,'/'],['/de/index.html',301,'/de/'],
  ['/de',301,'/de/'],['/de/guides.html',301,'/de/guides'],['/guides/',301,'/guides'],
  ['/unknown-seo-test',404],['/_src/original.json',404],['/de/not-real',404],['/assets/site.js',200]
]) {
 const response = await worker.fetch(new Request('https://hoobuys.org'+path),env);
 assert.equal(response.status,status,path);
 if(destination) assert.equal(new URL(response.headers.get('Location')).pathname,destination,path);
}
const www = await worker.fetch(new Request('https://www.hoobuys.org/de/guides.html?utm_source=test'),env);
assert.equal(www.headers.get('Location'),'https://hoobuys.org/de/guides?utm_source=test');
const post = await worker.fetch(new Request('https://hoobuys.org/',{method:'POST'}),env);assert.equal(post.status,405);
const head = await worker.fetch(new Request('https://hoobuys.org/',{method:'HEAD'}),env);assert.equal(await head.text(),'');
let submit, click;
const values={weight:'2400',length:'40',width:'30',height:'25',divisor:'6000'};
const nodes=Object.fromEntries(['actual','volume','greater'].map(k=>[k,{textContent:''}]));let result={hidden:true};const events=[];
const form={reportValidity:()=>true,addEventListener:(type,fn)=>{submit=fn;}};
const context={document:{documentElement:{lang:'en'},getElementById:()=>form,addEventListener:(type,fn)=>{if(type==='click')click=fn;},querySelector:(q)=>q==='.calc-result'?result:nodes[q.match(/"(.*?)"/)[1]]},FormData:class{*[Symbol.iterator](){yield* Object.entries(values);}},Intl,Number,Math,URL,location:{pathname:'/test',href:'https://hoobuys.org/test',origin:'https://hoobuys.org'},gtag:(...args)=>events.push(args)};
vm.runInNewContext(fs.readFileSync(new URL('assets/site.js',root),'utf8'),context);
submit({preventDefault(){}});assert.equal(nodes.actual.textContent,'2.4');assert.equal(nodes.volume.textContent,'5');assert.equal(nodes.greater.textContent,'5');assert.equal(result.hidden,false);assert.equal(events[0][1],'shipping_calculator_use');
values.length='35';values.width='25';values.height='20';submit({preventDefault(){}});assert.equal(nodes.volume.textContent,'2.92');
values.weight='10000';submit({preventDefault(){}});assert.equal(nodes.greater.textContent,'10');
for (const host of ['cnfanssp.com','www.cnfanssp.com']) {
 const before = events.length;
 const link = { href: 'https://' + host + '/AllProducts/5974.html?private=value', closest: () => null };
 click({target:{closest:()=>link}});
 assert.equal(events.length,before+1);
 assert.equal(events.at(-1)[1],'product_index_click');
 assert.equal(events.at(-1)[2].link_url,'https://' + host + '/AllProducts/5974.html');
}
const beforeOther = events.length;
click({target:{closest:()=>({href:'https://example.com/product',closest:()=>null})}});
assert.equal(events.length,beforeOther);
console.log('PASS: main-site product click tracking and query omission; canonical redirects, locale routes, source blocking, real 404s, HEAD/method handling, volumetric examples, actual-weight maximum and calculator event.');
