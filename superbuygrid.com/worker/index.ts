import handler from 'vinext/server/fetch-handler';
export default {
 async fetch(request:Request,env:any,ctx:ExecutionContext){
  const u=new URL(request.url);
  if(u.hostname==='www.superbuygrid.com'||(u.hostname==='superbuygrid.com'&&u.protocol!=='https:')){u.hostname='superbuygrid.com';u.protocol='https:';return Response.redirect(u.href,308)}
  if(/\.(?:js|css|svg|png|json|xml|txt|woff2?|ico)$/.test(u.pathname))return env.ASSETS.fetch(request);
  return handler.fetch(request,env,ctx);
 }
};
