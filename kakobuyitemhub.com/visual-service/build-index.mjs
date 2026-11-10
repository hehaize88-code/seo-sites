import fs from 'node:fs/promises';import * as cheerio from 'cheerio';import {embed} from './embedding.mjs';
await fs.mkdir('.visual-index',{recursive:true});let rows=[];try{rows=JSON.parse(await fs.readFile('.visual-index/index.json','utf8')).items;}catch{}
const existing=new Map(rows.map(x=>[x.id,x]));const catalogue=new Map();const visited=new Set();const failed=[];let pages=0;let next='https://cnfanshm.com/AllProducts/';const started=new Date().toISOString();
async function status(state){await fs.writeFile('.visual-index/progress.tmp',JSON.stringify({state,pages,discovered:catalogue.size,indexed:rows.length,failed:failed.length,started,updated:new Date().toISOString()}));await fs.rename('.visual-index/progress.tmp','.visual-index/progress.json');}
async function get(url){let last;for(let attempt=0;attempt<3;attempt++){try{const r=await fetch(url,{signal:AbortSignal.timeout(20000)});if(!r.ok)throw Error('HTTP '+r.status);return r;}catch(e){last=e;}}throw last;}
try{
 while(next){if(visited.has(next))throw Error('Pagination cycle');visited.add(next);const $=cheerio.load(await(await get(next)).text());const cards=$('.product-card').toArray();if(!cards.length)throw Error('Empty source page '+next);let added=0;
 for(const el of cards){const c=$(el);const id=c.find('a[href*="/AllProducts/"]').attr('href')?.match(/\/(\d+)\.html/)?.[1];const path=c.find('img').attr('data-src');if(!id||!path)continue;const image=new URL(path,'https://cnfanshm.com').href;if(!image.startsWith('https://cnfanshm.com/'))continue;if(!catalogue.has(id)){catalogue.set(id,{id,image});added++;}}
 if(!added)throw Error('Repeated catalogue page '+next);pages++;const link=$('a').toArray().find(a=>/^(下一页|Next|›|»)$/.test($(a).text().trim()));const href=link?$(link).attr('href'):null;next=href?new URL(href,next).href:'';if(next&&!/^https:\/\/cnfanshm\.com\/AllProducts\/list_1_\d+\/$/.test(next))throw Error('Unexpected pagination URL');await status('discovering');console.log('Discovered page',pages,'products',catalogue.size);
 }
 await fs.writeFile('.visual-index/catalogue.json',JSON.stringify([...catalogue.values()]));await status('indexing');
 for(const item of catalogue.values()){
 if(existing.get(item.id)?.image===item.image)continue;
 try{const bytes=Buffer.from(await(await get(item.image)).arrayBuffer());if(bytes.length>10*1024*1024)throw Error('Image exceeds size limit');const vector=await embed(bytes);const value={...item,vector};existing.set(item.id,value);rows=[...existing.values()];}catch(e){failed.push({id:item.id,reason:e.message});}
 if((rows.length+failed.length)%20===0){await save();await status('indexing');console.log('Indexed',rows.length,'of',catalogue.size,'failed',failed.length);}
 }
 // Keep only entries still present in the current verified catalogue.
 rows=rows.filter(x=>catalogue.has(x.id));await save();await fs.writeFile('.visual-index/failures.json',JSON.stringify(failed));await status(failed.length?'complete_with_errors':'complete');console.log('Finished',rows.length,'of',catalogue.size,'pages',pages,'failed',failed.length);
}catch(e){await status('failed');console.error(e.message);process.exitCode=1;}
async function save(){await fs.writeFile('.visual-index/index.tmp',JSON.stringify({model:'Xenova/clip-vit-base-patch32',updated:new Date().toISOString(),pages,items:rows}));await fs.rename('.visual-index/index.tmp','.visual-index/index.json');}
