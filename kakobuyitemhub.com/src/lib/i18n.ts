import dictionary from './translations.json';
export const languages=[{code:'en',name:'English'},{code:'zh',name:'简体中文'},{code:'de',name:'Deutsch'},{code:'fr',name:'Français'},{code:'es',name:'Español'},{code:'it',name:'Italiano'},{code:'pl',name:'Polski'},{code:'pt',name:'Português'}];
export function locale(url:URL){const code=url.searchParams.get('lang');return languages.some(l=>l.code===code)?code!:'en';}
export function translator(lang:string){return (en:string,zh:string)=>lang==='zh'?zh:lang==='en'?en:(dictionary as Record<string,Record<string,string>>)[en]?.[lang]||en;}
export function languageUrl(url:URL,lang:string){const next=new URL(url);next.searchParams.set('lang',lang);return next.pathname+next.search;}
