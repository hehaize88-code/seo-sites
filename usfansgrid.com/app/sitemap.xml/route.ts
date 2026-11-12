import {SITE_ORIGIN} from '../../lib/site';
import {locales} from '../../lib/i18n';
export function GET(){const paths=['sitemap-pages.xml',...locales.map(l=>`sitemaps/products-${l}.xml`)];return new Response(`<?xml version="1.0" encoding="UTF-8"?><sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${paths.map(p=>`<sitemap><loc>${SITE_ORIGIN}/${p}</loc></sitemap>`).join('')}</sitemapindex>`,{headers:{'Content-Type':'application/xml; charset=utf-8','Cache-Control':'public, max-age=3600'}});}
