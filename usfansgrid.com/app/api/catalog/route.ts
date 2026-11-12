import {getCatalog} from '../../../lib/catalog';
export async function GET(request:Request){const q=new URL(request.url).searchParams;return Response.json(await getCatalog({page:Number(q.get('page'))||1,q:q.get('q')||'',category:q.get('category')||'all',sort:q.get('sort')||'new'}),{headers:{'Cache-Control':'public, max-age=60'}});}
