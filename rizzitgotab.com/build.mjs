import fs from 'node:fs';
fs.mkdirSync('dist/server',{recursive:true});
const files=['locales.js','ui.js','official-assets.js','search-index.js','variants.js','features.js','app.js'];
let code=files.map(f=>(f==='search-index.js'?fs.readdirSync('worker/index-parts').sort().map(n=>fs.readFileSync('worker/index-parts/'+n,'utf8')).join(''):fs.readFileSync('worker/'+f,'utf8')).replace(/^import .*?;\n/gm,'').replace(/export const /g,'const ')).join('\n');
code='const CLIENT='+JSON.stringify(fs.readFileSync('worker/client.js','utf8'))+';\n'+code;
fs.writeFileSync('dist/server/index.js',code);
