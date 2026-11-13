import {catalog,product} from './catalog';
import {langs,title,t,cat} from './i18n';
export async function loadPage(route:string,search:Record<string,string|undefined>){
 const lang=langs.includes(search.lang||'')?search.lang!:'en',category=search.category||'',q=search.q||'',page=Math.max(1,Number(search.page)||1);
 let data:any=null;
 try{if(route.startsWith('/product/'))data=await product(route.split('/')[2]);else if(route==='/'||route==='/spreadsheet')data=await catalog({home:route==='/',category,q,page})}catch{}
 return {initialRoute:route,initialLang:lang,initialCategory:category,initialQuery:q,initialPage:page,initialData:data};
}
export async function pageMetadata(route:string,search:Record<string,string|undefined>){
 const lang=langs.includes(search.lang||'')?search.lang!:'en';
 const keys:Record<string,string>={'/':'hero','/spreadsheet':'sheet','/categories':'categories','/image-search':'imageSearch','/guides':'guides','/shipping':'shipping','/qc':'qc','/faq':'faq','/saved':'saved'};
 let label=keys[route]?t(keys[route],lang):'Product';
 if(route.startsWith('/product/')){try{label=title((await product(route.split('/')[2])).name,lang)}catch{}}
 const canonical='https://superbuygrid.com'+route+(lang==='en'?'':'?lang='+lang);
 return {title:label+' | Superbuy Grid',alternates:{canonical,languages:Object.fromEntries([...langs.map(l=>[l,'https://superbuygrid.com'+route+(l==='en'?'':'?lang='+l)]),['x-default','https://superbuygrid.com'+route]])},robots:route==='/saved'||search.q?{index:false,follow:true}:{index:true,follow:true}};
}
