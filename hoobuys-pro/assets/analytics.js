(function(){
  function send(name,params){
    if(typeof window.gtag==='function') window.gtag('event',name,params||{});
  }
  document.addEventListener('click',function(event){
    var link=event.target.closest('a');
    if(!link) return;
    var url;
    try{url=new URL(link.href,window.location.href);}catch(error){return;}
    if(url.hostname==='cnfanssp.com'){
      send('outbound_product_click',{page_path:window.location.pathname,link_path:url.pathname});
    }else if(link.closest('.article-card')){
      send('article_cta_click',{page_path:window.location.pathname,link_path:url.pathname});
    }else if(link.closest('.route')){
      send('category_click',{page_path:window.location.pathname,link_path:url.pathname});
    }
  });
  var search=document.querySelector('form.search');
  if(search) search.addEventListener('submit',function(){send('search_submit',{page_path:window.location.pathname});});
})();
