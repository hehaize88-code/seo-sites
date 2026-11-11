import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
export async function writeIndex(catalog,vectors,output,complete=true){
 const ids=[],values=[],imageKeys=[];for(const product of catalog.products){const row=vectors.get(product.id);if(row&&row.image===product.image){ids.push(product.id);imageKeys.push(createHash('sha256').update(product.image).digest('hex').slice(0,12));values.push(...row.vector);}}
 if(!ids.length)throw Error('No embeddings produced');
 const bytes=Buffer.from(Int8Array.from(values).buffer),hash=createHash('sha256').update(bytes).digest('hex').slice(0,12),filename=`vectors-${hash}.bin`;
 const manifest={version:1,model:'Xenova/dinov2-small',revision:'c2bb04a51fab207c420665f1946016107bffc701',dtype:'q8',dimension:384,encoding:'int8-unit-127',vectors:filename,createdAt:new Date().toISOString(),catalogCount:catalog.products.length,indexedCount:ids.length,failedCount:complete?catalog.products.length-ids.length:0,complete,ids,imageKeys};
 await fs.mkdir(output,{recursive:true});await fs.writeFile(path.join(output,filename),bytes);await fs.writeFile(path.join(output,'index.json'),JSON.stringify(manifest));return {indexed:ids.length,catalog:catalog.products.length,failed:manifest.failedCount,bytes:values.length};
}
