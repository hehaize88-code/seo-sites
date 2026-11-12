/// <reference lib="webworker" />
import {pipeline,env,RawImage} from '@huggingface/transformers';
import {nearest,type VisualIndex} from './matching';
const scope=self as unknown as DedicatedWorkerGlobalScope;
env.allowRemoteModels=false;env.allowLocalModels=true;
env.localModelPath=new URL('/visual-models/',scope.location.origin).href;
env.backends.onnx.wasm!.numThreads=1;
env.backends.onnx.wasm!.proxy=false;
env.backends.onnx.wasm!.wasmPaths=new URL('/visual-runtime/',scope.location.origin).href;
let indexPromise:Promise<{index:VisualIndex;values:Int8Array}>|undefined;
let modelPromise:Promise<any>|undefined;
async function prepareIndex(){
 if(!indexPromise)indexPromise=(async()=>{
  const index=await fetch('/visual/index.json',{cache:'no-cache'}).then(r=>{if(!r.ok)throw Error('index-unavailable');return r.json() as Promise<VisualIndex>});
  if(!/^vectors-[a-f0-9]{12}\.bin$/.test(index.vectors))throw Error('index-invalid');
  const binary=await fetch('/visual/'+index.vectors).then(r=>{if(!r.ok)throw Error('index-unavailable');return r.arrayBuffer()});
  const values=new Int8Array(binary);
  if(index.version!==2||values.length!==index.ids.length*index.dimension)throw Error('index-invalid');
  return {index,values};
 })().catch(e=>{indexPromise=undefined;throw e;});
 return indexPromise;
}
async function prepareModel(){
 if(!modelPromise)modelPromise=pipeline('image-feature-extraction','dinov2-small',{dtype:'q8',device:'wasm',progress_callback:(p:any)=>{if(p.status==='progress'&&p.file?.endsWith('.onnx'))scope.postMessage({type:'progress',value:Math.round(p.progress)});}}).catch(e=>{modelPromise=undefined;throw e;});
 return modelPromise;
}
scope.onmessage=async(event:MessageEvent<{image?:ArrayBuffer;exampleId?:string;imageUrl?:string}>)=>{
 try{
  const {index,values}=await prepareIndex();let embedding:Float32Array;
  if(event.data.exampleId){
   // Catalog photos already have descriptors. Reuse them for the same cosine search.
   
   const digest=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(event.data.imageUrl||''));
   const key=Array.from(new Uint8Array(digest),v=>v.toString(16).padStart(2,'0')).join('').slice(0,12);
   const position=index.imageKeys.indexOf(key);if(position<0||!index.refs[position]?.some(r=>r.id===event.data.exampleId))throw Error('index-stale');
   scope.postMessage({type:'matching'});embedding=Float32Array.from(values.slice(position*384,(position+1)*384));
  }else if(event.data.image){
   scope.postMessage({type:'loading'});const extractor=await prepareModel();scope.postMessage({type:'matching'});
   const image=await RawImage.fromBlob(new Blob([event.data.image],{type:'image/jpeg'}));const output=await extractor(image);embedding=Float32Array.from(output.data.slice(0,384));
  }else throw Error('image-invalid');
  scope.postMessage({type:'results',matches:nearest(embedding,values,index),indexedCount:index.indexedCount,createdAt:index.createdAt});
 }catch(error){console.error('Image search failed',error instanceof Error?error.message:'unknown');scope.postMessage({type:'error',code:error instanceof Error?error.message:'search-unavailable'});}
};
