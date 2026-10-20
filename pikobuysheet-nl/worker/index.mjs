import {apiResponse} from '../src/lib/source.mjs';
import assets from '../.astro-out/asset-map.mjs';
export default {async fetch(request){
  const url=new URL(request.url);if(!['GET','HEAD'].includes(request.method))return new Response('Method not allowed',{status:405,headers:{Allow:'GET, HEAD'}});
  // Keep the production host canonical without losing language paths or filters.
  if(url.hostname==='www.pikobuysheet.nl'||(url.hostname==='pikobuysheet.nl'&&url.protocol!=='https:')){
    url.hostname='pikobuysheet.nl';url.protocol='https:';return Response.redirect(url,301);
  }
  if(['/api/catalog','/api/product'].includes(url.pathname.replace(/\/$/,'')))return apiResponse(url);
  let path=url.pathname;const file=assets[path]||assets[path+'index.html']||assets[path+'/index.html'];
  if(!file)return new Response('Page not found',{status:404,headers:{'Content-Type':'text/plain; charset=utf-8'}});
  if(!path.endsWith('/')&&assets[path+'/index.html']){url.pathname+='/';return Response.redirect(url,308);}
  const headers={'Content-Type':file.type,'Cache-Control':path.startsWith('/_astro/')?'public,max-age=31536000,immutable':'public,max-age=60','X-Content-Type-Options':'nosniff','Referrer-Policy':'strict-origin-when-cross-origin'};
  if(url.hostname!=='pikobuysheet.nl'||url.search)headers['X-Robots-Tag']='noindex, follow';
  if(request.method==='HEAD')return new Response(null,{headers});
  const bytes=file.binary?Uint8Array.from(atob(file.data),c=>c.charCodeAt(0)):file.data;
  // Compress at build time to keep hundreds of localized HTML pages economical.
  // Decode before responding; the hosting layer negotiates wire compression.
  const body=file.gzip?new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip')):bytes;
  return new Response(body,{headers});
}};
