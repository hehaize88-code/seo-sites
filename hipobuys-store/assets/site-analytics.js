(function(){
  const STORE_HOST="cnfanssp.com";
  const campaign="hipobuy_content_hub";
  function decorate(raw){
    try{
      const url=new URL(raw,location.href);
      if(url.hostname!==STORE_HOST&&url.hostname!=="www."+STORE_HOST)return raw;
      url.hostname=STORE_HOST;
      if(!url.searchParams.has("utm_source"))url.searchParams.set("utm_source","hipobuys.store");
      if(!url.searchParams.has("utm_medium"))url.searchParams.set("utm_medium","referral");
      if(!url.searchParams.has("utm_campaign"))url.searchParams.set("utm_campaign",campaign);
      if(!url.searchParams.has("utm_content"))url.searchParams.set("utm_content",location.pathname.replace(/^\/+|\/+$/g,"")||"home");
      return url.toString();
    }catch{return raw}
  }
  function track(name,params){if(typeof window.gtag==="function")window.gtag("event",name,params)}
  document.addEventListener("DOMContentLoaded",function(){
    document.querySelectorAll("a[href]").forEach(function(link){
      const next=decorate(link.href);if(next!==link.href)link.href=next;
    });
    document.querySelectorAll("form[action]").forEach(function(form){
      try{if(new URL(form.action,location.href).hostname!==STORE_HOST)return}catch{return}
      [["utm_source","hipobuys.store"],["utm_medium","referral"],["utm_campaign","site_search"],["utm_content",location.pathname.replace(/^\/+|\/+$/g,"")||"home"]].forEach(function(pair){
        if(form.querySelector('[name="'+pair[0]+'"]'))return;
        const input=document.createElement("input");input.type="hidden";input.name=pair[0];input.value=pair[1];form.appendChild(input);
      });
    });
  });
  document.addEventListener("click",function(event){
    const link=event.target.closest&&event.target.closest("a[href]");if(!link)return;
    try{const url=new URL(link.href,location.href);if(url.hostname===STORE_HOST)track("outbound_to_cnfanssp",{link_url:url.toString(),link_text:(link.textContent||"").trim().slice(0,100),page_path:location.pathname,transport_type:"beacon"})}catch{}
  },true);
  document.addEventListener("submit",function(event){
    const form=event.target;try{if(new URL(form.action,location.href).hostname===STORE_HOST)track("search_submit",{page_path:location.pathname,search_term:(new FormData(form).get("keywords")||"").toString().slice(0,100),transport_type:"beacon"})}catch{}
  },true);
})();
