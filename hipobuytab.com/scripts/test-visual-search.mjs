import fs from 'node:fs/promises';import path from 'node:path';import assert from 'node:assert/strict';
import {pipeline,env,RawImage} from '@huggingface/transformers';
import {nearest} from '../lib/visual/matching.ts';
env.allowRemoteModels=false;env.localModelPath=path.resolve('public/visual-models')+'/';
const model=await pipeline('image-feature-extraction','dinov2-small',{dtype:'q8',device:'cpu',session_options:{intraOpNumThreads:2,interOpNumThreads:1}});
const index=JSON.parse(await fs.readFile('public/visual/index.json','utf8'));const values=new Int8Array(await fs.readFile('public/visual/'+index.vectors));
const reports=[];
for(const file of ['product-6077.jpg','product-6077-crop.jpg','product-6074.jpg','product-6082.jpg']){
 const start=Date.now();const image=await RawImage.read('/workspace/shared/hipobuy-search-tests/'+file);const output=await model(image);const hits=nearest(output.data.slice(0,384),values,index,10);const expected=file.match(/product-(\d+)/)[1];const rank=hits.findIndex(h=>h.id===expected)+1;assert(rank>0&&rank<=3,`${file}: expected ${expected} in top 3; got ${JSON.stringify(hits.slice(0,3))}`);reports.push({file,expected,rank,milliseconds:Date.now()-start,top:hits.slice(0,3)});
}
assert.throws(()=>nearest([1],values,index),/index-invalid/);
assert.throws(()=>nearest(new Float32Array(384),values,index),/image-invalid/);
assert.throws(()=>nearest(new Float32Array(384).fill(1),new Int8Array(3),index),/index-invalid/);
console.log(JSON.stringify({indexed:index.indexedCount,reports},null,2));await fs.writeFile('work/visual/test-results.json',JSON.stringify({indexed:index.indexedCount,reports},null,2));await model.dispose();
