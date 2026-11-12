// Can run bounded shards concurrently. Only derived features are written.
import fs from 'node:fs/promises';import path from 'node:path';import {createHash} from 'node:crypto';
import {pipeline,env,RawImage} from '@huggingface/transformers';
const shard=Number(process.argv[2]||0),shards=Number(process.argv[3]||1),work=path.resolve('work/visual');
const records=(await fs.readFile(path.join(work,'details.jsonl'),'utf8')).trim().split('\n').map(s=>JSON.parse(s));
const images=[...new Set(records.flatMap(p=>p.images))].filter(image=>parseInt(createHash('sha256').update(image).digest('hex').slice(0,8),16)%shards===shard);
const vectors=new Map();for(const file of [process.env.VISUAL_SEED,...(await fs.readdir(work)).filter(f=>/^vectors.*\.jsonl$/.test(f)).map(f=>path.join(work,f))].filter(Boolean)){for(const line of (await fs.readFile(file,'utf8')).trim().split('\n'))if(line){const row=JSON.parse(line);vectors.set(row.image,row.vector);}}
const pending=images.filter(image=>!vectors.has(image));console.log(JSON.stringify({shard,pending:pending.length,known:images.length-pending.length}));
env.allowRemoteModels=false;env.localModelPath=path.resolve('public/visual-models')+'/';
const extractor=await pipeline('image-feature-extraction','dinov2-small',{dtype:'q8',device:'cpu',session_options:{intraOpNumThreads:2,interOpNumThreads:1}});
async function read(url){for(let i=0;i<3;i++)try{const r=await fetch(url,{signal:AbortSignal.timeout(25000)});if(!r.ok)throw Error('HTTP '+r.status);return await RawImage.fromBlob(await r.blob());}catch(e){if(i===2)throw e;await new Promise(r=>setTimeout(r,3000*(i+1)));}}
const queued=new Map();const queue=i=>{if(i<pending.length)queued.set(i,read(pending[i]).then(image=>({image}),error=>({error})));};for(let i=0;i<16;i++)queue(i);
const started=Date.now();let failed=0;
for(let i=0;i<pending.length;i++){
 const loaded=await queued.get(i);queued.delete(i);queue(i+16);
 try{if(loaded.error)throw loaded.error;const v=(await extractor(loaded.image)).data.slice(0,384),norm=Math.hypot(...v);if(!norm)throw Error('Empty vector');const vector=Array.from(v,x=>Math.max(-127,Math.min(127,Math.round(x/norm*127))));await fs.appendFile(path.join(work,'vectors-shard-'+shard+'.jsonl'),JSON.stringify({image:pending[i],vector})+'\n');}catch(e){failed++;await fs.appendFile(path.join(work,'image-errors-'+shard+'.jsonl'),JSON.stringify({image:pending[i],error:e.message})+'\n');}
 if((i+1)%100===0||i===pending.length-1)console.log(JSON.stringify({shard,done:i+1,total:pending.length,failed,seconds:Math.round((Date.now()-started)/1000)}));
}
await extractor.dispose();
