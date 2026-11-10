import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';
const input=process.argv[2];const modelDir=process.argv[3];if(!input||!modelDir)throw Error('Usage: node scripts/prepare-visual-assets.mjs INDEX_JSON MODEL_DIRECTORY');
const root='public/visual/v1';fs.mkdirSync(root+'/model/onnx',{recursive:true});
for(const name of ['config.json','preprocessor_config.json'])fs.copyFileSync(path.join(modelDir,name),root+'/model/'+name);
fs.copyFileSync('node_modules/@huggingface/transformers/dist/transformers.web.min.js',root+'/transformers.js');
for(const name of ['ort-wasm-simd-threaded.mjs','ort-wasm-simd-threaded.wasm'])fs.copyFileSync('node_modules/onnxruntime-web/dist/'+name,root+'/'+name);
const bytes=fs.readFileSync(path.join(modelDir,'onnx/vision_model_quantized.onnx'));const chunks=[];for(let offset=0;offset<bytes.length;offset+=16*1024*1024){const name='vision-'+chunks.length+'.bin';const part=bytes.subarray(offset,offset+16*1024*1024);fs.writeFileSync(root+'/model/onnx/'+name,part);chunks.push({url:'/visual/v1/model/onnx/'+name,bytes:part.length,sha256:crypto.createHash('sha256').update(part).digest('hex')});}
const index=JSON.parse(fs.readFileSync(input));const n=index.items.length,dimensions=512;const vectors=new Int8Array(n*dimensions);const norms=new Float32Array(n);for(let i=0;i<n;i++){const v=index.items[i].vector;if(v.length!==dimensions)throw Error('Vector dimensions');const scale=127/Math.max(...v.map(Math.abs));let sum=0;for(let j=0;j<dimensions;j++){const q=Math.round(v[j]*scale);vectors[i*dimensions+j]=q;sum+=q*q;}norms[i]=Math.sqrt(sum);}
fs.writeFileSync(root+'/vectors.bin',vectors);fs.writeFileSync(root+'/norms.bin',new Uint8Array(norms.buffer));fs.writeFileSync(root+'/items.json',JSON.stringify(index.items.map(({id,image})=>({id,image}))));
const manifest={version:1,model:index.model,dimensions,count:n,updated:index.updated,modelBytes:bytes.length,chunks,downloadBytes:bytes.length+fs.statSync(root+'/ort-wasm-simd-threaded.wasm').size+vectors.byteLength+norms.byteLength+fs.statSync(root+'/items.json').size};
fs.writeFileSync(root+'/manifest.json',JSON.stringify(manifest));fs.writeFileSync('src/content/visual-status.json',JSON.stringify({state:'complete',count:n,discovered:n,updated:index.updated,downloadBytes:manifest.downloadBytes}));
fs.copyFileSync('node_modules/@huggingface/transformers/LICENSE',root+'/TRANSFORMERS-LICENSE.txt');
console.log(JSON.stringify({count:n,assets:root,downloadMB:Math.ceil(manifest.downloadBytes/1e6),modelChunks:chunks.length}));
