const MEASUREMENT_ID = 'G-VLWTW53ETS';
const ANALYTICS_HEAD = `<script async src="https://www.googletagmanager.com/gtag/js?id=${MEASUREMENT_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','${MEASUREMENT_ID}');</script>`;

const HOME_STYLE = `<style>
.piko-logo-img{display:block;width:245px;height:auto;max-height:52px;object-fit:contain}
html,body{max-width:100%;overflow-x:hidden}
@media(max-width:760px){body{font-size:13px!important}.container{width:94vw!important}.piko-logo-img{width:158px}.hero{padding:6px 0 4px!important}.hero-grid{display:block!important}.kicker{font-size:10px!important;padding:3px 7px!important;margin-bottom:4px!important}h1{font-size:26px!important;line-height:1!important;letter-spacing:-.03em!important;margin:0 0 6px!important}.lead{font-size:11.5px!important;line-height:1.35!important;margin:0 0 7px!important}.hero-actions{gap:6px!important;margin:0 0 6px!important}.hero-actions .cta{font-size:11px!important;padding:7px 9px!important}.metrics{display:flex!important;gap:5px!important;overflow-x:auto!important;margin-top:4px!important;padding-bottom:2px!important}.metric{flex:0 0 92px!important;padding:7px 8px!important;border-radius:12px!important;box-shadow:none!important}.metric b{font-size:17px!important}.metric span,.metric small{font-size:9.5px!important}.mock{display:block!important;margin-top:7px!important;border-radius:14px!important;box-shadow:none!important}.mocktop{display:none!important}.mockbody{padding:6px!important}.mockbody .step{display:grid!important;grid-template-columns:38px minmax(0,1fr) auto!important;padding:5px!important;gap:7px!important;margin-top:5px!important}.mockbody .step img{width:38px!important;height:38px!important;border-radius:9px!important;object-fit:cover!important}.mockbody .step b{font-size:10.5px!important}.mockbody .step .mobile-note{display:block!important;font-size:9px!important;white-space:nowrap!important;overflow:hidden!important;text-overflow:ellipsis!important}.mockbody .step .pill{font-size:9px!important;padding:5px 6px!important}.search{margin:0!important;padding:5px!important;border-radius:12px!important;gap:4px!important}.search input{min-width:0!important;padding:6px!important;font-size:12px!important}.search button{padding:0 12px!important;font-size:11px!important;border-radius:10px!important}.section{padding:7px 0!important;scroll-margin-top:58px!important}.section-head{display:block!important;margin-bottom:5px!important}h2{font-size:19px!important;line-height:1.05!important;margin:0 0 2px!important}.section-head p{font-size:11px!important;line-height:1.25!important}.chips{display:flex!important;overflow-x:auto!important;flex-wrap:nowrap!important;gap:5px!important;margin:5px 0 6px!important;padding-bottom:2px!important}.chip{flex:0 0 auto!important;padding:6px 8px!important;font-size:10.5px!important}.products{display:flex!important;overflow-x:auto!important;gap:7px!important;scroll-snap-type:x mandatory;padding-bottom:3px!important}.product-card,.product-card:nth-of-type(n+9){display:block!important;flex:0 0 138px!important;border-radius:14px!important;scroll-snap-align:start;box-shadow:none!important}.imgbox{height:64px!important}.pbody{padding:5px!important}.tags{display:none!important}.pbody h3{font-size:10.5px!important;line-height:1.12!important;min-height:22px!important;margin:0 0 2px!important}.pbody p{display:none!important}.price{font-size:14px!important;margin:2px 0 4px!important}.btn.dark{font-size:10px!important;padding:6px 5px!important;border-radius:8px!important}.catgrid,.infogrid,.articlegrid{display:flex!important;overflow-x:auto!important;gap:7px!important;padding-bottom:3px!important}.cat,.info,.article{flex:0 0 150px!important;padding:8px!important;border-radius:13px!important;box-shadow:none!important}.cat b,.info h3,.article h3{font-size:12px!important;line-height:1.15!important;margin:0 0 3px!important}.cat p,.info p,.article p{display:block!important;font-size:10.5px!important;line-height:1.3!important;margin:0 0 3px!important}.cat span{font-size:10.5px!important}.footer{padding:12px 0 8px!important;margin-top:8px!important}.products,.catgrid,.infogrid,.articlegrid,.chips,.metrics{scrollbar-width:none}.products::-webkit-scrollbar,.catgrid::-webkit-scrollbar,.infogrid::-webkit-scrollbar,.articlegrid::-webkit-scrollbar,.chips::-webkit-scrollbar,.metrics::-webkit-scrollbar{display:none}}
</style>`;

