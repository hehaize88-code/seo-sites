import {SITE_ORIGIN,isProductionHost} from '../../lib/site';
export function GET(request:Request){const live=isProductionHost(new URL(request.url).hostname);return new Response(live?`User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /*/saved\nSitemap: ${SITE_ORIGIN}/sitemap.xml\n`:'User-agent: *\nDisallow: /\n',{headers:{'Content-Type':'text/plain; charset=utf-8'}});}
