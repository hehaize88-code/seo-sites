document.addEventListener('click',function(event){
  var link=event.target.closest('a[href]');
  if(!link)return;
  var url;
  try{url=new URL(link.href,window.location.href)}catch(error){return}
  if(url.hostname!=='cnfanssp.com'&&url.hostname!=='www.cnfanssp.com')return;
  if(typeof window.gtag!=='function')return;
  window.gtag('event','open_main_site',{
    link_url:url.href,
    link_domain:url.hostname,
    link_text:(link.textContent||link.getAttribute('aria-label')||'').trim().slice(0,100),
    source_page:window.location.pathname,
    transport_type:'beacon'
  });
});
