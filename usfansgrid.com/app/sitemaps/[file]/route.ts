import {SITE_ORIGIN} from '../../../lib/site';
import {locales,type Locale,pathFor} from '../../../lib/i18n';
import index from '../../../public/visual/index.json';
const ids=[...new Set(index.refs.flat().map(r=>r.id))];
export async function GET(_request:Request,{params}:{params:Promise<{file:string}>}){const {file}=await params,match=file.match(/^products-([a-z]+)\.xml$/);if(!match||!locales.includes(match[1] as Locale))return new Response('Not found',{status:404});const locale=match[1] as Locale;return new Response(`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${ids.map(id=>`<url><loc>${SITE_ORIGIN+pathFor(locale,'product/'+id)}</loc></url>`).join('')}</urlset>`,{headers:{'Content-Type':'application/xml; charset=utf-8','Cache-Control':'public, max-age=3600'}});}
