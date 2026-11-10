import type {APIRoute} from 'astro';
export const GET:APIRoute=({url})=>new Response(url.hostname==='kakobuyitemhub.com'?'User-agent: *\nAllow: /\nDisallow: /api/\nSitemap: https://kakobuyitemhub.com/sitemap.xml\n':'User-agent: *\nDisallow: /\n',{headers:{'Content-Type':'text/plain; charset=utf-8'}});
