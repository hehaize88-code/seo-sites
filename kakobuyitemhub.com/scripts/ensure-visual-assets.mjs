import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';
const manifest=JSON.parse(fs.readFileSync('src/content/visual-assets.json'));let fetched=0;
for(const item of manifest.files){const target=path.join('public',item.path);let bytes=fs.existsSync(target)?fs.readFileSync(target):null;if(bytes&&crypto.createHash('sha256').update(bytes).digest('hex')===item.sha256)continue;
 const r=await fetch(manifest.base+'/'+item.path,{signal:AbortSignal.timeout(120000)});if(!r.ok)throw Error('Missing visual asset '+item.path);bytes=Buffer.from(await r.arrayBuffer());if(bytes.length!==item.bytes||crypto.createHash('sha256').update(bytes).digest('hex')!==item.sha256)throw Error('Visual asset checksum mismatch '+item.path);fs.mkdirSync(path.dirname(target),{recursive:true});fs.writeFileSync(target,bytes);fetched++;}
console.log('Visual assets verified:',manifest.files.length,'downloaded:',fetched);
