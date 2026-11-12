import fs from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {build} from 'esbuild';
const assets=JSON.parse(await fs.readFile('assets-binary/manifest.json','utf8'));
for(const a of assets){const bytes=Buffer.concat(await Promise.all(a.parts.map(p=>fs.readFile(p))));if(createHash('sha256').update(bytes).digest('hex')!==a.sha256)throw Error('Asset checksum mismatch');await fs.mkdir(a.path.slice(0,a.path.lastIndexOf('/')),{recursive:true});await fs.writeFile(a.path,bytes)}
await import('./build-visual-worker.mjs');
await fs.rm('dist',{recursive:true,force:true});await fs.mkdir('dist',{recursive:true});
await build({entryPoints:['src/worker.ts'],outfile:'dist/worker.js',bundle:true,format:'esm',platform:'browser',target:'es2022'});
await fs.cp('public','dist/public',{recursive:true});
const langs=['en','de','fr','es','it','pt','pl','zh'];const index=JSON.parse(await fs.readFile('public/visual/index.json','utf8'));const ids=[...new Set(index.refs.flat().map(r=>r.id))];
const urls=langs.flatMap(l=>['','spreadsheet','categories','image-search',...ids.map(id=>'product?source='+encodeURIComponent('/AllProducts/'+id+'.html'))].map(p=>'https://litbuytab.com/'+l+'/'+p));
await fs.writeFile('dist/public/sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+urls.map(u=>'<url><loc>'+u.replaceAll('&','&amp;')+'</loc></url>').join('')+'</urlset>');
console.log('Built LitbuyTab with '+urls.length+' sitemap URLs; no database bindings.');
