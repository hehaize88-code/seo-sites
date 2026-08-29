const SITE="https://hipobuys.store";
const STORE="https://www.cnbuycha.com";

const ROOT_PAGES=[
  "/","/agent-workflow-guide","/categories","/disclaimer","/faq","/first-order-checklist","/guides",
  "/hipobuy-coupons-insurance-storefront-checklist","/hipobuy-fees-storefront-guide",
  "/hipobuy-qc-photos-storefront-checklist","/hipobuy-shipping-estimate-europe-storefront",
  "/hipobuy-keyword-search-product-finds",
  "/hipobuy-store-qc-photos-shipping-cost-checklist-2026","/hipobuy-store-w2c-qc-shipping-workflow-2026",
  "/imprint","/languages","/privacy","/product-qc-checklist","/products","/seo-guide",
  "/storefront-shipping-guide","/w2c-product-route-storefront-guide","/w2c-store-links"
];

const DAILY_PAGES=[
  "hipobuy-90-day-warehouse-plan-2026-07-11","hipobuy-buyer-brief-guide-2026-07-16",
  "hipobuy-community-finds-verification-guide-2026-07-18","hipobuy-consolidated-parcel-playbook-2026-07-09",
  "hipobuy-coupon-checkout-audit-2026-07-19","hipobuy-destination-first-parcel-plan-2026-07-12",
  "hipobuy-evidence-ladder-guide-2026-07-20","hipobuy-mixed-cart-parcel-guide-2026-07-13",
  "hipobuy-pre-shipment-control-guide-2026-07-17","hipobuy-proof-first-order-log-2026-07-10",
  "hipobuy-store-route-qc-parcel-checklist-2026-07-09","hipobuy-two-stage-budget-guide-2026-07-15",
  "hipobuy-warehouse-exception-guide-2026-07-14"
].map(slug=>"/daily-seo/"+slug);

const LOCALIZED_PAGES=[
  "/en/","/en/hipobuy-coupon/","/en/hipobuy-fees/","/en/qc-photos/","/en/shipping-from-china/","/en/w2c-links/",
  "/de/","/de/hipobuy-gutschein/","/de/hipobuy-kosten/","/de/qc-fotos/","/de/versand-aus-china/","/de/w2c-links/",
  "/fr/","/fr/coupon-hipobuy/","/fr/frais-hipobuy/","/fr/liens-w2c/","/fr/livraison-depuis-la-chine/","/fr/photos-qc/",
  "/es/","/es/cupon-hipobuy/","/es/enlaces-w2c/","/es/envio-desde-china/","/es/fotos-qc/","/es/tarifas-hipobuy/",
  "/it/","/it/costi-hipobuy/","/it/coupon-hipobuy/","/it/foto-qc/","/it/link-w2c/","/it/spedizione-dalla-cina/",
  "/pl/","/pl/koszty-hipobuy/","/pl/kupon-hipobuy/","/pl/linki-w2c/","/pl/wysylka-z-chin/","/pl/zdjecia-qc/",
  "/pt/","/pt/cupom-hipobuy/","/pt/envio-da-china/","/pt/fotos-qc/","/pt/links-w2c/","/pt/taxas-hipobuy/",
  "/nl/","/nl/hipobuy-korting/","/nl/hipobuy-kosten/","/nl/qc-fotos/","/nl/verzending-uit-china/","/nl/w2c-links/"
];

const PAGES=new Set([...ROOT_PAGES,...DAILY_PAGES,...LOCALIZED_PAGES]);
const ASSETS=new Set([
  "/robots.txt","/sitemap.xml","/autry-shoes.png","/bape-shoes.png","/corteiz-jacket.png",
  "/gucci-jacket.png","/hoka-shoes.png","/lv-hoodie.png","/new-balance-9060.png"
]);
const OLD_STORE_HOSTS=new Set(["cnfanssp.com","www.cnfanssp.com","cnfanshp.com","www.cnfanshp.com"]);
const PLATFORM_HOSTS=new Set(["hipobuy.com","www.hipobuy.com","app.hipobuy.com","play.google.com","apps.apple.com"]);
const CATEGORY_PATHS=new Set(["/shoes/","/hoodies-sweaters/","/t-shirts/","/jackets/","/pants-shorts/","/Jersey/","/accessories/","/electronics/","/headwear/","/other-stuff/"]);
const FAQ_SCHEMA='<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Is HipoBuys Store a checkout site?","acceptedAnswer":{"@type":"Answer","text":"No. It is an independent discovery and guide hub and does not process product orders or payments."}},{"@type":"Question","name":"Should visitors check QC photos?","acceptedAnswer":{"@type":"Answer","text":"Yes. Start by matching product identity, colour, size and quantity, then review visible measurements, construction and damage."}},{"@type":"Question","name":"Can users start with W2C searches?","acceptedAnswer":{"@type":"Answer","text":"Yes. A useful W2C route connects current search intent to an exact, dated product listing and a later QC checklist."}},{"@type":"Question","name":"Does the site guarantee delivery time?","acceptedAnswer":{"@type":"Answer","text":"No. Delivery depends on the selected route, parcel contents, carrier operations and customs processing."}}]}</script>';

