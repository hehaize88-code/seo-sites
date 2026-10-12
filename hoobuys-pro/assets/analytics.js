(function(){
  function send(name, params){
    if(typeof window.gtag==='function') window.gtag('event',name,Object.assign({page_path:location.pathname,language:document.documentElement.lang},params||{}));
  }
  document.addEventListener('click',function(event){
    var link=event.target.closest('a'); if(!link)return;
    var url;try{url=new URL(link.href,location.href);}catch(e){return;}
    if(link.closest('.language-picker'))send('language_switch',{target_language:link.hreflang});
    else if(url.hostname==='cnfanssp.com'||url.hostname==='www.cnfanssp.com'){
      if(/^\/AllProducts\/\d+\.html$/.test(url.pathname))send('outbound_product_click',{link_path:url.pathname});
      else if(link.dataset.category)send('category_click',{category:link.dataset.category,link_path:url.pathname});
      else send('product_index_click',{link_path:url.pathname});
    } else if(link.closest('.article-card,.related,.essential-links'))send('article_cta_click',{link_path:url.pathname});
  });
  var search=document.querySelector('form.search');
  if(search)search.addEventListener('submit',function(){send('search_submit');});
})();
