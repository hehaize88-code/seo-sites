import { load } from 'cheerio/slim';
import {sourceSearchQuery} from './product-names';

const ORIGIN = 'https://cnfanshm.com';
export const categoryIds = [1,4,5,6,7,8,9,10,11,12,15,13];
export type Product = {recordId:string;name:string;priceCny:number|null;image:string;images?:string[];itemId?:string;originalUrl?:string;hipobuyUrl?:string;platforms?:{name:string;url:string}[]};
export type Catalog = {products:Product[];hasNext:boolean;page:number;rate:number|null;error?:string};
export type ProductResult = {product:Product|null;rate:number|null;error?:string};

async function source(path:string) {
  const response = await fetch(new URL(path,ORIGIN), {headers:{'Accept':'text/html,application/javascript','User-Agent':'HipobuyDirectory/1.0'},cache:'no-store',signal:AbortSignal.timeout(18000)});
  if(!response.ok) throw new Error(`Source returned ${response.status}`);
  return response.text();
}
function imageUrl(value:string|undefined) {
  if(!value)return '';
  try { const u=new URL(value,ORIGIN); return ['cnfanshm.com','www.cnfanshm.com'].includes(u.hostname)&&u.pathname.startsWith('/uploads/')?u.href:'';}catch{return '';}
}
function safeLink(value:string|undefined){try{const u=new URL(value||'');return ['http:','https:'].includes(u.protocol)?u.href:'';}catch{return '';}}
function price(text:string){const n=Number(text.trim().replace(/[^\d.]/g,''));return text.trim()&&Number.isFinite(n)?n:null;}
async function rate(){try{const js=await source('/template/moban/pc/static/js/script.js?v=2.2.0');const n=Number(js.match(/CNY_TO_USD_RATE\s*=\s*([\d.]+)/)?.[1]);return n>0?n:null;}catch{return null;}}

export async function getCatalog(opts:{q?:string;category?:number;sort?:string;page?:number}={}):Promise<Catalog>{
  const page=Math.max(1,Math.min(300,Number(opts.page)||1));
  const upstreamPage=Math.floor((page-1)/3)+1;
  const offset=((page-1)%3)*20;
  const q=sourceSearchQuery((opts.q||'').trim().slice(0,160));
  const sort=opts.sort==='price-asc'?'price':opts.sort==='price-desc'?'price':'new';
  const dir=opts.sort==='price-asc'?'asc':'desc';
  const params=new URLSearchParams({m:'home',c:q?'Search':'Lists',a:q?'lists':'index',sort,sort_asc:dir,ZXljbXM:'1',page:String(upstreamPage)});
  if(q){params.set('keywords',q);params.set('channelid','2');}else params.set('tid',String(categoryIds.includes(opts.category||1)?opts.category||1:1));
  const ratePromise=rate();
  try {
    const html=await source('/index.php?'+params.toString());const $=load(html);const products:Product[]=[];
    $('.product-grid .product-card').each((_,card)=>{const el=$(card);const href=el.find('.product-image').attr('href')||'';const id=el.attr('data-id')||href.match(/\/(\d+)\.html/)?.[1];if(!id)return;const img=el.find('.product-image img');products.push({recordId:id,name:el.find('h3.product-name').text().trim(),priceCny:price(el.find('.product-price').first().text()),image:imageUrl(img.attr('data-src')||img.attr('src'))});});
    const hasNextUpstream=$('.pagination a[href]').toArray().some(a=>{const href=$(a).attr('href')||'';const match=href.match(/[?&]page=(\d+)/)||href.match(/list_\d+_(\d+)/);return match?Number(match[1])>upstreamPage:/下一页|Next/i.test($(a).text());});
    return {products:products.slice(offset,offset+20),hasNext:products.length>offset+20||hasNextUpstream,page,rate:await ratePromise};
  } catch(e){console.error('catalog source unavailable',e instanceof Error?e.message:'error');return{products:[],hasNext:false,page,rate:await ratePromise,error:'source-unavailable'};}
}

export async function getProduct(recordId:string,options:{legacyRate?:boolean}={}):Promise<ProductResult>{
  if(!/^\d{1,8}$/.test(recordId))return{product:null,rate:null,error:'not-found'};
  const ratePromise=options.legacyRate===false?Promise.resolve(null):rate();
  try{
    const $=load(await source(`/AllProducts/${recordId}.html`));
    const name=$('h1.product-title').text().trim();if(!name)return{product:null,rate:await ratePromise,error:'not-found'};
    const itemId=$('.product-id').first().text().match(/\d{5,}/)?.[0];
    const originalUrl=safeLink($('.weidian-btn').attr('href'));
    const images=[...new Set($('.product-gallery img').toArray().map(el=>imageUrl($(el).attr('data-src')||$(el).attr('src'))).filter(Boolean))];
    const platforms=$('.platform-option[href]').toArray().map(a=>({name:$(a).text().trim().replace(/\s+Link$/i,''),url:safeLink($(a).attr('href'))})).filter(p=>p.name&&p.url);
    const sourceHipo=platforms.find(p=>{try{return /(^|\.)hipobuy\.com$/.test(new URL(p.url).hostname);}catch{return false;}})?.url;
    const weidian=originalUrl.includes('weidian.com/')&&itemId;
    const hipobuyUrl=sourceHipo||(weidian?`https://hipobuy.com/goods/details?channel=WEIDIAN&id=${itemId}`:'');
    return{product:{recordId,name,priceCny:price($('.product-price').first().text()),image:images[0]||'',images,itemId,originalUrl,hipobuyUrl,platforms},rate:await ratePromise};
  }catch{return{product:null,rate:await ratePromise,error:'source-unavailable'};}
}
