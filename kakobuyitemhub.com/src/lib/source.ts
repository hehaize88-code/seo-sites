import sourceCategories from '../content/categories.json';
import * as cheerio from 'cheerio';
export const origin='https://cnfanshm.com';
export const register='https://www.kakobuy.com/register/?affcode=9qtwd';
export const categories=[['All finds','全部商品',''],['Shoes','鞋履','shoes'],['Hoodies & sweaters','卫衣 / 毛衣','hoodie'],['T-shirts','T 恤','shirt'],['Jackets','夹克','jackets'],['Pants & shorts','长裤 / 短裤','pants'],['Accessories','配饰','accessories']];
export function photo(el:any){const raw=el.attr('data-src')||el.attr('src')||'';if(!raw||raw.startsWith('data:'))return '';try{const u=new URL(raw,origin);return u.protocol==='https:'?u.href:'';}catch{return '';}}
async function page(url:string){
 let last:unknown;
 for(let attempt=0;attempt<3;attempt++){
  try{
   const r=await fetch(url,{signal:AbortSignal.timeout(10000),headers:{'User-Agent':'KakobuyPreview/1.0'}});
   if(!r.ok){if(r.status<500&&r.status!==429)throw new Error('Source HTTP '+r.status);throw new Error('Source temporarily unavailable');}
   const html=await r.text();if(!html.trim())throw new Error('Source empty response');
   return cheerio.load(html);
  }catch(error){last=error;if(attempt<2)await new Promise(resolve=>setTimeout(resolve,350*(attempt+1)));}
 }
 console.error('Product source request failed after 3 attempts',last instanceof Error?last.message:'network error');
 throw new Error('Source unavailable');
}
export async function catalogue(query='',sort='new',category=''){
 query=query||category;
 let u=new URL('/index.php',origin);u.search=new URLSearchParams({m:'home',c:query?'Search':'Lists',a:query?'lists':'index',...(query?{keywords:query,channelid:'2'}:{tid:'1'}),sort:['new','click','price'].includes(sort)?sort:'new',sort_asc:'desc',ZXljbXM:'1'}).toString();
 // Categories use the source search service until category IDs are verified.
 if(query){u=new URL('/search.html',origin);u.search=new URLSearchParams({keywords:query,channelid:'2',sort:['new','click','price'].includes(sort)?sort:'new',sort_asc:'desc'}).toString();}
 const $=await page(u.href); const products:any[]=[];const seen=new Set();
 $('.product-card').each((_,e)=>{const el=$(e),path=el.find('a[href*="/AllProducts/"]').first().attr('href')||'',id=path.match(/\/(\d+)\.html/)?.[1];if(!id||seen.has(id))return;seen.add(id);products.push({id,title:el.find('.product-name').text().trim(),price:el.find('.product-price').first().text().trim(),image:photo(el.find('img').first()),source:origin+'/AllProducts/'+id+'.html'});});return products.slice(0,24);
}
export async function detail(id:string){if(!/^\d+$/.test(id))return null;const $=await page(origin+'/AllProducts/'+id+'.html');const root=$('.product-detail');const title=root.find('.product-title').text().trim();if(!title)return null;const images:string[]=[];root.find('.product-gallery img').each((_,e)=>{const p=photo($(e));if(p&&!images.includes(p))images.push(p);});const source=root.find('a.weidian-btn').attr('href')||'';let buy='';try{const u=new URL(source);if(['weidian.com','item.taobao.com','detail.1688.com'].includes(u.hostname)){const b=new URL('https://item2.kakobuy.com/item/details');b.searchParams.set('url',u.href);b.searchParams.set('affcode','rf8x8');buy=b.href;}}catch{}
 return {id,title,images,price:root.find('.product-price').first().text().trim(),source,buy,sourceId:root.find('.product-id').text().trim()};
}



export {sourceCategories};
export async function fullCatalogue(query='',sort='new',slug='all',number=1){
 const category=sourceCategories.find(c=>c.slug===slug);if(!category)throw new Error('Unknown category');
 const u=new URL(query?'/search.html':'/index.php',origin);
 u.search=new URLSearchParams(query?{keywords:query,channelid:'2',sort,sort_asc:'desc',page:String(number)}:{m:'home',c:'Lists',a:'index',tid:category.tid,sort,sort_asc:'desc',ZXljbXM:'1',page:String(number)}).toString();
 const $=await page(u.href);const products:any[]=[];const seen=new Set();
 $('.product-card').each((_,e)=>{const el=$(e),path=el.find('a[href*="/AllProducts/"]').first().attr('href')||'',id=path.match(/\/(\d+)\.html/)?.[1];if(!id||seen.has(id))return;seen.add(id);products.push({id,title:el.find('.product-name').text().trim(),price:el.find('.product-price').first().text().trim(),image:photo(el.find('img').first())});});
 const pagination=$('.pagination a').toArray().flatMap(e=>{const a=$(e),href=a.attr('href');if(!href)return [];const link=new URL(href,origin);const p=Number(link.searchParams.get('page')||link.pathname.match(/list_\d+_(\d+)/)?.[1]||1);return Number.isSafeInteger(p)&&p>0?[{number:p,label:a.text().trim()}]:[];});
 return {products,pagination};
}
