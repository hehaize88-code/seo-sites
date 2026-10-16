// Pre-rendered HTML is the source of truth. Do not inject English copy at runtime.
const LANG_ROOT=/^\/(zh|fr|de|es|it|pl|nl|pt)$/;
const LEGACY='/articles/pikobuy-w2c-qc-shipping-checklist';
export default {
  async fetch(request,env){
    const url=new URL(request.url);
    let path=url.pathname;
    const original=url.toString();
    if(url.hostname==='www.pikobuychina.com')url.hostname='pikobuychina.com';
    if(url.protocol==='http:')url.protocol='https:';
    const localized=path.match(/^\/(zh|fr|de|es|it|pl|nl|pt)(?=\/)/);
    const prefix=localized?localized[0]:'';
    const local=path.slice(prefix.length);
    if(local==='/index.html'||local==='/mobile'||local==='/mobile.html')path=prefix+'/';
    else if(local===LEGACY||local===LEGACY+'.html')path=prefix+'/guides/pikobuy-w2c-qc-shipping-2026';
    else if(path.endsWith('.html'))path=path.slice(0,-5);
    if(LANG_ROOT.test(path))path+='/';
    else if(path.length>1&&!/^\/(zh|fr|de|es|it|pl|nl|pt)\/$/.test(path))path=path.replace(/\/+$/,'');
    url.pathname=path;
    if(url.toString()!==original)return Response.redirect(url.toString(),301);
    const response=await env.ASSETS.fetch(request);
    const headers=new Headers(response.headers);
    headers.set('x-pikobuy-release','2026-10-16-multilingual');
    if((headers.get('content-type')||'').includes('text/html')){
      headers.set('cache-control','no-cache, max-age=0, must-revalidate');
      if(response.status===404)headers.set('x-robots-tag','noindex');
    }
    return new Response(response.body,{status:response.status,statusText:response.statusText,headers});
  }
};