const CATEGORIES = [
  ['Shoes','shoes'],['Sweatshirts','hoodies-sweaters'],['T-Shirts','t-shirts'],
  ['Jackets','jackets'],['Pants/Shorts','pants-shorts'],['Headwear','headwear'],
  ['Accessories','accessories'],['Short Sets','short-sets'],['Electronics','electronics'],
  ['Other Stuff','other-stuff'],['Jersey','jersey']
];

const HOME_ARTICLES = `<section class="section" id="articles"><div class="container"><div class="section-head"><div><h2 data-i18n="articles_title">PikoBuy Buyer Guides</h2><p data-i18n="articles_lead">Open a card to read the complete independent guide on its own page.</p></div><a class="cta secondary" href="/articles">View All Articles</a></div><div class="articlegrid"><a class="article" href="/guides/how-to-buy-from-pikobuy-2026"><h3>How to Buy From PikoBuy</h3><p>Follow the complete product-link, first-payment, warehouse QC and international parcel workflow.</p><span class="btn">Read Full Guide</span></a><a class="article" href="/guides/how-to-submit-pikobuy-parcel-2026"><h3>How to Submit a Parcel</h3><p>Select warehouse items, check the address, compare routes and pay international shipping.</p><span class="btn">Read Full Guide</span></a><a class="article" href="/guides/how-long-does-pikobuy-take-2026"><h3>How Long Does PikoBuy Take?</h3><p>Separate seller processing, China delivery, warehouse work, parcel dispatch and carrier transit.</p><span class="btn">Read Full Guide</span></a><a class="article" href="/guides/how-to-cancel-pikobuy-purchase-2026"><h3>Cancel a Purchase or Return an Item</h3><p>Choose the correct action for an unshipped order, warehouse item or dispatched parcel.</p><span class="btn">Read Full Guide</span></a><a class="article" href="/guides/does-pikobuy-ship-to-canada-2026"><h3>Does PikoBuy Ship to Canada?</h3><p>Verify live Canadian routes, billable weight, address details and landed-cost uncertainty.</p><span class="btn">Read Full Guide</span></a></div></div></section>`;

function categorySection(){
  const cards=CATEGORIES.map(([name,slug])=>`<a class="cat" href="https://cnfansge.com/${slug}/" target="_blank" rel="noopener"><b>${name}</b><p>Open the dedicated catalog page for this category.</p><span data-i18n="open_filter">Open category</span></a>`).join('');
  return `<section class="section" id="categories"><div class="container"><div class="section-head"><div><h2 data-i18n="categories_title">Product Categories</h2><p data-i18n="categories_lead">Tap a category to open its dedicated product catalog page.</p></div></div><div class="catgrid">${cards}</div></div></section>`;
}

const CLIENT_SCRIPT = `<script>(()=>{
function send(name,params){if(typeof window.gtag==='function')window.gtag('event',name,params||{})}
function text(el){return (el.textContent||'').trim().replace(/\\s+/g,' ').slice(0,120)}
function logo(){document.querySelectorAll('a.brand').forEach(a=>{if(!a.querySelector('img'))a.innerHTML='<img class="piko-logo-img" src="/assets/123.png" alt="PIKOBUY">'})}
document.addEventListener('click',event=>{const a=event.target.closest('a[href]');if(!a)return;let url;try{url=new URL(a.href,location.href)}catch{return}const params={link_url:url.href,link_text:text(a)};if(url.hostname.endsWith('cnfansge.com'))send(a.closest('.product-card,.hero-product-card')?'product_card_click':'main_site_click',params);else if(url.origin===location.origin&&(/\\/guides\\//.test(url.pathname)||/\\/articles\\//.test(url.pathname)))send('article_open',params)},true);
const destination='https://cnfansge.com/search.html';
function redirect(input){const keyword=(input.value||'').trim();if(!keyword){input.focus();return}send('search_submit',{search_term:keyword,search_destination:destination});setTimeout(()=>{location.href=destination+'?keywords='+encodeURIComponent(keyword)+'&channelid=2'},120)}
function bind(){document.querySelectorAll('.search').forEach(box=>{if(box.dataset.mainSearchBound==='1')return;const input=box.querySelector('input');const button=box.querySelector('button,[type="submit"]');if(!input||!button)return;box.dataset.mainSearchBound='1';const submit=e=>{if(e){e.preventDefault();e.stopPropagation();e.stopImmediatePropagation()}redirect(input)};button.removeAttribute('onclick');button.onclick=null;button.type='button';button.addEventListener('click',submit,true);input.addEventListener('keydown',e=>{if(e.key==='Enter')submit(e)},true);const form=box.tagName==='FORM'?box:box.closest('form');if(form){form.removeAttribute('action');form.onsubmit=null;form.addEventListener('submit',submit,true)}})}
logo();bind();document.addEventListener('DOMContentLoaded',()=>{logo();bind()});setTimeout(bind,500);
})();</script>`;

