(function(){
  'use strict';
  const STORE='cnfanshp.com';
  const locale=document.documentElement.lang||'en';
  function track(name,params){if(typeof window.gtag==='function')window.gtag('event',name,Object.assign({page_language:locale,page_path:location.pathname,transport_type:'beacon'},params));}
  function decorate(link){try{const u=new URL(link.href,location.href);if(!['cnfanssp.com','www.cnfanssp.com',STORE,'www.'+STORE].includes(u.hostname))return;u.hostname=STORE;u.protocol='https:';for(const [k,v] of Object.entries({utm_source:'hipobuys.store',utm_medium:'referral',utm_campaign:'hipobuy_content_hub',utm_content:location.pathname}))if(!u.searchParams.has(k))u.searchParams.set(k,v);link.href=u.toString();}catch{}}
  function init(){
    document.querySelectorAll('a[href]').forEach(decorate);
    const menu=document.querySelector('.menu'),nav=document.querySelector('#nav');
    if(menu&&nav)menu.addEventListener('click',function(){nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(nav.classList.contains('open')));});
    document.querySelectorAll('form[action]').forEach(function(form){try{if(new URL(form.action,location.href).hostname!==STORE)return;}catch{return;}for(const [name,value] of Object.entries({utm_source:'hipobuys.store',utm_medium:'referral',utm_campaign:'site_search',utm_content:location.pathname})){if(form.querySelector('[name="'+name+'"]'))continue;const input=document.createElement('input');input.type='hidden';input.name=name;input.value=value;form.appendChild(input);}});
    document.querySelectorAll('[data-calculator]').forEach(function(form){form.addEventListener('submit',function(event){event.preventDefault();const data=new FormData(form);const values=['length','width','height','weight','divisor'].map(k=>Number(data.get(k)));const out=form.querySelector('output');if(values.some(v=>!Number.isFinite(v)||v<=0)){out.textContent=form.dataset.invalid;return;}const [l,w,h,weight,divisor]=values;const volume=l*w*h/divisor,billable=Math.max(weight,volume);if(!Number.isFinite(volume)){out.textContent=form.dataset.invalid;return;}const number=new Intl.NumberFormat(locale,{maximumFractionDigits:3});out.textContent=form.dataset.volume+': '+number.format(volume)+' kg · '+form.dataset.billable+': '+number.format(billable)+' kg';track('shipping_weight_calculation',{content_group:'shipping'});});});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
  document.addEventListener('click',function(event){const a=event.target.closest&&event.target.closest('a[href]');if(!a)return;try{const u=new URL(a.href,location.href);if(u.hostname===STORE)track('outbound_product_click',{link_domain:STORE,link_url:u.origin+u.pathname});else if(a.closest('.languages'))track('language_switch',{target_language:a.hreflang});}catch{}},true);
  document.addEventListener('submit',function(event){try{if(new URL(event.target.action,location.href).hostname===STORE)track('product_search',{content_group:'products'});}catch{}},true);
})();
