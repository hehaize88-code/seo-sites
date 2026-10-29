import {languages,routes,pathFor} from '../lib/i18n.mjs';
import {editorial} from '../lib/editorial.mjs';
import {editorialDate} from '../lib/article-routes.mjs';
import {site} from '../site.config.mjs';

export function GET() {
  const urls=Object.keys(languages).flatMap(lang=>routes.map(route=>{
    const article=editorial(lang).articles.find(a=>'articles/'+a.slug===route);
    // The existing article cross-links changed too. FAQ facts retain their
    // original date. Build time is not evidence of an editorial update.
    const modified=route==='faq'?editorialDate:'2026-10-29';
    const alternatives=[...Object.keys(languages).map(l=>[l,l]),['x-default','nl']];
    return `<url><loc>${site.domain+pathFor(lang,route)}</loc><lastmod>${article?.updated||modified}</lastmod>${alternatives.map(([label,l])=>`<xhtml:link rel="alternate" hreflang="${label}" href="${site.domain+pathFor(l,route)}"/>`).join('')}</url>`;
  })).join('');
  return new Response(`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">${urls}</urlset>`,{headers:{'Content-Type':'application/xml'}});
}
