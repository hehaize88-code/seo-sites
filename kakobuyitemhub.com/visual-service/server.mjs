import http from 'node:http';import fs from 'node:fs/promises';import * as cheerio from 'cheerio';import {embed,cosine} from './embedding.mjs';
let busy=false;const attempts=new Map();const MAX=5*1024*1024;
const send=(res,status,data)=>{res.writeHead(status,{'content-type':'application/json; charset=utf-8','cache-control':'no-store','x-content-type-options':'nosniff'});res.end(JSON.stringify(data));};
http.createServer(async(req,res)=>{
 if(req.url==='/api/visual/status'&&req.method==='GET'){try{const index=JSON.parse(await fs.readFile('.visual-index/index.json','utf8'));let progress={};try{progress=JSON.parse(await fs.readFile('.visual-index/progress.json','utf8'));}catch{}return send(res,200,{...progress,count:index.items.length,updated:index.updated});}catch{return send(res,503,{error:'index_unavailable'});}}
 if(req.url!=='/api/visual'||req.method!=='POST')return send(res,404,{error:'not_found'});
 const origin=req.headers.origin;if(origin){try{const host=new URL(origin).hostname;if(!['127.0.0.1','localhost','receiving-mysql-styles-clarke.trycloudflare.com'].includes(host))return send(res,403,{error:'origin'});}catch{return send(res,403,{error:'origin'});}}
 if(!/^image\/(jpeg|png|webp)$/.test(req.headers['content-type']||''))return send(res,415,{error:'invalid_image'});
 if(Number(req.headers['content-length']||0)>MAX)return send(res,413,{error:'too_large'});
 const ip=String(req.headers['x-preview-client']||req.socket.remoteAddress);const now=Date.now();for(const [key,val] of attempts)if(now-val.start>60000)attempts.delete(key);let attempt=attempts.get(ip)||{start:now,count:0};attempt.count++;attempts.set(ip,attempt);if(attempt.count>10||attempts.size>1000)return send(res,429,{error:'rate_limited'});
 if(busy)return send(res,429,{error:'busy'});busy=true;
 try{
 const chunks=[];let size=0;for await(const chunk of req){size+=chunk.length;if(size>MAX){send(res,413,{error:'too_large'});return;}chunks.push(chunk);}if(!size)return send(res,400,{error:'invalid_image'});
 const index=JSON.parse(await fs.readFile('.visual-index/index.json','utf8'));if(!index.items.length)return send(res,503,{error:'index_unavailable'});
 let vector;try{vector=await embed(Buffer.concat(chunks));}catch{return send(res,400,{error:'invalid_image'});}
 const nearest=index.items.map(x=>({...x,similarity:cosine(vector,x.vector)})).sort((a,b)=>b.similarity-a.similarity).filter(x=>x.similarity>=.5).slice(0,8);
 const hits=[];for(let offset=0;offset<nearest.length;offset+=4){const batch=await Promise.all(nearest.slice(offset,offset+4).map(async item=>{try{const r=await fetch('https://cnfanshm.com/AllProducts/'+item.id+'.html',{signal:AbortSignal.timeout(12000)});if(!r.ok)return null;const $=cheerio.load(await r.text());const root=$('.product-detail');const title=root.find('.product-title').text().trim();if(!title)return null;return {id:item.id,image:item.image,title,price:root.find('.product-price').first().text().trim()};}catch{return null;}}));hits.push(...batch.filter(Boolean));}
 if(nearest.length&&!hits.length)return send(res,502,{error:'source_unavailable'});
 send(res,200,{hits,indexed:index.items.length,updated:index.updated,partial:hits.length<nearest.length});
 }catch{return send(res,503,{error:'unavailable'});}finally{busy=false;}
}).listen(4323,'127.0.0.1',()=>console.log('Visual search ready: 4323. Uploaded images are not stored.'));
