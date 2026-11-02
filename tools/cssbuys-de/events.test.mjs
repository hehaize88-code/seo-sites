import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const code=readFileSync(new URL('../../cssbuys-de/assets/site-events.js',import.meta.url),'utf8');
for(const language of ['en','de-DE','fr-FR','es-ES','it-IT','pl-PL']){
  const listeners={},events=[];
  class Form {constructor(action){this.action=action;}}
  const window={gtag:(...x)=>events.push(x)};
  const context=vm.createContext({window,URL,HTMLFormElement:Form,location:{href:'https://cssbuys.de/de/',pathname:'/de/'},document:{documentElement:{lang:language},addEventListener:(name,fn)=>listeners[name]=fn}});
  vm.runInContext(code,context);vm.runInContext(code,context);
  const click=(href)=>listeners.click({target:{closest:()=>({href,dataset:{outboundPlacement:'article'}})}});
  click('https://cnfanshp.com/AllProducts/5487.html');
  assert.equal(events.filter(x=>x[1]==='catalog_outbound_click').length,1);
  assert.equal(events.filter(x=>x[1]==='product_outbound_click').length,1);
  assert.equal(events[0][2].product_id,'5487');assert.equal(events[0][2].content_language,language);
  click('https://www.cnfanshp.com/hoodies-sweaters/');
  assert.equal(events.filter(x=>x[1]==='catalog_outbound_click').length,2);
  click('https://cssbuys.de/guides/');assert.equal(events.length,3);
  listeners.submit({target:new Form('https://cnfanshp.com/search.html?keywords=private-test')});
  assert.equal(events.at(-1)[1],'catalog_search');assert(!JSON.stringify(events).includes('private-test'));
}
console.log('PASS: six languages; one catalogue event per exit; legacy product event; www support; internal-link exclusion; no search text collected; duplicate binding prevented.');
