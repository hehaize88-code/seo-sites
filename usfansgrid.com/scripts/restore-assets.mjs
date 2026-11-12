import fs from 'node:fs/promises';
import {createHash} from 'node:crypto';
const manifest=JSON.parse(await fs.readFile('assets-binary/manifest.json','utf8'));
for(const asset of manifest){
 const bytes=Buffer.concat(await Promise.all(asset.parts.map(part=>fs.readFile(part))));
 if(createHash('sha256').update(bytes).digest('hex')!==asset.sha256)throw new Error('Asset checksum mismatch: '+asset.path);
 await fs.mkdir(asset.path.slice(0,asset.path.lastIndexOf('/')),{recursive:true});
 await fs.writeFile(asset.path,bytes);
}
console.log('Restored and verified image-search model and runtime.');
