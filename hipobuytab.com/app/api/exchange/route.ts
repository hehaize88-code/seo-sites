import {getExchange} from '@/lib/exchange';
export async function GET(){const data=await getExchange();return Response.json(data,{status:data.status==='current'?200:503,headers:{'Cache-Control':data.status==='current'?'public, max-age=3600':'no-store','X-Robots-Tag':'noindex'}});}
