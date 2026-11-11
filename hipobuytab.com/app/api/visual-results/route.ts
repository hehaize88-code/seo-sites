import {getProduct} from '@/lib/catalog';
export async function GET(request:Request){
 const ids=(new URL(request.url).searchParams.get('ids')||'').split(',');
 if(!ids.length||ids.length>12||ids.some(id=>!/^\d{1,8}$/.test(id)))return Response.json({error:'invalid-ids'},{status:400});
 const unique=[...new Set(ids)];const results=[];
 // Bound upstream concurrency; this adapter stores no catalog or uploaded images.
 for(let i=0;i<unique.length;i+=4)results.push(...await Promise.all(unique.slice(i,i+4).map(id=>getProduct(id,{legacyRate:false}))));
 const products=results.map(r=>r.product).filter(Boolean);
 return Response.json({products,unavailable:results.filter(r=>!r.product).length},{headers:{'Cache-Control':'public, max-age=120'}});
}
