import {product} from '../../../lib/catalog';
export async function GET(req:Request){try{return Response.json(await product(new URL(req.url).searchParams.get('id')||''),{headers:{'Cache-Control':'public, max-age=120'}})}catch{return Response.json({error:'Source product unavailable'},{status:502})}}
