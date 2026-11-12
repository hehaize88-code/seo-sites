import {getExchange} from '../../../lib/exchange';
export async function GET(){const data=await getExchange();return Response.json(data,{headers:{'Cache-Control':data.status==='current'?'public, max-age=1800':'no-store'}});}
