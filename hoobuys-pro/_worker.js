const SECURITY_HEADERS={
  "X-Content-Type-Options":"nosniff",
  "Referrer-Policy":"strict-origin-when-cross-origin",
  "Permissions-Policy":"camera=(), microphone=(), geolocation=()",
  "X-Frame-Options":"SAMEORIGIN",
  "Strict-Transport-Security":"max-age=31536000; includeSubDomains",
  "Content-Security-Policy":"default-src 'self'; img-src 'self' https://www.cnbuycha.com data:; style-src 'self' 'unsafe-inline'; script-src 'self'; form-action 'self' https://www.cnbuycha.com; base-uri 'self'; frame-ancestors 'self'"
};

function redirect(url,status=301){
  return new Response(null,{status,headers:{Location:url.toString(),"Cache-Control":"public, max-age=3600"}});
}

export default{
  async fetch(request,env){
    const url=new URL(request.url);
    if(url.hostname==="www.hoobuys.pro"){
      url.hostname="hoobuys.pro";
      return redirect(url);
    }
    if(url.pathname==="/languages"||url.pathname==="/languages.html"){
      url.pathname="/";
      return redirect(url);
    }
    if(url.pathname==="/hoobuy-pro-europe-parcel-ledger-w2c-qc-2026-07-14"||url.pathname==="/hoobuy-pro-europe-parcel-ledger-w2c-qc-2026-07-14.html"){
      url.pathname="/shipping-guide";
      return redirect(url);
    }
    if(url.pathname.endsWith(".html")){
      url.pathname=url.pathname.slice(0,-5)||"/";
      return redirect(url);
    }
    if(url.pathname!=="/"&&url.pathname.endsWith("/")){
      url.pathname=url.pathname.slice(0,-1);
      return redirect(url);
    }
    const response=await env.ASSETS.fetch(request);
    const headers=new Headers(response.headers);
    for(const [name,value] of Object.entries(SECURITY_HEADERS))headers.set(name,value);

    const type=headers.get("content-type")||"";
    if(!type.includes("text/html")||response.status!==200){
      if(response.status===404)headers.set("Cache-Control","public, max-age=60");
      return new Response(response.body,{status:response.status,statusText:response.statusText,headers});
    }

    headers.set("Cache-Control","public, max-age=0, s-maxage=3600, stale-while-revalidate=86400");
    const canonical="https://hoobuys.pro"+url.pathname;
    const transformed=new HTMLRewriter()
      .on('link[rel="canonical"]',{element(element){element.remove()}})
      .on("head",{element(element){element.append('<link rel="canonical" href="'+canonical+'">',{html:true})}})
      .transform(new Response(response.body,{status:response.status,statusText:response.statusText,headers}));
    return transformed;
  }
};
