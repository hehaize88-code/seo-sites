import fs from 'node:fs/promises';import path from 'node:path';import {createHash} from 'node:crypto';
const work=path.resolve('work/visual'),out=path.resolve('public/visual');
const catalog=JSON.parse(await fs.readFile(path.join(work,'catalog-ids.json'),'utf8'));
const known=new Map();for(const p of (await fs.readFile(path.join(work,'details.jsonl'),'utf8')).trim().split('\n').map(s=>JSON.parse(s)))known.set(p.recordId,p);
const images=new Map();
// A catalogue snapshot can seed existing first-image descriptors, while detail coverage remains explicit.
if(process.env.VISUAL_CATALOG_SEED){const seed=JSON.parse(await fs.readFile(process.env.VISUAL_CATALOG_SEED,'utf8'));for(const p of seed.products){if(catalog.ids.includes(p.id)&&!known.has(p.id)){if(!images.has(p.image))images.set(p.image,[]);images.get(p.image).push({id:p.id,photo:0});}}}
for(const p of known.values()){if(!catalog.ids.includes(p.recordId))continue;for(let photo=0;photo<p.images.length;photo++){const url=p.images[photo];if(!images.has(url))images.set(url,[]);const list=images.get(url);if(!list.some(r=>r.id===p.recordId&&r.photo===photo))list.push({id:p.recordId,photo});}}
const vectors=new Map();for(const file of [process.env.VISUAL_SEED,...(await fs.readdir(work)).filter(f=>/^vectors.*\.jsonl$/.test(f)).map(f=>path.join(work,f))].filter(Boolean)){for(const line of (await fs.readFile(file,'utf8')).trim().split('\n'))if(line){const row=JSON.parse(line);vectors.set(row.image,row.vector);}}
const ids=[],photos=[],refs=[],imageKeys=[],values=[],indexedProducts=new Set();
for(const [image,owners] of images){const vector=vectors.get(image);if(!vector)continue;ids.push(owners[0].id);photos.push(owners[0].photo);refs.push(owners);for(const r of owners)indexedProducts.add(r.id);imageKeys.push(createHash('sha256').update(image).digest('hex').slice(0,12));values.push(...vector);}
const bytes=Buffer.from(Int8Array.from(values).buffer),filename='vectors-'+createHash('sha256').update(bytes).digest('hex').slice(0,12)+'.bin';
const detailCount=catalog.ids.filter(id=>known.has(id)).length;
const manifest={version:2,model:'Xenova/dinov2-small',revision:'c2bb04a51fab207c420665f1946016107bffc701',dtype:'q8',dimension:384,encoding:'int8-unit-127',vectors:filename,createdAt:new Date().toISOString(),catalogCount:catalog.ids.length,indexedProductCount:indexedProducts.size,detailCount,imageCount:images.size,indexedCount:ids.length,failedCount:images.size-ids.length,failedDetailCount:catalog.ids.length-detailCount,complete:images.size===ids.length&&detailCount===catalog.ids.length,ids,photos,imageKeys,refs};
await fs.mkdir(out,{recursive:true});await fs.writeFile(path.join(out,filename),bytes);await fs.writeFile(path.join(out,'index.json'),JSON.stringify(manifest));console.log(JSON.stringify({...manifest,ids:undefined,photos:undefined,refs:undefined,imageKeys:undefined}));