function patchHome(html){
  html=html.replace('<title>PikoBuy Shipping, Tracking &amp; Warehouse Guide (2026)</title>','<title>PikoBuy Guide: Buy, Ship, Track &amp; Check QC (2026)</title>')
    .replace('content="Understand PikoBuy order stages, warehouse QC, shipping costs, returns and parcel tracking with practical, fact-checked 2026 guides."','content="Learn how to use PikoBuy in 2026: buy products, review warehouse QC, submit a parcel, estimate shipping, track delivery and request a return."')
    .replace('content="PikoBuy Shipping, Tracking &amp; Warehouse Guide (2026)"','content="PikoBuy Guide: Buy, Ship, Track &amp; Check QC (2026)"')
    .replace('content="Practical PikoBuy help for order status, warehouse QC, shipping cost and parcel tracking."','content="Learn how to buy, check warehouse QC, submit a parcel, estimate shipping, track delivery and handle returns with PikoBuy."')
    .replace('{"":"https://schema.org","":"WebSite"}','{"@context":"https://schema.org","@type":"WebSite"}')
    .replace('<h1 data-i18n="hero_title">PikoBuy Shipping, Tracking and Warehouse Guide (2026)</h1>','<h1 data-i18n="hero_title">How to Use PikoBuy: Buy, QC, Ship and Track</h1>');
  html=html.replaceAll('href="#home"','href="/"').replaceAll('href="#finds"','href="/finds"').replaceAll('href="#categories"','href="/categories"').replaceAll('href="#w2c"','href="/w2c"').replaceAll('href="#qc"','href="/qc"').replaceAll('href="#shipping"','href="/shipping"').replaceAll('href="#coupons"','href="/coupons"').replaceAll('href="#articles"','href="/articles"');
  html=html.replaceAll('https://cnfansge.com/sweatshirts/','https://cnfansge.com/hoodies-sweaters/').replaceAll('https://www.cnfansge.com/sweatshirts/','https://cnfansge.com/hoodies-sweaters/');
  html=html.replace(/<section class="section" id="categories">[\s\S]*?<section class="section" id="finds">/,categorySection()+'<section class="section" id="finds">');
  html=html.replace(/<section id="categories"[\s\S]*?<section id="finds"/,categorySection()+'<section id="finds"');
  html=html.replace(/<section class="section" id="articles">[\s\S]*?<\/section>/,HOME_ARTICLES);
  html=html.replace("categories_lead:'点击类目可直接筛选本页紧凑产品卡片。'","categories_lead:'点击类目会直接打开主站对应的独立分类页面。'").replace("open_filter:'筛选产品'","open_filter:'打开分类'").replace("categories_lead:'Tap a category to filter the compact product cards on this page.'","categories_lead:'Tap a category to open its dedicated product catalog page.'").replace("open_filter:'Filter products'","open_filter:'Open category'");
  html=html.replace("hero_title:'Pikobuy 2026 电子表格：W2C好物、QC照片和中国购物链接'","hero_title:'PikoBuy 使用指南：下单、质检、发货与追踪'").replace("articles_title:'SEO文章与FAQ'","articles_title:'PikoBuy买家指南'").replace("articles_lead:'点击文章卡片即可进入对应的完整独立文章页。'","articles_lead:'点击卡片即可在独立页面阅读完整指南。'").replace("hero_title:'PikoBuy Shipping, Tracking and Warehouse Guide (2026)'","hero_title:'How to Use PikoBuy: Buy, QC, Ship and Track'").replace("articles_title:'SEO Articles & FAQ'","articles_title:'PikoBuy Buyer Guides'").replace("articles_lead:'Open a card to read the complete independent article.'","articles_lead:'Open a card to read the complete independent guide on its own page.'");
  html=html.replace("document.querySelectorAll('[data-filter-link]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();setFilter(a.dataset.filterLink)}));",'');
  return html.replace('</head>',HOME_STYLE+'</head>');
}

