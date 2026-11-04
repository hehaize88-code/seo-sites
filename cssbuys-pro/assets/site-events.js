(() => {
  if(window.__cssbuysEvents)return;window.__cssbuysEvents=true;
  document.addEventListener('click',event=>{
    const link=event.target.closest?.('a[href]');if(!link||typeof window.gtag!=='function')return;
    try{
      const target=new URL(link.href,location.href);
      const store=['cnfanshp.com','www.cnfanshp.com'].includes(target.hostname);
      const agent=target.hostname==='cssbuy.com'||target.hostname.endsWith('.cssbuy.com');
      if(!store&&!agent)return;
      // Log the destination path, never account identifiers or arbitrary query values.
      window.gtag('event',store?'store_outbound_click':'cssbuy_outbound_click',{
        link_url:target.origin+target.pathname,link_text:(link.textContent||'').trim().slice(0,100),
        language:document.documentElement.lang,link_type:store?(target.pathname==='/AllProducts/'?'catalog':target.pathname.startsWith('/AllProducts/')?'product':'category'):'official_resource',
        transport_type:'beacon'
      });
    }catch(_){}
  });
  document.addEventListener('submit',event=>{
    const form=event.target;if(!form.matches?.('form[role="search"]')||typeof window.gtag!=='function')return;
    window.gtag('event','store_search',{language:document.documentElement.lang,transport_type:'beacon'});
  });
})();
