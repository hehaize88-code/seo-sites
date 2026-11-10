import {defineMiddleware} from 'astro:middleware';
export const onRequest=defineMiddleware(async(context,next)=>{
 const url=new URL(context.request.url);
 if(url.hostname==='www.kakobuyitemhub.com'||(url.hostname==='kakobuyitemhub.com'&&url.protocol!=='https:')){url.hostname='kakobuyitemhub.com';url.protocol='https:';return Response.redirect(url.href,301);}
 const response=await next();
 if(url.hostname!=='kakobuyitemhub.com')response.headers.set('X-Robots-Tag','noindex, nofollow');
 response.headers.set('X-Content-Type-Options','nosniff');return response;
});
