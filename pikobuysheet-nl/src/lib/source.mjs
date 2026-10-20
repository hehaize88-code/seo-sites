import {load} from 'cheerio/slim';
import {site, categories, purchaseUrl} from '../site.config.mjs';

const cache = new Map(), pending = new Map();
const TTL = 300_000;
export class SourceError extends Error { constructor(message, status=503) { super(message); this.status=status; } }
export async function fetchSource(path) {
  const url = new URL(path, site.source);
  if (!['www.cnfanshp.com','cnfanshp.com'].includes(url.hostname) || url.protocol !== 'https:') throw new SourceError('Invalid source',400);
  const key=url.href, existing=cache.get(key);
  if(existing && existing.until > Date.now()) return existing.value;
  if(pending.has(key)) return pending.get(key);
  const task=(async()=>{
    const r=await fetch(url,{signal:AbortSignal.timeout(15000),redirect:'follow'});
    if(!r.ok) throw new SourceError(`Source returned ${r.status}`, r.status===404?404:503);
    const value=await r.text();
    if(value.length>2_000_000 || /error code: 10\d\d|Just a moment\.\.\.|cf-chl-platform/.test(value)) throw new SourceError('Source unavailable');
    if(cache.size>=120) cache.delete(cache.keys().next().value);
    cache.set(key,{until:Date.now()+TTL,value}); return value;
  })().catch(e=>{throw e instanceof SourceError?e:new SourceError('Source timeout or network error');}).finally(()=>pending.delete(key));
  pending.set(key,task);return task;
}
let rateCache;
export async function rateFor($) {
  if(rateCache && rateCache.until>Date.now())return rateCache.value;
  const path=$('script[src]').map((_,el)=>$(el).attr('src')).get().find(s=>/\/template\/moban\/pc\/static\/js\/script\.js/.test(s));
  if(!path) throw new SourceError('Price conversion unavailable');
  const script=await fetchSource(path);
  const rate=Number(script.match(/\bCNY_TO_USD_RATE\s*=\s*(\d+(?:\.\d+)?)/)?.[1]);
  if(!Number.isFinite(rate)||rate<=0||rate>100)throw new SourceError('Price conversion unavailable');
  rateCache={value:rate,until:Date.now()+TTL};return rate;
}
function usd(text,rate){const raw=String(text).replace(/[^\d.-]/g,'');if(!raw)return null;const n=Number(raw);return Number.isFinite(n)?Number((text.includes('$')?n:n/rate).toFixed(2)):null;}
function imageUrl(raw){
  if(!raw || raw.startsWith('data:'))return null;
  const u=new URL(raw,site.source);
  return ['cnfanshp.com','www.cnfanshp.com'].includes(u.hostname)&&u.pathname.startsWith('/uploads/')?u.href:null;
}
export function parseCards(html,rate){
  const $=load(html);const products=[];
  $('.product-grid .product-card').each((_,el)=>{
    const card=$(el), href=card.find('a.product-image').attr('href')||'', id=href.match(/\/AllProducts\/(\d+)\.html/)?.[1];
    const img=card.find('.product-image img').first();const image=imageUrl(img.attr('data-src')||img.attr('src'));
    if(!id)return;
    products.push({id,title:card.find('.product-name').text().trim(),image,price:usd(card.find('.product-price').text().trim(),rate),currency:'USD',views:Number(card.find('.product-views span').text().trim())||0,date:Number(card.attr('data-date'))||0,sourceUrl:new URL(href,site.source).href});
  });return products;
}
export async function getCatalog({category='all',q='',sort='new',page=1}={}){
  const cat=categories.find(c=>c[0]===category)||categories[0];
  q=String(q).trim().slice(0,100);page=Math.max(1,Math.min(10000,Math.floor(Number(page)||1)));
  if(!['new','popular','price-asc','price-desc'].includes(sort))sort='new';
  const sourcePage=Math.floor((page-1)/3)+1, offset=((page-1)%3)*site.pageSize;
  const key=sort==='popular'?'click':sort.startsWith('price')?'price':'new';
  const direction=sort==='price-asc'?'asc':'desc';
  let u;
  if(q){
    // The upstream sort query loses the keyword filter. Read the real matching
    // pages first, then sort that complete set; never sort just one visible page.
    const searchUrl=n=>{const v=new URL('/search.html',site.source);v.search=new URLSearchParams({keywords:q,channelid:'2',page:String(n)}).toString();return v.href;};
    if(sort!=='new'){
      const first=await fetchSource(searchUrl(1)),$=load(first),rate=await rateFor($);
      const total=Number($('#search-count').text().replace(/[^\d]/g,''));
      if(!Number.isFinite(total)||!$('#search-count').length)throw new SourceError('Unrecognised source response');
      // Bound traffic to the origin. Broad searches ask the visitor to refine.
      if(total>1200)throw new SourceError('search_too_broad',422);
      const pages=Math.ceil(total/60),all=parseCards(first,rate);let last=first;
      for(let start=2;start<=pages;start+=3){const batch=await Promise.all(Array.from({length:Math.min(3,pages-start+1)},(_,i)=>fetchSource(searchUrl(start+i))));batch.forEach(h=>{const pageRoot=load(h);if(!pageRoot('.product-grid').length)throw new SourceError('Incomplete source search');all.push(...parseCards(h,rate));last=h;});}
      const unique=[...new Map(all.map(p=>[p.id,p])).values()];
      const lastRoot=load(last);if(lastRoot('.pagination a').toArray().some(el=>/下一页|next/i.test(lastRoot(el).text())&&lastRoot(el).attr('href')))throw new SourceError('Incomplete source search');
      unique.sort(sort==='popular'?(a,b)=>b.views-a.views||b.date-a.date:sort==='price-asc'?(a,b)=>(a.price??Infinity)-(b.price??Infinity):(a,b)=>(b.price??-Infinity)-(a.price??-Infinity));
      const begin=(page-1)*site.pageSize;
      return{products:unique.slice(begin,begin+site.pageSize),page,pageSize:site.pageSize,hasNext:begin+site.pageSize<unique.length,total:unique.length,sourceReportedTotal:total,category:'all',q,sort,sourceUrl:searchUrl(1),updatedAt:new Date().toISOString()};
    }
    u=new URL(searchUrl(sourcePage));
  }
  else {
    const base=await fetchSource(cat[1]);const $=load(base);
    const action=$('.sort-btn').map((_,el)=>$(el).attr('onclick')||'').get().find(t=>t.includes('tid='));
    const tid=action?.match(/[?&]tid=(\d+)/)?.[1];
    if(!tid)throw new SourceError('Category unavailable');
    u=new URL('/index.php',site.source);u.search=new URLSearchParams({m:'home',c:'Lists',a:'index',tid,sort:key,sort_asc:direction,ZXljbXM:'1',page:String(sourcePage)}).toString();
  }
  const html=await fetchSource(u.href), $=load(html);
  if(!$('.product-grid').length&&!$('.search-results').length)throw new SourceError('Unrecognised source response');
  const rate=await rateFor($), all=parseCards(html,rate), products=all.slice(offset,offset+site.pageSize);
  const next=$('.pagination a').toArray().some(el=>{const href=$(el).attr('href');if(!href||!/下一页|next/i.test($(el).text()))return false;try{return Number(new URL(href,site.source).searchParams.get('page'))>sourcePage;}catch{return false;}});
  const countText=$('#search-count').text().trim(), total=countText?Number(countText.replace(/[^\d]/g,'')):null;
  return {products,page,pageSize:site.pageSize,hasNext:offset+site.pageSize<all.length||next,total:total||null,category:q?'all':cat[0],q,sort,sourceUrl:u.href,updatedAt:new Date().toISOString()};
}
export async function getProduct(id){
  if(!/^\d{1,10}$/.test(id||''))throw new SourceError('Invalid product',400);
  const html=await fetchSource(`/AllProducts/${id}.html`),$=load(html), root=$('.product-detail');
  if(!root.length)throw new SourceError('Product not found',404);
  const link=root.find('a.weidian-btn').attr('href'), productId=link?new URL(link).searchParams.get('itemID'):root.find('.product-id').text().match(/\d{6,20}/)?.[0];
  const rate=await rateFor($);
  const images=[...new Set(root.find('.product-gallery img').map((_,el)=>imageUrl($(el).attr('data-src')||$(el).attr('src'))).get().filter(Boolean))];
  return {id,productId,title:root.find('.product-title').text().trim(),images,price:usd(root.find('.product-price').first().text().trim(),rate),currency:'USD',buyUrl:purchaseUrl(productId),sourceUrl:new URL(`/AllProducts/${id}.html`,site.source).href,qcImages:[],qcAvailable:false,updatedAt:new Date().toISOString()};
}
export async function apiResponse(url){
  try{
    const data=url.pathname.replace(/\/$/,'')==='/api/product'?await getProduct(url.searchParams.get('id')):await getCatalog(Object.fromEntries(url.searchParams));
    return Response.json(data,{headers:{'Cache-Control':'public, max-age=60, s-maxage=300','X-Content-Type-Options':'nosniff'}});
  }catch(e){return Response.json({error:e.status===422?'search_too_broad':e.status===404?'not_found':'source_unavailable',reason:e.message},{status:e.status||503,headers:{'Cache-Control':'no-store','Retry-After':'60'}});}
}