function patchHtml(html,isHome){
  if(isHome)html=patchHome(html);
  if(!html.includes('googletagmanager.com/gtag/js'))html=html.replace('</head>',ANALYTICS_HEAD+'</head>');
  if(!html.includes("article_open',params"))html=html.replace('</body>',CLIENT_SCRIPT+'</body>');
  return html;
}

const LEGACY_PATHS=new Map([
  ['/index.html','/'],['/mobile','/'],['/mobile.html','/'],['/seo-guide.html','/seo-guide'],
  ['/faq.html','/faq'],['/guides.html','/guides'],['/finds.html','/finds'],
  ['/categories.html','/categories'],['/w2c.html','/w2c'],['/qc.html','/qc'],
  ['/shipping.html','/shipping'],['/coupons.html','/coupons'],['/articles.html','/articles'],
  ['/guides/pikobuy-tracking-order-status-guide-2026.html','/guides/pikobuy-tracking-order-status-guide-2026'],
  ['/guides/pikobuy-total-landed-cost-worksheet-2026.html','/guides/pikobuy-total-landed-cost-worksheet-2026'],
  ['/guides/pikobuy-domestic-shipping-seller-warehouse-2026.html','/guides/pikobuy-domestic-shipping-seller-warehouse-2026'],
  ['/guides/pikobuy-w2c-qc-shipping-2026.html','/guides/pikobuy-w2c-qc-shipping-2026'],
  ['/guides/pikobuychina-spreadsheet-qc-parcel-2026-07-09.html','/guides/pikobuychina-spreadsheet-qc-parcel-2026-07-09'],
  ['/guides/how-to-buy-from-pikobuy-2026.html','/guides/how-to-buy-from-pikobuy-2026'],
  ['/guides/how-to-submit-pikobuy-parcel-2026.html','/guides/how-to-submit-pikobuy-parcel-2026'],
  ['/guides/how-long-does-pikobuy-take-2026.html','/guides/how-long-does-pikobuy-take-2026'],
  ['/guides/how-to-cancel-pikobuy-purchase-2026.html','/guides/how-to-cancel-pikobuy-purchase-2026'],
  ['/guides/does-pikobuy-ship-to-canada-2026.html','/guides/does-pikobuy-ship-to-canada-2026'],
  ['/articles/pikobuy-w2c-qc-shipping-checklist','/guides/pikobuy-w2c-qc-shipping-2026'],
  ['/articles/pikobuy-w2c-qc-shipping-checklist.html','/guides/pikobuy-w2c-qc-shipping-2026']
]);

export default{async fetch(request,env){
  const url=new URL(request.url);
  if(url.protocol!=='https:'||url.hostname==='www.pikobuychina.com'){
    url.hostname='pikobuychina.com';url.protocol='https:';return Response.redirect(url.toString(),301);
  }
  const path=url.pathname.length>1?url.pathname.replace(/\/+$/,''):url.pathname;
  const target=LEGACY_PATHS.get(path);
  if(target){url.pathname=target;return Response.redirect(url.toString(),301)}
  const res=await env.ASSETS.fetch(request);
  const contentType=res.headers.get('content-type')||'';
  if(!contentType.includes('text/html'))return res;
  const headers=new Headers(res.headers);
  headers.set('content-type','text/html; charset=UTF-8');
  headers.set('cache-control','no-cache, max-age=0, must-revalidate');
  return new Response(patchHtml(await res.text(),path==='/'),{status:res.status,statusText:res.statusText,headers});
}};
