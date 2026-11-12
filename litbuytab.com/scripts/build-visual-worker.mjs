import {build} from 'vite';
import path from 'node:path';
// Separate build avoids injecting the framework's window-based dev overlay into a Worker.
await build({configFile:false,publicDir:false,base:'/visual/worker/',logLevel:'warn',resolve:{conditions:['browser','import','default']},define:{'process.env.NODE_ENV':'"production"'},build:{target:'es2022',minify:true,assetsInlineLimit:0,outDir:'public/visual/worker',emptyOutDir:true,rollupOptions:{input:path.resolve('lib/visual/search.worker.ts'),output:{entryFileNames:'search-worker.js',chunkFileNames:'chunks/[name]-[hash].js',assetFileNames:'assets/[name]-[hash][extname]'}}}});
