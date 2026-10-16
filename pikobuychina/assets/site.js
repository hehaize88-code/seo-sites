(()=>{
  const menu=document.querySelector('details.menu');
  const small=window.matchMedia('(max-width:800px)');
  const syncMenu=()=>{if(menu)menu.open=!small.matches};
  syncMenu();small.addEventListener('change',syncMenu);
  const language=document.querySelector('#language');
  if(language)language.addEventListener('change',()=>{location.assign(language.value)});
  const send=(name,data)=>{if(typeof window.gtag==='function')window.gtag('event',name,{page_language:document.documentElement.lang,...data})};
  document.addEventListener('click',event=>{
    const a=event.target.closest('a[href]');if(!a)return;
    let u;try{u=new URL(a.href,location.href)}catch{return}
    const data={link_url:u.href,link_text:a.textContent.trim().slice(0,120)};
    if(u.hostname==='cnfansge.com'||u.hostname==='www.cnfansge.com')send(a.closest('.product')?'product_card_click':'main_site_click',data);
    else if(u.origin===location.origin&&/^\/(?:zh\/|de\/|fr\/|es\/|it\/|pl\/|nl\/|pt\/)?(?:guides|articles)\//.test(u.pathname))send('article_open',data);
  });
  document.querySelectorAll('form.search').forEach(form=>form.addEventListener('submit',()=>{
    const input=form.querySelector('[name=keywords]');
    if(input&&input.value.trim())send('search_submit',{search_destination:form.action});
  }));
})();
