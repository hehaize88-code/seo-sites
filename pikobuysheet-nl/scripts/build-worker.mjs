import {readdir,readFile,writeFile,mkdir,copyFile} from 'node:fs/promises';
import {join,extname} from 'node:path';
import {gzipSync} from 'node:zlib';
import {build} from 'esbuild';
import {languages} from '../src/lib/i18n.mjs';

const root='.astro-out',assets={},htmlGroups=new Map(),bundles={};
const types={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.xml':'application/xml; charset=utf-8','.txt':'text/plain; charset=utf-8','.png':'image/png','.svg':'image/svg+xml','.woff2':'font/woff2'};
async function walk(dir){
  for(const file of await readdir(dir,{withFileTypes:true})){
    const path=join(dir,file.name);
    if(file.isDirectory()){await walk(path);continue;}
    if(file.name==='asset-map.mjs')continue;
    const key='/'+path.slice(root.length+1),type=types[extname(file.name)]||'application/octet-stream',data=await readFile(path);
    if(extname(file.name)==='.html'){
      // Compress a locale together so shared navigation, product HTML and
      // repeated vocabulary are stored once in the gzip dictionary.
      const prefix=key.split('/')[1],group=Object.hasOwn(languages,prefix)?prefix:'nl';
      if(!htmlGroups.has(group))htmlGroups.set(group,{buffers:[],length:0});
      const entry=htmlGroups.get(group);
      assets[key]={type,group,offset:entry.length,length:data.length};
      entry.buffers.push(data);entry.length+=data.length;
    }else{
      const binary=/image\/png|font\/|octet-stream/.test(type),gzip=!binary&&data.length>1024;
      assets[key]={type,binary:binary||gzip,gzip,data:(gzip?gzipSync(data,{level:9}):data).toString(binary||gzip?'base64':'utf8')};
    }
  }
}
await walk(root);
for(const [group,{buffers}] of htmlGroups)bundles[group]=gzipSync(Buffer.concat(buffers),{level:9}).toString('base64');
await writeFile(join(root,'asset-map.mjs'),'export const bundles='+JSON.stringify(bundles)+';\nexport default '+JSON.stringify(assets)+';');
await mkdir('dist/server',{recursive:true});await mkdir('dist/.openai',{recursive:true});
await copyFile('.openai/hosting.json','dist/.openai/hosting.json');
await build({entryPoints:['worker/index.mjs'],outfile:'dist/server/index.js',bundle:true,format:'esm',platform:'browser',target:'es2022',minify:true});
const compressedBytes=gzipSync(await readFile('dist/server/index.js'),{level:9}).length;
// A conservative project budget; do not silently grow the deployment artifact.
if(compressedBytes>3_000_000)throw Error(`Worker exceeds the 3 MB project budget: ${compressedBytes} bytes`);
console.log(`Bundled ${Object.keys(assets).length} assets in ${htmlGroups.size} locale groups; Worker gzip size ${compressedBytes} bytes.`);
