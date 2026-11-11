import categories from '../content/categories.json';
import {translator} from './i18n';
// Translate source category labels without changing brand/model names or item numbers.
export function productTitle(title:string,lang:string){
 if(lang==='en')return title;
 const t=translator(lang);
 const terms=[...categories.filter(c=>c.slug!=='all').map(c=>[c.label,c.zh]),['T-shirts','T 恤'],['Hoodies','卫衣'],['Sweaters','毛衣']];
 for(const [en,zh] of terms.sort((a,b)=>b[0].length-a[0].length)){
  const escaped=en.replace(/[.*+?^${}()|[\\]\\]/g,'\\$&');
  const pattern=new RegExp('(^|[^a-zA-Z])('+escaped+')(?=$|[^a-zA-Z])','gi');
  title=title.replace(pattern,(_,prefix)=>prefix+t(en,zh));
 }
 return title;
}
