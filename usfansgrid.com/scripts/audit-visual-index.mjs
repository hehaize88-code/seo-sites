// Verify published descriptors against the complete source-gallery crawl.
import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
const root=path.resolve('public/visual');
const index=JSON.parse(await fs.readFile(path.join(root,'index.json'),'utf8'));
const catalog=JSON.parse(await fs.readFile('work/visual/catalog-ids.json','utf8'));
const details=new Map((await fs.readFile('work/visual/details.jsonl','utf8')).trim().split('\n').filter(Boolean).map(line=>{const p=JSON.parse(line);return[p.recordId,p];}));
const expected=new Map();let galleryReferences=0;
for(const id of catalog.ids){const product=details.get(id);if(!product)continue;
 for(let photo=0;photo<product.images.length;photo++){
  const url=product.images[photo],u=new URL(url);
  if(!['cnfanshm.com','www.cnfanshm.com'].includes(u.hostname)||!u.pathname.startsWith('/uploads/'))throw Error('Unexpected image source');
  const key=createHash('sha256').update(url).digest('hex').slice(0,12);
  if(!expected.has(key))expected.set(key,new Set());expected.get(key).add(id+':'+photo);galleryReferences++;
 }
}
const values=new Int8Array(await fs.readFile(path.join(root,index.vectors)));
if(index.dimension!==384||values.length!==index.indexedCount*384||index.ids.length!==index.indexedCount||index.imageKeys.length!==index.indexedCount||index.refs.length!==index.indexedCount)throw Error('Descriptor shape mismatch');
if(new Set(index.imageKeys).size!==index.imageKeys.length)throw Error('Duplicate image key');
let indexedReferences=0;const owners=new Set();
for(let row=0;row<index.indexedCount;row++){
 const wanted=expected.get(index.imageKeys[row]);if(!wanted)throw Error('Image not present in current source galleries');
 const refs=index.refs[row];if(refs.length!==wanted.size)throw Error('Missing shared-image owner');
 for(const r of refs){if(!wanted.has(r.id+':'+r.photo))throw Error('Image points to the wrong product or photo');owners.add(r.id);indexedReferences++;}
 const norm=Math.hypot(...values.slice(row*384,(row+1)*384));if(norm<115||norm>140)throw Error('Invalid image descriptor');
}
const missingImages=expected.size-index.indexedCount;
const missingProducts=catalog.ids.filter(id=>!details.has(id)).length;
if(index.failedCount!==missingImages||index.failedDetailCount!==missingProducts||index.indexedProductCount!==owners.size||index.imageCount!==expected.size)throw Error('Coverage report mismatch');
if(index.complete!==(!missingImages&&!missingProducts))throw Error('Incorrect completeness flag');
if(process.argv.includes('--require-complete')&&!index.complete)throw Error('Full-gallery coverage is not ready');
console.log(JSON.stringify({products:catalog.ids.length,details:details.size,uniqueImages:expected.size,indexedImages:index.indexedCount,galleryReferences,indexedReferences,missingImages,missingProducts,complete:index.complete}));
