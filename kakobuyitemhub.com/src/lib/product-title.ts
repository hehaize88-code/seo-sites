import titles from '../content/product-translations.json';
// Display-only translation catalog. Source titles, products and identifiers are unchanged.
export function productTitle(title:string,lang:string){
 if(lang==='en')return title;
 return (titles as Record<string,Record<string,string>>)[title]?.[lang]||title;
}
