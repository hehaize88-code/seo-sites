/** Rebuildable visual features only. Product content stays on cnfanshm.com. */
import fs from 'node:fs/promises';
import path from 'node:path';
import {load} from 'cheerio/slim';
import {writeIndex} from './visual-index-files.mjs';
const root=process.cwd(), work=path.join(root,'work/visual'), output=path.join(root,'public/visual');
await fs.mkdir(work,{recursive:true});await fs.mkdir(output,{recursive:true});
const origin='https://cnfanshm.com';
const checkpoint=path.join(work,'catalog.json');
const wait=ms=>new Promise(r=>setTimeout(r,ms));
async function request(url){for(let attempt=0;attempt<3;attempt++){try{const r=await fetch(url,{signal:AbortSignal.timeout(30000)});if(!r.ok)throw Error(`HTTP ${r.status}`);return r;}catch(e){if(attempt===2)throw e;await wait(750*(attempt+1));}}}
let catalog;
try{catalog=JSON.parse(await fs.readFile(checkpoint,'utf8'));}catch{catalog={products:[],nextPage:1,complete:false};}
const seen=new Set(catalog.products.map(p=>p.id));
for(let page=catalog.nextPage;!catalog.complete&&page<=300;page++){
 const params=new URLSearchParams({m:'home',c:'Lists',a:'index',tid:'1',sort:'new',sort_asc:'desc',ZXljbXM:'1',page:String(page)});
 const $=load(await(await request(origin+'/index.php?'+params)).text());
 const cards=$('.product-grid .product-card');if(!cards.length)throw Error(`Empty catalog page ${page}; refusing incomplete build`);
 let added=0;
 cards.each((_,card)=>{const el=$(card),id=el.attr('data-id'),img=el.find('.product-image img'),raw=img.attr('data-src')||img.attr('src');if(!/^\d{1,8}$/.test(id||'')||!raw||seen.has(id))return;const url=new URL(raw,origin);if(url.hostname!=='cnfanshm.com'||!url.pathname.startsWith('/uploads/'))return;seen.add(id);catalog.products.push({id,image:url.href});added++;});
 const hasNext=$('.pagination a[href]').toArray().some(a=>{const href=$(a).attr('href')||'';const m=href.match(/[?&]page=(\d+)/)||href.match(/list_\d+_(\d+)/);return m?+m[1]>page:/下一页|Next/i.test($(a).text());});
 if(!added&&hasNext)throw Error(`Repeated catalog page ${page}; source pagination changed`);
 catalog.nextPage=page+1;catalog.complete=!hasNext;catalog.fetchedAt=new Date().toISOString();await fs.writeFile(checkpoint,JSON.stringify(catalog));
 console.log(JSON.stringify({phase:'catalog',page,added,total:catalog.products.length,complete:catalog.complete}));
}
if(!catalog.complete)throw Error('Catalog page safety limit reached');
if(process.argv.includes('--crawl-only'))process.exit(0);
const {pipeline,env,RawImage}=await import('@huggingface/transformers');
env.allowRemoteModels=false;env.localModelPath=path.join(root,'public/visual-models/');env.backends.onnx.wasm.numThreads=1;
const extractor=await pipeline('image-feature-extraction','dinov2-small',{dtype:'q8',device:'cpu',session_options:{intraOpNumThreads:2,interOpNumThreads:1}});
const vectorPath=path.join(work,'vectors.jsonl');let vectors=new Map();
try{for(const line of (await fs.readFile(vectorPath,'utf8')).trim().split('\n')){if(line){const v=JSON.parse(line);vectors.set(v.id,v);}}}catch{}
const failures=[];let done=0;
const pending=catalog.products.filter(product=>vectors.get(product.id)?.image!==product.image);
done=catalog.products.length-pending.length;
// Fetch a small window ahead; model inference remains bounded and deterministic.
const images=new Map();
function queue(i){if(i>=pending.length)return;const product=pending[i];images.set(i,request(product.image).then(r=>r.blob()).then(blob=>RawImage.fromBlob(blob)).then(image=>({image}),error=>({error})));}
const concurrency=48;
for(let i=0;i<concurrency;i++)queue(i);
for(let i=0;i<pending.length;i++){
 const product=pending[i];const loaded=await images.get(i);images.delete(i);queue(i+concurrency);
 try{
  if(loaded.error)throw loaded.error;
  const tensor=await extractor(loaded.image);const embedding=tensor.data.slice(0,384);const norm=Math.hypot(...embedding);if(embedding.length!==384||!norm)throw Error('Invalid embedding');
  const vector=Array.from(embedding,x=>Math.max(-127,Math.min(127,Math.round(x/norm*127))));
  const row={id:product.id,image:product.image,vector};vectors.set(product.id,row);await fs.appendFile(vectorPath,JSON.stringify(row)+'\n');
 }catch(e){failures.push({id:product.id,error:e.message});}
 done++;if(done%50===0||done===catalog.products.length)console.log(JSON.stringify({phase:'embedding',done,total:catalog.products.length,failures:failures.length}));
}
const summary=await writeIndex(catalog,vectors,output);
await fs.writeFile(path.join(work,'failures.json'),JSON.stringify(failures,null,2));
console.log(JSON.stringify({phase:'complete',...summary}));
await extractor.dispose();
