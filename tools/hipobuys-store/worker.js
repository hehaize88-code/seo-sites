const SITE='https://hipobuys.store';
const PAGES=new Set(__PAGES__);
const ASSETS=new Set(__ASSETS__);
const ENGLISH_SLUGS=new Set(__SLUGS__);
const STORE_HOSTS=new Set(['cnfanssp.com','www.cnfanssp.com','cnfanshp.com','www.cnfanshp.com']);
const SECURITY_HEADERS={
  'X-Content-Type-Options':'nosniff',
  'Referrer-Policy':'strict-origin-when-cross-origin',
  'Permissions-Policy':'camera=(), microphone=(), geolocation=()',
  'X-Frame-Options':'SAMEORIGIN',
  'Strict-Transport-Security':'max-age=31536000; includeSubDomains',
  'Content-Security-Policy':"default-src 'self'; img-src 'self' data: https://cnfanssp.com https://cnfanshp.com https://www.googletagmanager.com https://*.google-analytics.com; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com; connect-src 'self' https://www.googletagmanager.com https://*.google-analytics.com https://*.analytics.google.com https://*.google.com; form-action 'self' https://cnfanshp.com; base-uri 'self'; frame-ancestors 'self'"
};
function addSecurity(headers){for(const [key,value] of Object.entries(SECURITY_HEADERS))headers.set(key,value);}
function redirect(url){return new Response(null,{status:301,headers:{Location:url.toString(),'Cache-Control':'public, max-age=300'}});}
function canonicalPath(pathname){
  let path=pathname.replace(/\/{2,}/g,'/');
  if(path.endsWith('/index.html'))path=path.slice(0,-10);
  else if(path.endsWith('.html'))path=path.slice(0,-5);
  if(path==='/en'||path==='/en/')return '/';
  const english=path.match(/^\/en\/([^/]+)\/?$/);
  if(english&&(ENGLISH_SLUGS.has(english[1])||english[1]==='articles'))return '/'+english[1];
  if(PAGES.has(path))return path;
  if(path.endsWith('/')&&PAGES.has(path.slice(0,-1)))return path.slice(0,-1);
  if(PAGES.has(path+'/'))return path+'/';
  return path;
}
function rewriteHref(value,current){
  if(!value||/^(#|mailto:|tel:|javascript:)/i.test(value))return value;
  let u;try{u=new URL(value,current);}catch{return value;}
  if(['hipobuys.store','www.hipobuys.store'].includes(u.hostname))return canonicalPath(u.pathname)+u.search+u.hash;
  if(STORE_HOSTS.has(u.hostname)){u.hostname='cnfanshp.com';u.protocol='https:';u.port='';return u.toString();}
  return value; // Official references remain external, with their actual destination intact.
}
async function notFound(request,env){
  const res=await env.ASSETS.fetch(new URL('/404',request.url));
  const headers=new Headers(res.headers);addSecurity(headers);headers.set('X-Robots-Tag','noindex, nofollow');headers.set('Cache-Control','public, max-age=60');
  return new Response(res.body,{status:404,headers});
}
export default {async fetch(request,env){
  const u=new URL(request.url),path=canonicalPath(u.pathname);
  if(u.hostname==='www.hipobuys.store'||path!==u.pathname){u.hostname='hipobuys.store';u.protocol='https:';u.pathname=path;return redirect(u);}
  if(!PAGES.has(path)&&!ASSETS.has(path))return notFound(request,env);
  const response=await env.ASSETS.fetch(request);
  if(response.status===404)return notFound(request,env);
  const headers=new Headers(response.headers);addSecurity(headers);
  if(!headers.get('content-type')?.includes('text/html')||response.status!==200){
    headers.set('Cache-Control',path.endsWith('.xml')||path==='/robots.txt'?'public, max-age=300':/\/assets\/(editorial|site)-[a-f0-9]+\./.test(path)?'public, max-age=31536000, immutable':'public, max-age=3600');
    return new Response(response.body,{status:response.status,headers});
  }
  headers.set('Cache-Control','public, max-age=0, s-maxage=300, stale-while-revalidate=60');
  return new HTMLRewriter()
    .on('link[rel="canonical"]',{element(e){e.setAttribute('href',SITE+path);}})
    .on('meta[property="og:url"]',{element(e){e.setAttribute('content',SITE+path);}})
    .on('a[href]',{element(e){const value=e.getAttribute('href'),next=rewriteHref(value,u);if(next!==value)e.setAttribute('href',next);if(next&&next.startsWith('https://cnfanshp.com/')){e.setAttribute('target','_blank');e.setAttribute('rel','nofollow sponsored noopener');}}})
    .on('form[action]',{element(e){e.setAttribute('action',rewriteHref(e.getAttribute('action'),u));}})
    .transform(new Response(response.body,{status:response.status,headers}));
}};
