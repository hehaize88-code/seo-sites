const SITE='https://hipobuys.store';
const PAGES=new Set(["/","/agent-workflow-guide","/articles","/categories","/daily-seo/hipobuy-90-day-warehouse-plan-2026-07-11","/daily-seo/hipobuy-buyer-brief-guide-2026-07-16","/daily-seo/hipobuy-community-finds-verification-guide-2026-07-18","/daily-seo/hipobuy-consolidated-parcel-playbook-2026-07-09","/daily-seo/hipobuy-coupon-checkout-audit-2026-07-19","/daily-seo/hipobuy-destination-first-parcel-plan-2026-07-12","/daily-seo/hipobuy-evidence-ladder-guide-2026-07-20","/daily-seo/hipobuy-mixed-cart-parcel-guide-2026-07-13","/daily-seo/hipobuy-pre-shipment-control-guide-2026-07-17","/daily-seo/hipobuy-proof-first-order-log-2026-07-10","/daily-seo/hipobuy-store-route-qc-parcel-checklist-2026-07-09","/daily-seo/hipobuy-two-stage-budget-guide-2026-07-15","/daily-seo/hipobuy-warehouse-exception-guide-2026-07-14","/de/","/de/articles/","/de/hipobuy-gutschein/","/de/hipobuy-kosten/","/de/hipobuy-order-status-tracking-guide/","/de/hipobuy-rehearsal-parcel-volumetric-weight/","/de/hipobuy-shipping-calculator-weight-dimensions/","/de/hipobuy-shipping-time-seller-warehouse-delivery/","/de/hipobuy-size-guide-clothing-shoes/","/de/hipobuy-sneaker-finds-sizing-qc/","/de/hipobuy-warehouse-location-forwarding-address/","/de/qc-fotos/","/de/versand-aus-china/","/de/w2c-links/","/disclaimer","/en/hipobuy-coupon/","/en/hipobuy-fees/","/en/qc-photos/","/en/shipping-from-china/","/en/w2c-links/","/es/","/es/articles/","/es/cupon-hipobuy/","/es/enlaces-w2c/","/es/envio-desde-china/","/es/fotos-qc/","/es/hipobuy-order-status-tracking-guide/","/es/hipobuy-rehearsal-parcel-volumetric-weight/","/es/hipobuy-shipping-calculator-weight-dimensions/","/es/hipobuy-shipping-time-seller-warehouse-delivery/","/es/hipobuy-size-guide-clothing-shoes/","/es/hipobuy-sneaker-finds-sizing-qc/","/es/hipobuy-warehouse-location-forwarding-address/","/es/tarifas-hipobuy/","/faq","/first-order-checklist","/fr/","/fr/articles/","/fr/coupon-hipobuy/","/fr/frais-hipobuy/","/fr/hipobuy-order-status-tracking-guide/","/fr/hipobuy-rehearsal-parcel-volumetric-weight/","/fr/hipobuy-shipping-calculator-weight-dimensions/","/fr/hipobuy-shipping-time-seller-warehouse-delivery/","/fr/hipobuy-size-guide-clothing-shoes/","/fr/hipobuy-sneaker-finds-sizing-qc/","/fr/hipobuy-warehouse-location-forwarding-address/","/fr/liens-w2c/","/fr/livraison-depuis-la-chine/","/fr/photos-qc/","/guides","/hipobuy-1688-finds-moq-variants-seller-questions","/hipobuy-coupons-insurance-storefront-checklist","/hipobuy-custom-order-vs-forwarding-order","/hipobuy-fees-storefront-guide","/hipobuy-keyword-search-product-finds","/hipobuy-login-app-account-navigation","/hipobuy-order-status-tracking-guide","/hipobuy-qc-photos-storefront-checklist","/hipobuy-rehearsal-parcel-volumetric-weight","/hipobuy-restricted-items-shipping-lines","/hipobuy-review-2026-safety-workflow","/hipobuy-shipping-calculator-weight-dimensions","/hipobuy-shipping-estimate-europe-storefront","/hipobuy-shipping-time-seller-warehouse-delivery","/hipobuy-shipping-us-uk-canada","/hipobuy-size-guide-clothing-shoes","/hipobuy-sneaker-finds-sizing-qc","/hipobuy-spreadsheet-2026-product-links-qc-checks","/hipobuy-store-qc-photos-shipping-cost-checklist-2026","/hipobuy-store-w2c-qc-shipping-workflow-2026","/hipobuy-taobao-finds-listing-comparison","/hipobuy-warehouse-location-forwarding-address","/imprint","/it/","/it/articles/","/it/costi-hipobuy/","/it/coupon-hipobuy/","/it/foto-qc/","/it/hipobuy-order-status-tracking-guide/","/it/hipobuy-rehearsal-parcel-volumetric-weight/","/it/hipobuy-shipping-calculator-weight-dimensions/","/it/hipobuy-shipping-time-seller-warehouse-delivery/","/it/hipobuy-size-guide-clothing-shoes/","/it/hipobuy-sneaker-finds-sizing-qc/","/it/hipobuy-warehouse-location-forwarding-address/","/it/link-w2c/","/it/spedizione-dalla-cina/","/languages","/nl/","/nl/articles/","/nl/hipobuy-korting/","/nl/hipobuy-kosten/","/nl/hipobuy-order-status-tracking-guide/","/nl/hipobuy-rehearsal-parcel-volumetric-weight/","/nl/hipobuy-shipping-calculator-weight-dimensions/","/nl/hipobuy-shipping-time-seller-warehouse-delivery/","/nl/hipobuy-size-guide-clothing-shoes/","/nl/hipobuy-sneaker-finds-sizing-qc/","/nl/hipobuy-warehouse-location-forwarding-address/","/nl/qc-fotos/","/nl/verzending-uit-china/","/nl/w2c-links/","/pl/","/pl/articles/","/pl/hipobuy-order-status-tracking-guide/","/pl/hipobuy-rehearsal-parcel-volumetric-weight/","/pl/hipobuy-shipping-calculator-weight-dimensions/","/pl/hipobuy-shipping-time-seller-warehouse-delivery/","/pl/hipobuy-size-guide-clothing-shoes/","/pl/hipobuy-sneaker-finds-sizing-qc/","/pl/hipobuy-warehouse-location-forwarding-address/","/pl/koszty-hipobuy/","/pl/kupon-hipobuy/","/pl/linki-w2c/","/pl/wysylka-z-chin/","/pl/zdjecia-qc/","/privacy","/product-qc-checklist","/products","/pt/","/pt/articles/","/pt/cupom-hipobuy/","/pt/envio-da-china/","/pt/fotos-qc/","/pt/hipobuy-order-status-tracking-guide/","/pt/hipobuy-rehearsal-parcel-volumetric-weight/","/pt/hipobuy-shipping-calculator-weight-dimensions/","/pt/hipobuy-shipping-time-seller-warehouse-delivery/","/pt/hipobuy-size-guide-clothing-shoes/","/pt/hipobuy-sneaker-finds-sizing-qc/","/pt/hipobuy-warehouse-location-forwarding-address/","/pt/links-w2c/","/pt/taxas-hipobuy/","/seo-guide","/storefront-shipping-guide","/w2c-product-route-storefront-guide","/w2c-store-links"]);
const ASSETS=new Set(["/assets/brand-logo.css","/assets/editorial-9d4b0d97d1f6.css","/assets/hipobuy-logo.png","/assets/seo-article.css","/assets/site-67a2475014a8.js","/assets/site-analytics.js","/autry-shoes.png","/bape-shoes.png","/corteiz-jacket.png","/google-sitemap.xml","/gucci-jacket.png","/hoka-shoes.png","/lv-hoodie.png","/new-balance-9060.png","/robots.txt","/sitemap-extra.xml","/sitemap.xml"]);
const ENGLISH_SLUGS=new Set(["hipobuy-order-status-tracking-guide", "hipobuy-warehouse-location-forwarding-address", "hipobuy-shipping-calculator-weight-dimensions", "hipobuy-rehearsal-parcel-volumetric-weight", "hipobuy-shipping-time-seller-warehouse-delivery", "hipobuy-size-guide-clothing-shoes", "hipobuy-sneaker-finds-sizing-qc"]);
const STORE_HOSTS=new Set(['cnfanssp.com','www.cnfanssp.com','cnfanshp.com','www.cnfanshp.com']);
const SECURITY_HEADERS={
  'X-Content-Type-Options':'nosniff',
  'Referrer-Policy':'strict-origin-when-cross-origin',
  'Permissions-Policy':'camera=(), microphone=(), geolocation=()',
  'X-Frame-Options':'SAMEORIGIN',
  'Strict-Transport-Security':'max-age=31536000; includeSubDomains',
  'Content-Security-Policy':"default-src 'self'; img-src 'self' data: https://cnfanssp.com https://cnfanshp.com https://www.googletagmanager.com https://*.google-analytics.com; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com; connect-src 'self' https://www.googletagmanager.com https://*.google-analytics.com https://*.analytics.google.com https://*.google.com; form-action 'self' https://cnfanshp.com; base-uri 'self'; frame-ancestors 'self'"
};
function addSecurity(headers){for(const [key,value] of Object.entries(SECURITY_HEADERS))headers.set(key,value);}
function redirect(url){return new Response(null,{status:301,headers:{Location:url.toString(),'Cache-Control':'public, max-age=300'}});}
function canonicalPath(pathname){
  let path=pathname.replace(/\/{2,}/g,'/');
  if(path.endsWith('/index.html'))path=path.slice(0,-10);
  else if(path.endsWith('.html'))path=path.slice(0,-5);
  if(path==='/en'||path==='/en/')return '/';
  const english=path.match(/^\/en\/([^/]+)\/?$/);
  if(english&&(ENGLISH_SLUGS.has(english[1])||english[1]==='articles'))return '/'+english[1];
  if(PAGES.has(path))return path;
  if(path.endsWith('/')&&PAGES.has(path.slice(0,-1)))return path.slice(0,-1);
  if(PAGES.has(path+'/'))return path+'/';
  return path;
}
function rewriteHref(value,current){
  if(!value||/^(#|mailto:|tel:|javascript:)/i.test(value))return value;
  let u;try{u=new URL(value,current);}catch{return value;}
  if(['hipobuys.store','www.hipobuys.store'].includes(u.hostname))return canonicalPath(u.pathname)+u.search+u.hash;
  if(STORE_HOSTS.has(u.hostname)){u.hostname='cnfanshp.com';u.protocol='https:';u.port='';return u.toString();}
  return value; // Official references remain external, with their actual destination intact.
}
async function notFound(request,env){
  const res=await env.ASSETS.fetch(new URL('/404',request.url));
  const headers=new Headers(res.headers);addSecurity(headers);headers.set('X-Robots-Tag','noindex, nofollow');headers.set('Cache-Control','public, max-age=60');
  return new Response(res.body,{status:404,headers});
}
export default {async fetch(request,env){
  const u=new URL(request.url),path=canonicalPath(u.pathname);
  if(u.hostname==='www.hipobuys.store'||path!==u.pathname){u.hostname='hipobuys.store';u.protocol='https:';u.pathname=path;return redirect(u);}
  if(!PAGES.has(path)&&!ASSETS.has(path))return notFound(request,env);
  const response=await env.ASSETS.fetch(request);
  if(response.status===404)return notFound(request,env);
  const headers=new Headers(response.headers);addSecurity(headers);
  if(!headers.get('content-type')?.includes('text/html')||response.status!==200){
    headers.set('Cache-Control',path.endsWith('.xml')||path==='/robots.txt'?'public, max-age=300':/\/assets\/(editorial|site)-[a-f0-9]+\./.test(path)?'public, max-age=31536000, immutable':'public, max-age=3600');
    return new Response(response.body,{status:response.status,headers});
  }
  headers.set('Cache-Control','public, max-age=0, s-maxage=300, stale-while-revalidate=60');
  return new HTMLRewriter()
    .on('link[rel="canonical"]',{element(e){e.setAttribute('href',SITE+path);}})
    .on('meta[property="og:url"]',{element(e){e.setAttribute('content',SITE+path);}})
    .on('a[href]',{element(e){const value=e.getAttribute('href'),next=rewriteHref(value,u);if(next!==value)e.setAttribute('href',next);if(next&&next.startsWith('https://cnfanshp.com/')){e.setAttribute('target','_blank');e.setAttribute('rel','nofollow sponsored noopener');}}})
    .on('form[action]',{element(e){e.setAttribute('action',rewriteHref(e.getAttribute('action'),u));}})
    .transform(new Response(response.body,{status:response.status,headers}));
}};
