import {sourceSearchQuery} from './product-names';
import {parseSourceDetail} from './source-images.mjs';
export type Product={recordId:string;name:string;priceCny:number|null;image:string;images?:string[];itemId?:string;originalUrl?:string;buyUrl?:string;platforms?:{name:string;url:string}[];matchPhoto?:number};
export type Catalog={products:Product[];page:number;hasNext:boolean;error?:string};
export const categories=[{key:'all',id:1},{key:'shoes',id:4},{key:'sweatshirts',id:5},{key:'tshirts',id:6},{key:'jackets',id:7},{key:'pants',id:8},{key:'headwear',id:9},{key:'accessories',id:10},{key:'sets',id:11},{key:'electronics',id:12},{key:'other',id:15},{key:'jerseys',id:13}];
const ORIGIN='https://cnfanshm.com';
// An expiring, process-local request cache only. There is no database or catalogue copy.
const cache=new Map<string,{expires:number;html:string}>();
async function source(path:string){
 const old=cache.get(path);if(old&&old.expires>Date.now())return old.html;
 const r=await fetch(ORIGIN+path,{headers:{Accept:'text/html','User-Agent':'USFansDirectory/1.0'},signal:AbortSignal.timeout(18000)});
 if(!r.ok)throw new Error('Source HTTP '+r.status);const html=await r.text();
 if(cache.size>80)cache.clear();cache.set(path,{html,expires:Date.now()+60000});return html;
}
function decode(s:string){return s.replace(/<[^>]*>/g,'').replace(/&amp;/g,'&').replace(/&quot;/g,'"').replace(/&#0?39;|&apos;/g,"'").replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&nbsp;/g,' ').replace(/&#(\d+);/g,(_,n)=>String.fromCodePoint(Number(n))).trim();}
function attr(s:string,key:string){return decode(s.match(new RegExp('\\b'+key+'=["\\\']([^"\\\']*)["\\\']','i'))?.[1]||'');}
function cls(s:string,name:string){return decode(s.match(new RegExp('<[^>]+class=["\\\'][^"\\\']*\\b'+name+'\\b[^"\\\']*["\\\'][^>]*>([\\s\\S]*?)<\\/','i'))?.[1]||'');}
function imageURL(s:string){try{const u=new URL(s,ORIGIN);return ['cnfanshm.com','www.cnfanshm.com'].includes(u.hostname)&&u.pathname.startsWith('/uploads/')?u.href:'';}catch{return '';}}
function price(s:string){const v=Number(s.replace(/[^0-9.]/g,''));return s&&Number.isFinite(v)?v:null;}
export function parseCatalog(html:string){
 const chunks=html.split(/<div\b(?=[^>]*class=["'][^"']*\bproduct-card\b)[^>]*>/i).slice(1);
 return chunks.map(s=>{const imageTag=s.match(/<img\b[^>]*>/i)?.[0]||'';return {recordId:s.match(/\/AllProducts\/(\d+)\.html/)?.[1]||'',name:cls(s,'product-name')||decode(s.match(/<h3[^>]*>([\s\S]*?)<\/h3>/i)?.[1]||''),priceCny:price(cls(s,'product-price')),image:imageURL(attr(imageTag,'data-src')||attr(imageTag,'src'))};}).filter(p=>p.recordId&&p.name&&p.image);
}
export async function getCatalog(opts:{q?:string;category?:string;sort?:string;page?:number}={}):Promise<Catalog>{
 const page=Math.max(1,Math.min(900,Math.floor(Number(opts.page)||1))),upstreamPage=Math.floor((page-1)/3)+1,offset=((page-1)%3)*20;
 const q=sourceSearchQuery((opts.q||'').trim().slice(0,120));const cat=categories.find(c=>c.key===opts.category)||categories[0];
 const p=new URLSearchParams({m:'home',c:q?'Search':'Lists',a:q?'lists':'index',sort:opts.sort?.startsWith('price')?'price':opts.sort==='popular'?'click':'new',sort_asc:opts.sort==='price-asc'?'asc':'desc',ZXljbXM:'1',page:String(upstreamPage)});
 if(q){p.set('keywords',q);p.set('channelid','2');}else p.set('tid',String(cat.id));
 const searchParams=new URLSearchParams({keywords:q,channelid:'2',page:String(upstreamPage)});
 try{const html=await source(q?'/search.html?'+searchParams:'/index.php?'+p);const all=parseCatalog(html);const pagination=html.split('class="pagination"')[1]?.split('</div>')[0]||'';const hasNext=[...pagination.matchAll(/(?:&amp;|&)page=(\d+)/g)].some(m=>Number(m[1])>upstreamPage);return {products:all.slice(offset,offset+20),hasNext:all.length>offset+20||hasNext,page};}catch(e){console.error('Catalogue fetch:',e instanceof Error?e.message:String(e));return {products:[],hasNext:false,page,error:'source-unavailable'};}
}
export async function getProduct(id:string):Promise<{product:Product|null;error?:string}>{
 if(!/^\d{1,8}$/.test(id))return {product:null,error:'not-found'};
 try{const product=parseSourceDetail(await source('/AllProducts/'+id+'.html'),id);return product?{product}:{product:null,error:'not-found'};
 }catch{return {product:null,error:'source-unavailable'};}
}
