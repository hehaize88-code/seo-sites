import {build} from 'esbuild';
// Bundle bare package imports: native module workers do not inherit import maps.
const result=await build({metafile:true,entryPoints:['node_modules/@huggingface/transformers/dist/transformers.web.min.js'],outfile:'public/visual/runtime-v2/transformers.js',bundle:true,format:'esm',platform:'browser',minify:true,alias:{'onnxruntime-web/webgpu':'onnxruntime-web/wasm'},legalComments:'eof'});
const external=Object.values(result.metafile.outputs).flatMap(output=>output.imports).filter(entry=>entry.external&&!/^(?:https?:|data:|blob:|\.?\.?\/)/.test(entry.path));
if(external.length)throw Error('Browser runtime has unresolved package imports: '+external.map(x=>x.path).join(', '));

