import {defineConfig} from 'astro/config';
export default defineConfig({
  site:'https://pikobuysheet.nl', output:'static', trailingSlash:'always',outDir:'./.astro-out',server:{host:'0.0.0.0',port:4173},
  vite:{server:{allowedHosts:['terminal.local'],watch:{ignored:['**/.astro-out/**','**/dist/**']}}}
});
