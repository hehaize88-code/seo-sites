import articles from '../content/articles.json';
export const guides=articles;
export const editorialCopy=(pair:string[],lang:string)=>pair[lang==='zh'?1:0];
