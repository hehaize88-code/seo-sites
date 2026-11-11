import {getProduct} from '@/lib/catalog';
export async function GET(_request:Request,{params}:{params:Promise<{id:string}>}){const {id}=await params;const result=await getProduct(id);return Response.json(result,{status:result.product?200:result.error==='not-found'?404:502,headers:{'Cache-Control':'no-store','X-Robots-Tag':'noindex'}});}
