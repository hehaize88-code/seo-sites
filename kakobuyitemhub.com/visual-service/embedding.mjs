import {ProxyAgent,setGlobalDispatcher} from 'undici';
if(process.env.HTTPS_PROXY)setGlobalDispatcher(new ProxyAgent(process.env.HTTPS_PROXY));
import {AutoProcessor,CLIPVisionModelWithProjection,RawImage,env} from '@huggingface/transformers';
import sharp from 'sharp';
env.cacheDir=new URL('../.visual-cache/',import.meta.url).pathname.replace(/^\/([A-Za-z]:)/,'$1');
let ready;
export async function embed(bytes){
 ready??=Promise.all([AutoProcessor.from_pretrained('Xenova/clip-vit-base-patch32'),CLIPVisionModelWithProjection.from_pretrained('Xenova/clip-vit-base-patch32',{dtype:'q8',device:'cpu',session_options:{intraOpNumThreads:2}})]);
 const [processor,model]=await ready;
 const {data,info}=await sharp(bytes,{limitInputPixels:25000000}).rotate().resize(512,512,{fit:'inside',withoutEnlargement:true}).flatten({background:'#fff'}).removeAlpha().raw().toBuffer({resolveWithObject:true});
 const inputs=await processor(new RawImage(new Uint8ClampedArray(data),info.width,info.height,info.channels));
 const result=await model(inputs);const vector=Array.from(result.image_embeds.data);const norm=Math.hypot(...vector);return vector.map(x=>x/norm);
}
export const cosine=(a,b)=>a.reduce((sum,x,i)=>sum+x*b[i],0);

