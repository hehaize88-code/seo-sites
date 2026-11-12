import {locales, pathFor, type Locale} from './i18n';
export const SITE_ORIGIN='https://usfansgrid.com';
export const sitePages=['','spreadsheet','categories','image-search','qc','shipping','faq','guides','how-to-buy','about','privacy'];
export function isProductionHost(host:string|null){return host?.split(':')[0]==='usfansgrid.com';}
export function canonicalPath(locale:Locale,page=''){return pathFor(locale,page);}
export function languageAlternates(page=''):Record<string,string>{return Object.fromEntries([...locales.map(l=>[l==='zh'?'zh-CN':l,SITE_ORIGIN+pathFor(l,page)]),['x-default',SITE_ORIGIN+pathFor('en',page)]]);}
export function xmlEscape(value:string){return value.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');}
