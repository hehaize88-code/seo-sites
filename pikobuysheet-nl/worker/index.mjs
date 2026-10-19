import {apiResponse} from '../src/lib/source.mjs';
import assets from '../.astro-out/asset-map.mjs';
export default {async fetch(request){
  const url=new URL(request.url);if(!['GET','HEAD'].includes(request.method))return new Response('Method not allowed',{status:405,headers:{Allow:'GET, HEAD'}});
  if(['/api/catalog','/api/product'].includes(url.pathname.replace(/\/$/,'')))return apiResponse(url);
  let path=url.pathname;const file=assets[path]||assets[path+'index.html']||assets[path+'/index.html'];
  if(!file)return new Response('Page not found',{status:404,headers:{'Content-Type':'text/plain; charset=utf-8'}});
  if(!path.endsWith('/')&&assets[path+'/index.html']){url.pathname+='/';return Response.redirect(url,308);}
  const headers={'Content-Type':file.type,'Cache-Control':path.startsWith('/_astro/')?'public,max-age=31536000,immutable':'public,max-age=60','X-Content-Type-Options':'nosniff','Referrer-Policy':'strict-origin-when-cross-origin'};
  if(url.hostname!=='pikobuysheet.nl'||url.search)headers['X-Robots-Tag']='noindex, follow';
  const bytes=file.binary?Uint8Array.from(atob(file.data),c=>c.charCodeAt(0)):file.data;
  return new Response(request.method==='HEAD'?null:bytes,{headers});
}};
