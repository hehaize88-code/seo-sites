// Rebuildable image features only. No product names, prices, or image files are stored in the published index.
import fs from 'node:fs/promises';
import path from 'node:path';
import {spawn} from 'node:child_process';
import {load} from 'cheerio/slim';
import {parseSourceDetail,sourceImage} from '../lib/source-images.mjs';
const origin='https://cnfanshm.com',work=path.resolve('work/visual'),out=path.resolve('public/visual');
await fs.mkdir(work,{recursive:true});await fs.mkdir(out,{recursive:true});
async function request(url){for(let i=0;i<4;i++){try{const r=await fetch(url,{signal:AbortSignal.timeout(25000)});if(r.status===429){await new Promise(resolve=>setTimeout(resolve,Math.max(5000,Number(r.headers.get('Retry-After')||0)*1000)*(i+1)));throw Error('HTTP 429');}if(!r.ok)throw Error(`HTTP ${r.status}`);return r;}catch(e){if(i===3)throw e;await new Promise(r=>setTimeout(r,1500*(i+1)));}}}
async function pool(items,fn,n=8){let next=0;await Promise.all(Array.from({length:n},async()=>{while(next<items.length){const i=next++;await fn(items[i],i);}}));}
const url=page=>origin+'/index.php?'+new URLSearchParams({m:'home',c:'Lists',a:'index',tid:'1',sort:'new',sort_asc:'desc',ZXljbXM:'1',page:String(page)});
const catalog=new Map();
function add(html){const q=load(html);q('.product-grid .product-card').each((_,el)=>{const id=q(el).attr('data-id'),img=q(el).find('.product-image img');if(/^\d{1,8}$/.test(id||'')&&sourceImage(img.attr('data-src')||img.attr('src'))&&q(el).find('.product-name').text().trim())catalog.set(id,{id});});}
let last=0;
if(process.argv.includes('--resume-catalog')){const saved=JSON.parse(await fs.readFile(path.join(work,'catalog-ids.json'),'utf8'));for(const id of saved.ids)catalog.set(id,{id});last=-1;}
else{
for(let page=1;page<=300;page++){
 const html=await(await request(url(page))).text(),q=load(html),before=catalog.size;add(html);
 const hasNext=q('.pagination a[href]').toArray().some(a=>Number((q(a).attr('href')||'').match(/[?&]page=(\d+)/)?.[1])>page);
 if(before===catalog.size)throw Error('Empty or repeated catalog page '+page);
 if(page%20===0)console.log(JSON.stringify({phase:'catalog',page,total:catalog.size}));
 if(!hasNext){last=page;break;}
}
await fs.writeFile(path.join(work,'catalog-ids.json'),JSON.stringify({ids:[...catalog.keys()],createdAt:new Date().toISOString()}));
}
if(!last)throw Error('Incomplete catalogue');
console.log(JSON.stringify({phase:'catalog-complete',count:catalog.size,last}));
let details=new Map();try{if(!process.argv.includes('--resume-catalog'))await fs.writeFile(path.join(work,'details.jsonl'),'');for(const line of (await fs.readFile(path.join(work,'details.jsonl'),'utf8')).trim().split('\n'))if(line){const p=JSON.parse(line);details.set(p.recordId,p);}}catch{}
let done=0,failures=[];
await pool([...catalog.keys()],async id=>{if(!details.has(id)){try{const p=parseSourceDetail(await(await request(origin+'/AllProducts/'+id+'.html')).text(),id);if(!p||!p.images.length)throw Error('No detail images');details.set(id,p);await fs.appendFile(path.join(work,'details.jsonl'),JSON.stringify(p)+'\n');}catch(e){failures.push({id,error:e.message});}await new Promise(r=>setTimeout(r,150));}done++;if(done%200===0)console.log(JSON.stringify({phase:'details',done,total:catalog.size,failures:failures.length}));},Math.max(1,Math.min(12,Number(process.env.VISUAL_DETAIL_CONCURRENCY)||4)));
const unique=new Map();for(const id of catalog.keys()){const p=details.get(id);if(!p)continue;for(let i=0;i<p.images.length;i++){const image=p.images[i];if(!unique.has(image))unique.set(image,{image,refs:[]});unique.get(image).refs.push({id,photo:i});}}
await fs.writeFile(path.join(work,'image-manifest.json'),JSON.stringify({createdAt:new Date().toISOString(),catalogCount:catalog.size,detailCount:[...catalog.keys()].filter(id=>details.has(id)).length,failures,images:[...unique.values()]}));
console.log(JSON.stringify({phase:'all-images',products:catalog.size,details:details.size,images:unique.size,failures:failures.length}));
if(process.argv.includes('--crawl-only'))process.exit(0);
// Resume image work by source URL; completed vectors are reused across runs.
async function run(script){await new Promise((resolve,reject)=>{const child=spawn(process.execPath,[path.resolve('scripts',script)],{stdio:'inherit',env:process.env});child.on('error',reject);child.on('exit',code=>code===0?resolve():reject(Error(script+' exited '+code)));});}
await run('index-images-pooled.mjs');
await run('package-visual-index.mjs');
