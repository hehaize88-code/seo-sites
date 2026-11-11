import fs from 'node:fs/promises';
import path from 'node:path';
const revision='c2bb04a51fab207c420665f1946016107bffc701';
const files=['config.json','preprocessor_config.json','onnx/model_quantized.onnx'];
const destination=path.resolve('public/visual-models/dinov2-small');
for(const file of files){const target=path.join(destination,file);await fs.mkdir(path.dirname(target),{recursive:true});try{if((await fs.stat(target)).size>100){console.log('Available:',file);continue;}}catch{}
 const r=await fetch(`https://huggingface.co/Xenova/dinov2-small/resolve/${revision}/${file}`,{signal:AbortSignal.timeout(180000)});if(!r.ok)throw Error(`${file}: ${r.status}`);const bytes=Buffer.from(await r.arrayBuffer());await fs.writeFile(target,bytes);console.log(file,bytes.length);
}
await fs.mkdir('public/visual-runtime',{recursive:true});
for(const file of ['ort-wasm-simd-threaded.jsep.mjs','ort-wasm-simd-threaded.jsep.wasm']){
 try{await fs.copyFile('node_modules/onnxruntime-web/dist/'+file,'public/visual-runtime/'+file);console.log('Runtime:',file);}catch{console.log('Run again after dependency installation for:',file);}
}
