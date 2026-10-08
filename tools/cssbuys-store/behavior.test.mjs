import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const root = new URL('../../cssbuys-store/', import.meta.url);
const script = fs.readFileSync(new URL('assets/site-tracking.js', root), 'utf8');
class Element { closest() {return this.link;} }
class Form { constructor(term) {this.dataset={};this.action='https://www.cnfanssp.com/search.html';this.input={value:term,focus(){}};this.elements={namedItem:()=>this.input};this.submissions=0;} matches(){return true;} submit(){this.submissions++;} }
function setup(analytics=true) {
 const events=[],handlers={},winhandlers={},timers=[],forms=[];
 const window={location:{href:'https://cssbuys.store/fr/',pathname:'/fr/'},addEventListener:(name,fn)=>winhandlers[name]=fn,setTimeout:fn=>timers.push(fn)};
 if(analytics)window.gtag=(...args)=>events.push(args);
 const document={documentElement:{lang:'fr'},addEventListener:(name,fn)=>handlers[name]=fn,querySelectorAll:()=>forms};
 const context=vm.createContext({window,document,URL,Element,HTMLFormElement:Form});
 vm.runInContext(script,context);vm.runInContext(script,context);
 return {events,handlers,winhandlers,timers,forms};
}
const x=setup();const element=new Element();
element.link={href:'https://www.cnfanssp.com/AllProducts/3400.html',textContent:'Jordan 4',dataset:{location:'hero_products',productId:'3400'}};
x.handlers.click({target:element});assert.equal(x.events.length,1);assert.equal(x.events[0][1],'open_main_site');assert.equal(x.events[0][2].page_language,'fr');assert.equal(x.events[0][2].product_id,'3400');
element.link.href='https://cssbuys.store/fr/guides/';x.handlers.click({target:element});assert.equal(x.events.length,1);
const form=new Form('  Jordan 4  ');x.forms.push(form);let prevented=0;
x.handlers.submit({target:form,preventDefault:()=>prevented++});assert.equal(prevented,1);assert.equal(form.input.value,'Jordan 4');
assert.equal(x.events[1][1],'search');assert.equal(x.events[1][2].search_term,'Jordan 4');assert.equal(x.events[2][2].click_location,'homepage_search');
x.events[2][2].event_callback();x.timers.forEach(fn=>fn());assert.equal(form.submissions,1);
x.winhandlers.pageshow();assert.equal(form.dataset.submitting,undefined);
const y=setup(false);let blocked=false;y.handlers.submit({target:new Form('LACOSTE'),preventDefault:()=>blocked=true});assert.equal(blocked,false);
let blank=false;y.handlers.submit({target:new Form('   '),preventDefault:()=>blank=true});assert.equal(blank,true);
const workerCode=fs.readFileSync(new URL('_worker.js',root),'utf8');
const worker=(await import('data:text/javascript;base64,'+Buffer.from(workerCode).toString('base64'))).default;
let injected=0;globalThis.HTMLRewriter=class {on(_,handler){this.handler=handler;return this;}transform(response){this.handler.element({getAttribute:()=> 'inline',append:()=>injected++});return response;}};
const env={ASSETS:{fetch:async()=>new Response('<html></html>',{headers:{'content-type':'text/html'}})}};
for(const [from,to] of [['/de','/de/'],['/fr/guides','/fr/guides/'],['/es/index.html','/es/'],['/it/guides/qc-guide.html','/it/guides/qc-guide'],['/products/5987','/products/3400']]){
 const r=await worker.fetch(new Request('https://cssbuys.store'+from),env);assert.equal(r.status,301);assert.equal(r.headers.get('location'),'https://cssbuys.store'+to);
}
const r=await worker.fetch(new Request('https://cssbuys.store/pl/'),env);assert.equal(r.status,200);assert.equal(injected,0);assert.match(r.headers.get('content-security-policy'),/www\.cnfanssp\.com/);
console.log('PASS: outbound/search events, analytics fallback, double-submit protection, browser-back reset, localized redirects and single script injection.');
