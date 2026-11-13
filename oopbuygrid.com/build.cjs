const fs=require('fs'),vm=require('vm'),path=require('path');
const out='dist/public',base='https://oopbuygrid.com';
fs.rmSync('dist',{recursive:true,force:true});fs.mkdirSync(out,{recursive:true});fs.cpSync('public',out,{recursive:true});
for(const name of ['image-index.json','products.json']){const parts=fs.readdirSync('source-chunks').filter(f=>f.startsWith(name+'.part')).sort();fs.writeFileSync(out+'/'+name,Buffer.concat(parts.map(f=>fs.readFileSync('source-chunks/'+f))))}
const template=fs.readFileSync('public/index.html','utf8');
const source=fs.readFileSync('public/app.js','utf8').split('\n').filter(l=>!l.startsWith("window.addEventListener('hashchange'")).join('\n');
const app={innerHTML:''};
const context={localStorage:{},document:{addEventListener(){},querySelector:s=>s==='#app'?app:null,querySelectorAll:()=>[],documentElement:{lang:'en'},title:''},window:{addEventListener(){}},location:{hash:'',pathname:'/'},innerWidth:1280,Intl,Date,console};
vm.createContext(context);vm.runInContext(source,context);
context.inputProducts=JSON.parse(fs.readFileSync(out+'/products.json'));context.inputAudit=JSON.parse(fs.readFileSync('public/catalog-audit.json'));context.inputRates=JSON.parse(fs.readFileSync('public/rates.json'));
vm.runInContext('products=inputProducts;catalogAudit=inputAudit;rates=inputRates.rates;rateDate=inputRates.time_last_update_utc?.slice(0,16)||"";calculate=()=>{};',context);
const guides=vm.runInContext('guideData.map(g=>g[0])',context);
const routes=['/','/spreadsheet','/categories','/image-search','/shipping','/articles','/faq','/qc','/privacy','/terms',...guides.map(g=>'/guide/'+g),...context.inputProducts.map(p=>'/product/'+p.id)];
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const route of routes){
 context.location.pathname=route;
 // The image page binds upload events only in the browser.
 if(route==='/image-search')vm.runInContext('shell(imagePage())',context);else vm.runInContext('render()',context);
 let body=app.innerHTML.replace(/href="#\//g,'href="/');
 const product=route.startsWith('/product/')?context.inputProducts.find(p=>route==='/product/'+p.id):null;
 const description=product?`${product.title}. Browse available product photos, reference prices and buying links on Oopbuy Grid.`:'Browse Oopbuy finds, search product photos and compare buying links. Independent product discovery with 24 interface languages.';
 let html=template.replace('<div id="app"></div>','<div id="app">'+body+'</div>').replace(/<title>.*?<\/title>/,'<title>'+esc(context.document.title)+'</title>').replace(/<meta name="description"[^>]*>/,'<meta name="description" content="'+esc(description)+'">').replace(/<link rel="canonical"[^>]*>/,'<link rel="canonical" href="'+base+route+'">');
 const file=path.join(out,route,'index.html');fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,html);
}
const urlset=rs=>'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+rs.map(r=>'<url><loc>'+base+esc(r)+'</loc></url>').join('')+'</urlset>';
fs.writeFileSync(out+'/sitemap-pages.xml',urlset(routes.filter(r=>!r.startsWith('/product/'))));
fs.writeFileSync(out+'/sitemap-products.xml',urlset(routes.filter(r=>r.startsWith('/product/'))));
fs.writeFileSync(out+'/sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+['pages','products'].map(n=>'<sitemap><loc>'+base+'/sitemap-'+n+'.xml</loc></sitemap>').join('')+'</sitemapindex>');
fs.writeFileSync(out+'/robots.txt','User-agent: *\nAllow: /\nSitemap: '+base+'/sitemap.xml\n');
fs.writeFileSync(out+'/404.html','<!doctype html><html lang="en"><head><meta name="robots" content="noindex"><title>Page not found · Oopbuy Grid</title></head><body><h1>Page not found</h1><a href="/">Back to Oopbuy Grid</a></body></html>');
console.log(JSON.stringify({pages:routes.length,products:context.inputProducts.length,images:context.inputAudit.indexedImageCount}));
