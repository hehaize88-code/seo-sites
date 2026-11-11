import handler from "vinext/server/fetch-handler";
export default {
 async fetch(request:Request,env:Cloudflare.Env,ctx:ExecutionContext){
  const url=new URL(request.url);
  if(url.hostname==='www.hipobuytab.com'||(url.hostname==='hipobuytab.com'&&url.protocol!=='https:')){url.hostname='hipobuytab.com';url.protocol='https:';return Response.redirect(url.toString(),308)}
  if(url.pathname==='/en'||url.pathname==='/en/'){url.pathname='/';return Response.redirect(url.toString(),308)}
  if(url.pathname.length>1&&url.pathname.endsWith('/')){url.pathname=url.pathname.replace(/\/+$/,'');return Response.redirect(url.toString(),308)}
  if(/^\/sitemap(?:-[a-z-]+)?\.xml$/.test(url.pathname))return env.ASSETS.fetch(request);
  if(/^\/(?:_next|assets|visual|visual-models|visual-runtime|brands)\//.test(url.pathname))return env.ASSETS.fetch(request);
  return handler.fetch(request,env,ctx);
 }
};
