import mediaRoles from './media-roles.json';
const BASE='https://cnfanshm.com';
const cache=new Map<string,{at:number,value:string}>();
const pending=new Map<string,Promise<string>>();
export const categories=['shoes','hoodies-sweaters','t-shirts','jackets','pants-shorts','headwear','accessories','short-sets','electronics','other-stuff','jersey'];
export async function source(path:string):Promise<string>{
 const hit=cache.get(path);if(hit&&Date.now()-hit.at<300000)return hit.value;
 if(pending.has(path))return pending.get(path)!;
 const task=(async()=>{const r=await fetch(BASE+path,{headers:{'User-Agent':'SuperbuyGridCatalog/1.0','Accept':'text/html,application/xml'},signal:AbortSignal.timeout(18000)});if(!r.ok)throw Error('Source unavailable ('+r.status+')');const value=await r.text();if(value.includes('cf-chl-')||value.includes('<title>Attention Required!'))throw Error('Source unavailable');if(cache.size>180)cache.delete(cache.keys().next().value!);cache.set(path,{at:Date.now(),value});return value;})();
 pending.set(path,task);try{return await task}finally{pending.delete(path)}
}
export function clean(s:string){return s.replace(/<[^>]+>/g,'').replace(/&amp;/g,'&').replace(/&quot;/g,'"').replace(/&#39;|&apos;/g,"'").replace(/&nbsp;/g,' ').trim()}
export function cards(s:string){return s.split(/<div class="product-card glass-card"/).slice(1).map(b=>{const id=b.match(/href="\/AllProducts\/(\d+)\.html"/)?.[1];const name=b.match(/<h3[^>]*>([\s\S]*?)<\/h3>/)?.[1];const img=b.match(/data-src="([^"]+)"/)?.[1];const price=b.match(/class="product-price">\s*([\d.]+)/)?.[1];return {id,name:clean(name||''),image:img?new URL(img,BASE).href:'',price:price?+price:null}}).filter(p=>p.id)}
export async function product(id:string){if(!/^\d{1,10}$/.test(id))throw Error('Invalid ID');const s=await source('/AllProducts/'+id+'.html');const block=s.split('<div class="product-detail">')[1]?.split('<section class="product-list">')[0];if(!block)throw Error('Product unavailable');const name=clean(block.match(/<h1[^>]*>([\s\S]*?)<\/h1>/)?.[1]||'');const images=[...new Set([...block.matchAll(/(?:data-src|src)="([^"<>]+)"/g)].map(m=>m[1]).filter(x=>x.includes('/uploads/')).map(x=>new URL(x,BASE).href))];const raw=[...block.matchAll(/href="([^"]+)"/g)].map(m=>clean(m[1])).find(x=>/^https?:\/\/(?:www\.)?(?:weidian\.com|item\.taobao\.com|detail\.1688\.com|detail\.tmall\.com)\//.test(x))||'';const agents=[...s.matchAll(/<a\s+[^>]*href="([^"]+)"[^>]*class="platform-option"[^>]*>([\s\S]*?)<\/a>/g)].map(m=>({url:clean(m[1]),name:clean(m[2].match(/alt="([^"]+)"/)?.[1]||m[2]).replace(/ Link$/i,'')})).map(a=>({...a,name:a.url.includes('bbdbuy.com/')?'BBDBuy':a.url.includes('basetao.com/')?'Basetao':a.url.includes('joyagoo.com/')?'Joyagoo':a.name})).filter(a=>/^https:\/\//.test(a.url)&&a.name&&a.name.toLowerCase()!=='superbuy');
 const media=images.map(src=>({src,kind:(mediaRoles as Record<string,string>)[src]||'detail',styleUrl:''}));
 // SKU URLs are accepted only when explicitly attached to that image in the source.
 for(const m of block.matchAll(/<a[^>]*href="(https:\/\/weidian\.com\/[^"]+)"[^>]*>([\s\S]*?)<\/a>/g)){const im=m[2].match(/(?:data-src|src)="([^"]+)"/)?.[1];if(im){const found=media.find(x=>x.src===new URL(im,BASE).href);if(found&&/[?&](?:skuId|sku_id)=/.test(clean(m[1])))found.styleUrl=clean(m[1]);}}
 return {id,name,images,media,agents,image:images[0]||'',price:Number(block.match(/class="product-price">\s*([\d.]+)/)?.[1])||null,original:raw,itemId:block.match(/class="product-id">\s*ID:\s*(\d+)/)?.[1]||'',buy:raw?'https://www.superbuy.com/en/page/buy/?url='+encodeURIComponent(raw):''}}
export async function catalog({category='',page=1,q='',home=false}:{category?:string,page?:number,q?:string,home?:boolean}){
 if(home){const items=cards(await source('/'));return {items:items.slice(0,12),next:true,page:1,total:null}}
 if(category&&!categories.includes(category))throw Error('Invalid category');
 let path=q?'/search.html?channelid=2&keywords='+encodeURIComponent(q):category?'/'+category+'/':'/AllProducts/';
 // Follow the actual source pagination URLs; never manufacture source category IDs.
 let html=await source(path);const sourcePage=Math.ceil(page/3);
 if(sourcePage>1){const next=html.match(/<a href="([^"]+)"[^>]*>下一页<\/a>/)?.[1];if(!next)return {items:[],next:false,page,total:null};const u=new URL(clean(next),BASE);if(u.origin!==BASE)throw Error('Invalid source pagination');if(u.searchParams.has('page'))u.searchParams.set('page',String(sourcePage));else u.pathname=u.pathname.replace(/(list_\d+_)2(\/|\.html)/,'$1'+sourcePage+'$2');html=await source(u.pathname+u.search)}
 const items=cards(html);const offset=((page-1)%3)*20;return {items:items.slice(offset,offset+20),next:items.length>offset+20||Boolean(html.match(/<a href="([^"]+)"[^>]*>下一页<\/a>/)),page,total:null};
}
