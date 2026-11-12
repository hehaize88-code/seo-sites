import fs from 'node:fs/promises';
import path from 'node:path';
import {pipeline,env,RawImage} from '@huggingface/transformers';
const work=path.resolve('work/visual');
const records=(await fs.readFile(path.join(work,'details.jsonl'),'utf8')).trim().split('\n').filter(Boolean).map(JSON.parse);
const images=[...new Set(records.flatMap(p=>p.images))],known=new Set();
for(const file of [process.env.VISUAL_SEED,...(await fs.readdir(work)).filter(f=>/^vectors.*\.jsonl$/.test(f)).map(f=>path.join(work,f))].filter(Boolean)){
 for(const line of (await fs.readFile(file,'utf8')).trim().split('\n'))if(line)known.add(JSON.parse(line).image);
}
const retryOnly=process.env.VISUAL_RETRY_LIST?new Set(JSON.parse(await fs.readFile(process.env.VISUAL_RETRY_LIST,'utf8'))):null;
const pending=images.filter(url=>!known.has(url)&&(!retryOnly||retryOnly.has(url)));
const output=process.env.VISUAL_OUTPUT||'vectors-pooled.jsonl';if(!/^vectors[-a-z0-9]*\.jsonl$/.test(output))throw Error('Invalid checkpoint filename');
const concurrency=Math.max(1,Math.min(64,Number(process.env.VISUAL_CONCURRENCY)||32));
console.log(JSON.stringify({pending:pending.length,seed:images.filter(url=>known.has(url)).length,concurrency}));
if(!pending.length)process.exit(0);
env.allowRemoteModels=false;env.localModelPath=path.resolve('public/visual-models')+'/';
const extractor=await pipeline('image-feature-extraction','dinov2-small',{dtype:'q8',device:'cpu',session_options:{intraOpNumThreads:4,interOpNumThreads:1}});
async function read(url){for(let i=0;i<2;i++)try{
 const r=await fetch(url,{signal:AbortSignal.timeout(Number(process.env.VISUAL_TIMEOUT)||45000)});
 if(r.status===429){await new Promise(resolve=>setTimeout(resolve,Math.max(5000,Number(r.headers.get('Retry-After')||0)*1000)));throw Error('HTTP 429');}
 if(!r.ok)throw Error('HTTP '+r.status);return await RawImage.fromBlob(await r.blob());
}catch(e){if(i===1)throw e;await new Promise(r=>setTimeout(r,1500));}}
let next=0,done=0,failed=0,lastReport=0,inferencing=false,modelMs=0;
const started=Date.now(),ready=[];
function report(){if(done-lastReport>=100||done===pending.length){lastReport=done;console.log(JSON.stringify({done,total:pending.length,failed,seconds:Math.round((Date.now()-started)/1000),modelSeconds:Math.round(modelMs/1000)}));}}
async function failure(url,e){failed++;await fs.appendFile(path.join(work,'image-errors-pooled.jsonl'),JSON.stringify({image:url,error:e.message})+'\n');}
async function encode(batch){
 const t=Date.now(),tensor=await extractor(batch.map(item=>item.image));modelMs+=Date.now()-t;
 if(tensor.dims.length!==3||tensor.dims[2]!==384||tensor.dims[0]!==batch.length)throw Error('Unexpected embedding dimensions');
 const stride=tensor.dims[1]*tensor.dims[2],rows=[];
 for(let i=0;i<batch.length;i++){
  const v=tensor.data.slice(i*stride,i*stride+384),norm=Math.hypot(...v);if(!norm)throw Error('Empty vector');
  const vector=Array.from(v,x=>Math.max(-127,Math.min(127,Math.round(x/norm*127))));rows.push(JSON.stringify({image:batch[i].url,vector}));
 }
 await fs.appendFile(path.join(work,output),rows.join('\n')+'\n');
}
async function drain(){
 if(inferencing)return;inferencing=true;
 while(ready.length){
  const batch=ready.splice(0,4);
  try{await encode(batch);}catch(e){
   // Isolate an invalid image instead of losing the other photos in its batch.
   for(const item of batch)try{await encode([item]);}catch(error){await failure(item.url,error);}
  }
  done+=batch.length;report();for(const item of batch)item.resolve();
 }
 inferencing=false;
}
await Promise.all(Array.from({length:concurrency},async()=>{
 while(next<pending.length){const url=pending[next++];try{
  const image=await read(url);await new Promise(resolve=>{ready.push({url,image,resolve});void drain();});
 }catch(e){await failure(url,e);done++;report();}}
}));
await extractor.dispose();
