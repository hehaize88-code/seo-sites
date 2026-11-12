import {load} from 'cheerio/slim';
const origin='https://cnfanshm.com';
export function sourceImage(value){try{const u=new URL(value||'',origin);return ['cnfanshm.com','www.cnfanshm.com'].includes(u.hostname)&&u.pathname.startsWith('/uploads/')?u.href:'';}catch{return '';}}
export function parseSourceDetail(html,id){
 const $=load(html),name=$('h1.product-title').text().trim();if(!name)return null;
 const images=[...new Set($('.product-gallery img, .product-description img').toArray().map(el=>sourceImage($(el).attr('data-src')||$(el).attr('src'))).filter(Boolean))];
 const safeLink=value=>{try{const u=new URL(value||'');return ['https:','http:'].includes(u.protocol)?u.href:'';}catch{return '';}};
 const originalUrl=safeLink($('.weidian-btn').attr('href'));
 const itemId=$('.product-id').first().text().match(/\d{5,}/)?.[0];
 const platforms=$('.platform-option[href]').toArray().map(a=>({name:$(a).text().trim().replace(/\s+Link$/i,''),url:safeLink($(a).attr('href'))})).filter(p=>p.name&&p.url);
 const priceText=$('.product-price').first().text().trim(),priceValue=Number(priceText.replace(/[^\d.]/g,''));
 return {recordId:String(id),name,priceCny:priceText&&Number.isFinite(priceValue)?priceValue:null,image:images[0]||'',images,itemId,originalUrl,platforms,buyUrl:itemId&&/^https?:\/\/(?:www\.)?weidian\.com\//.test(originalUrl)?'https://www.usfans.com/product/3/'+itemId:undefined};
}