const SECURITY_HEADERS={
  "X-Content-Type-Options":"nosniff",
  "Referrer-Policy":"strict-origin-when-cross-origin",
  "Permissions-Policy":"camera=(), microphone=(), geolocation=()",
  "X-Frame-Options":"SAMEORIGIN",
  "Strict-Transport-Security":"max-age=31536000; includeSubDomains",
  "Content-Security-Policy":"default-src 'self'; img-src 'self' https://www.cnbuycha.com data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com; form-action 'self' https://www.cnbuycha.com; base-uri 'self'; frame-ancestors 'self'"
};

function addSecurity(headers){
  for(const [name,value] of Object.entries(SECURITY_HEADERS))headers.set(name,value);
}

function redirect(url,status=301){
  return new Response(null,{status,headers:{Location:url.toString(),"Cache-Control":"public, max-age=3600"}});
}

function cleanPath(pathname){
  if(pathname==="/index.html")return "/";
  if(pathname.endsWith("/index.html"))return pathname.slice(0,-10)+"/";
  if(pathname.endsWith(".html"))return pathname.slice(0,-5)||"/";
  return pathname;
}

function canonicalPath(pathname){
  let clean=cleanPath(pathname);
  if(PAGES.has(clean))return clean;
  if(clean!=="/"&&clean.endsWith("/")&&PAGES.has(clean.slice(0,-1)))return clean.slice(0,-1);
  if(!clean.endsWith("/")&&PAGES.has(clean+"/"))return clean+"/";
  return clean;
}

function rewriteHref(value,currentUrl){
  if(!value||value.startsWith("#")||value.startsWith("mailto:")||value.startsWith("tel:")||value.startsWith("javascript:"))return value;
  let target;
  try{target=new URL(value,currentUrl)}catch{return value}
  if(target.hostname==="hipobuys.store"||target.hostname==="www.hipobuys.store"){
    target.hostname="hipobuys.store";
    target.pathname=canonicalPath(target.pathname);
    return target.pathname+target.search+target.hash;
  }
  if(OLD_STORE_HOSTS.has(target.hostname)){
    if(CATEGORY_PATHS.has(target.pathname))return STORE+target.pathname;
    if(target.pathname.startsWith("/AllProducts/")&&target.pathname!=="/AllProducts/")return "/products";
    return STORE+"/AllProducts/";
  }
  if(PLATFORM_HOSTS.has(target.hostname))return "/guides";
  return value;
}

async function notFound(request,env){
  const assetUrl=new URL("/404",request.url);
  const response=await env.ASSETS.fetch(assetUrl);
  const headers=new Headers(response.headers);
  addSecurity(headers);
  headers.set("Cache-Control","public, max-age=60");
  headers.set("X-Robots-Tag","noindex, nofollow");
  return new Response(response.body,{status:404,statusText:"Not Found",headers});
}

export default{
  async fetch(request,env){
    const url=new URL(request.url);

    if(url.hostname==="www.hipobuys.store"){
      url.hostname="hipobuys.store";
      url.pathname=canonicalPath(url.pathname);
      return redirect(url);
    }
    if(url.pathname==="/sitemap-extra.xml"){
      url.pathname="/sitemap.xml";
      return redirect(url);
    }

    const finalPath=canonicalPath(url.pathname);
    if(finalPath!==url.pathname){
      url.pathname=finalPath;
      return redirect(url);
    }

    if(!PAGES.has(url.pathname)&&!ASSETS.has(url.pathname))return notFound(request,env);

    const response=await env.ASSETS.fetch(request);
    if(response.status===404)return notFound(request,env);
    const headers=new Headers(response.headers);
    addSecurity(headers);
    const type=headers.get("content-type")||"";

    if(!type.includes("text/html")||response.status!==200){
      headers.set("Cache-Control",url.pathname==="/sitemap.xml"||url.pathname==="/robots.txt"?"public, max-age=300":"public, max-age=86400");
      return new Response(response.body,{status:response.status,statusText:response.statusText,headers});
    }

    headers.set("Cache-Control","public, max-age=0, s-maxage=3600, stale-while-revalidate=86400");
    const canonical=SITE+url.pathname;
    const current=url.toString();
    const extraHead=url.pathname==="/faq"?FAQ_SCHEMA:"";
    return new HTMLRewriter()
      .on('link[rel="canonical"]',{element(element){element.remove()}})
      .on('meta[property="og:url"]',{element(element){element.remove()}})
      .on("head",{element(element){element.append('<link rel="canonical" href="'+canonical+'"><meta property="og:url" content="'+canonical+'">'+extraHead,{html:true})}})
      .on("a[href]",{element(element){const href=element.getAttribute("href");const next=rewriteHref(href,current);if(next!==href)element.setAttribute("href",next);if(next&&next.startsWith(STORE)){element.setAttribute("rel","nofollow sponsored noopener");element.setAttribute("target","_blank")}}})
      .on("form[action]",{element(element){const action=element.getAttribute("action");if(action)element.setAttribute("action",rewriteHref(action,current))}})
      .on("img",{element(element){if(!element.hasAttribute("width"))element.setAttribute("width","600");if(!element.hasAttribute("height"))element.setAttribute("height","450");if(!element.hasAttribute("loading"))element.setAttribute("loading","lazy")}})
      .transform(new Response(response.body,{status:response.status,statusText:response.statusText,headers}));
  }
};
