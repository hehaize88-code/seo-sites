import {getProduct} from '../../../../lib/catalog';
export async function GET(_:Request,{params}:{params:Promise<{id:string}>}){const {id}=await params;const data=await getProduct(id);return Response.json(data,{status:data.product?200:data.error==='not-found'?404:503,headers:{'Cache-Control':'public, max-age=60'}});}
