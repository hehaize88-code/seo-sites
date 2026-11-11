import {getCatalog} from '@/lib/catalog';
export async function GET(request:Request){const p=new URL(request.url).searchParams;return Response.json(await getCatalog({q:p.get('q')||'',category:Number(p.get('category'))||1,sort:p.get('sort')||'new',page:Number(p.get('page'))||1}),{headers:{'Cache-Control':'no-store','X-Robots-Tag':'noindex'}});}
