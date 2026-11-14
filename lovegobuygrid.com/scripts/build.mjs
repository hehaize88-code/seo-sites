import fs from 'node:fs/promises';import path from 'node:path';
const read=p=>fs.readFile(p,'utf8');await fs.mkdir('dist/assets',{recursive:true});
for(const file of JSON.parse(await read('source-chunks/manifest.json'))){const content=(await Promise.all(file.parts.map(p=>read('source-chunks/'+p)))).join('');await fs.mkdir(path.dirname('dist/assets/'+file.dest),{recursive:true});await fs.writeFile('dist/assets/'+file.dest,Buffer.from(content,'base64'));}
const locale=(await read('src/locales.js')).replaceAll('export ',''),extra=await read('src/extra-locales.js');
const APP_JS=locale+'\n'+extra+'\n'+await read('src/client.js');
const STYLE_CSS=await read('src/style.css');
const HTML=(await read('src/index.html')).replace('noindex,nofollow','index,follow');
const SEARCH_WORKER=await read('src/search-worker.js');
let server=(await read('src/server.js')).replace('export default {async fetch','const app = {async fetch');
const preamble=`const PACKED_ASSETS={};const HTML=${JSON.stringify(HTML)};const STYLE_CSS=${JSON.stringify(STYLE_CSS)};const APP_JS=${JSON.stringify(APP_JS)};const SEARCH_WORKER=${JSON.stringify(SEARCH_WORKER)};\n`;
const routes=['','spreadsheet','categories','image-search','guide','faq','shipping'];
const langs=['en','de','fr','es','it','nl','pt','pl','ro','sv','zh','da','fi','el','cs','hu','bg','sk','hr','ja','ko','vi','th','id','sl','lt','lv','et','ga','mt'];
const tail=`
const site='https://lovegobuygrid.com';
const locales=${JSON.stringify(langs)}, pages=${JSON.stringify(routes)};
export default {async fetch(request,env,ctx){
 const u=new URL(request.url);
 if(u.hostname==='www.lovegobuygrid.com'||u.protocol==='http:')return Response.redirect(site+u.pathname+u.search,308);
 if(u.pathname==='/')return Response.redirect(site+'/en/',308);
 if(u.pathname==='/robots.txt')return new Response('User-agent: *\\nAllow: /\\nDisallow: /api/\\nDisallow: /image?\\nSitemap: '+site+'/sitemap.xml',{headers:{'Content-Type':'text/plain'}});
 if(u.pathname==='/sitemap.xml'){const xml='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+locales.flatMap(l=>pages.map(p=>'<url><loc>'+site+'/'+l+'/'+p+'</loc></url>')).join('')+'</urlset>';return new Response(xml,{headers:{'Content-Type':'application/xml;charset=utf-8'}});}
 if(['/brand/logo.png','/favicon.ico','/search/metadata.json.gz','/search/signatures.bin.gz'].includes(u.pathname))return env.ASSETS.fetch(request);
 const bits=u.pathname.split('/').filter(Boolean),isPage=locales.includes(bits[0])&&(pages.includes(bits.slice(1).join('/'))||/^product\\/\\d+$/.test(bits.slice(1).join('/')));
 if(!isPage&&!['/app.js','/style.css','/search-worker.js','/api/catalog','/api/product','/image'].includes(u.pathname))return new Response('Not found',{status:404});
 const res=await app.fetch(request,env,ctx),headers=new Headers(res.headers);headers.delete('X-Robots-Tag');
 if(isPage){let html=await res.text();const canonical=site+u.pathname;const sub=bits.slice(1).join('/');const alternates=locales.map(l=>'<link rel="alternate" hreflang="'+l+'" href="'+site+'/'+l+'/'+sub+'">').join('');html=html.replace('<html lang="en">','<html lang="'+bits[0]+'">').replace('</head>','<link rel="canonical" href="'+canonical+'">'+alternates+'<link rel="alternate" hreflang="x-default" href="'+site+'/en/'+sub+'"></head>');return new Response(html,{status:res.status,headers});}
 headers.set('X-Robots-Tag','noindex');return new Response(res.body,{status:res.status,headers});
}};`;
await fs.writeFile('dist/worker.js',preamble+server+tail);console.log('Built self-contained Cloudflare Worker and assets.');
