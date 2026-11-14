const ORIGIN='https://cnfanshm.com';
const decode=s=>s.replace(/&amp;/g,'&').replace(/&quot;/g,'"').replace(/&#39;|&apos;/g,"'").replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&#(\d+);/g,(_,n)=>String.fromCodePoint(+n));
const clean=s=>decode((s||'').replace(/<[^>]*>/g,'').trim());
const match=(s,re)=>s.match(re)?.[1]||'';
export function parseList(html){
 const products=[];const seen=new Set();
 for(const block of html.split(/<div\s+class="product-card[^\"]*"/).slice(1)){
  const id=match(block,/href="\/AllProducts\/(\d+)\.html/);if(!id||seen.has(id))continue;seen.add(id);
  const name=clean(match(block,/<h3[^>]*>([\s\S]*?)<\/h3>/));
  const image=match(block,/data-src="([^\"]+)"/);
  const price=Number(clean(match(block,/<div class="product-price">([\s\S]*?)<\/div>/)));
  if(name&&image)products.push({id,name,image,price:Number.isFinite(price)?price:null});
 }
 const pagination=match(html,/<div class="pagination">([\s\S]*?)<\/div>/);
 const links=[...pagination.matchAll(/<a\s+href="([^\"]+)"[^>]*>([\s\S]*?)<\/a>/g)].map(m=>({path:decode(m[1]),label:clean(m[2])}));
 return {products,next:links.find(x=>x.label.includes('下一'))?.path||null,previous:links.find(x=>x.label.includes('上一'))?.path||null};
}
export function parseDetail(html,id){
 const name=clean(match(html,/<h1 class="product-title">([\s\S]*?)<\/h1>/));
 if(!name)throw Error('Product unavailable');
 const gallery=match(html,/<div class="product-gallery">([\s\S]*?)<div class="product-info">/);
 const description=match(html,/<div class="product-description">([\s\S]*?)<div class="(?:related|recommend)/)||'';
 const images=[...new Set([...(gallery+description).matchAll(/data-src="([^\"]+)"/g)].map(m=>decode(m[1])))];
 const original=decode(match(html,/href="(https:\/\/weidian\.com\/item\.html\?[^\"]+)"/));
 const purchase=decode(match(html,/href="(https:\/\/www\.lovegobuy\.com\/product\?[^\"]+)"/));
 const agents=[...html.matchAll(/<a(?=[^>]*class="platform-option")[^>]*href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/g)].map(m=>({url:decode(m[1]),name:clean(match(m[2],/<span[^>]*>([\s\S]*?)<\/span>/)).replace(/\s*Link$/i,'')})).filter(a=>/^https?:\/\//.test(a.url)&&a.name);
 return {id,name,images,agents,styles:[],qc:[],price:Number(clean(match(html,/<div class="product-price">([\s\S]*?)<\/div>/)))||null,original,purchase,productId:original?new URL(original).searchParams.get('itemID'):null};
}
function validPath(p){return p==='/'||/^\/(?:AllProducts|shoes|hoodies-sweaters|t-shirts|jackets|pants-shorts|headwear|accessories|short-sets|electronics|other-stuff|jersey)\/(?:list_\d+_\d+\/)?$/.test(p)||/^\/AllProducts\/\d+\.html$/.test(p)||/^\/(?:search\.html|index\.php)\?/.test(p);}
async function upstream(path,ctx){
 const url=new URL(path,ORIGIN);if(url.origin!==ORIGIN)throw Error('Invalid source');
 const res=await fetch(url.href,{headers:{'User-Agent':'LovegobuyCatalogPreview/1.0','Accept':'text/html,image/*'},signal:AbortSignal.timeout(25000)});
 if(!res.ok)throw Error('Upstream '+res.status);
 const headers=new Headers(res.headers);headers.set('Cache-Control','public,max-age=300');
 const copy=new Response(res.body,{status:res.status,headers});return copy;
}
export default {async fetch(request,env,ctx){
 const url=new URL(request.url);const headers={'X-Content-Type-Options':'nosniff','X-Robots-Tag':'noindex, nofollow','Referrer-Policy':'no-referrer'};
 if(PACKED_ASSETS[url.pathname]){const [type,b64]=PACKED_ASSETS[url.pathname];return new Response(Uint8Array.from(atob(b64),c=>c.charCodeAt(0)),{headers:{...headers,'Content-Type':type,'Cache-Control':'public,max-age=86400'}});}
 if(url.pathname==='/search-worker.js')return new Response(SEARCH_WORKER,{headers:{...headers,'Content-Type':'text/javascript'}});
 if(url.pathname==='/robots.txt')return new Response('User-agent: *\nDisallow: /',{headers:{'Content-Type':'text/plain'}});
 if(url.pathname==='/app.js')return new Response(APP_JS,{headers:{...headers,'Content-Type':'text/javascript;charset=utf-8'}});
 if(url.pathname==='/style.css')return new Response(STYLE_CSS,{headers:{...headers,'Content-Type':'text/css;charset=utf-8'}});
 if(url.pathname==='/api/catalog'||url.pathname==='/api/product'){
  try{
   let path=url.searchParams.get('path')||'/AllProducts/';
   if(url.pathname==='/api/product'){const id=url.searchParams.get('id')||'';if(!/^\d{1,12}$/.test(id))return new Response('Invalid ID',{status:400});path='/AllProducts/'+id+'.html';}
   if(!validPath(path))return new Response('Invalid path',{status:400});
   const html=await(await upstream(path,ctx)).text();
   if(!html.includes('product-card')&&!html.includes('product-title')&&!html.includes('search-keyword'))throw Error('Unexpected response');
   const data=url.pathname==='/api/product'?parseDetail(html,url.searchParams.get('id')):parseList(html);
   return Response.json(data,{headers});
  }catch(e){console.error('catalog-source-error',e.message);return Response.json({error:'The product source is temporarily unavailable. Please retry.'},{status:502,headers});}
 }
 if(url.pathname==='/image'){
  const p=url.searchParams.get('path')||'';if(!/^\/uploads\/[a-zA-Z0-9_./-]+\.(?:webp|png|jpg|jpeg|gif)$/i.test(p)||p.includes('..'))return new Response('Invalid image',{status:400});
  try{const r=await upstream(p,ctx);return new Response(r.body,{headers:{...headers,'Content-Type':r.headers.get('Content-Type')||'image/jpeg','Cache-Control':'public,max-age=86400'}});}catch{return new Response('Image unavailable',{status:502});}
 }
 if(url.pathname==='/favicon.ico')return Response.redirect('https://www.lovegobuy.com/favicon.ico',302);
 return new Response(HTML,{headers:{...headers,'Content-Type':'text/html;charset=utf-8','Content-Security-Policy':"default-src 'self'; img-src 'self' https: data: blob:; style-src 'self'; script-src 'self'; connect-src 'self' https://open.er-api.com; worker-src 'self'; base-uri 'none'; frame-ancestors 'none'"}});
}};
