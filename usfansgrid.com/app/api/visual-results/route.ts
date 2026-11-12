import {getProduct,Product} from '../../../lib/catalog';
export async function POST(request:Request){
 let data:any;try{data=await request.json();}catch{return Response.json({error:'invalid-request'},{status:400});}
 if(!data||!Array.isArray(data.matches)||data.matches.length>12)return Response.json({error:'invalid-request'},{status:400});
 const matches=data.matches.filter((m:any)=>m&&/^\d{1,8}$/.test(m.id)&&Number.isSafeInteger(m.photo)&&m.photo>=0&&m.photo<2000&&/^[a-f0-9]{12}$/.test(m.imageKey));
 const products:Product[]=[];
 for(let start=0;start<matches.length;start+=4){await Promise.all(matches.slice(start,start+4).map(async(m:any)=>{const {product}=await getProduct(m.id);if(!product)return;const photo=product.images?.[m.photo];if(!photo)return;const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(photo))),n=>n.toString(16).padStart(2,'0')).join('').slice(0,12);if(hash!==m.imageKey)return;products.push({...product,image:photo,matchPhoto:m.photo});}));}
 return Response.json({products,unavailable:matches.length-products.length},{headers:{'Cache-Control':'no-store'}});
}
