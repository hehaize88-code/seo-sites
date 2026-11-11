import {getCatalog,getProduct} from '@/lib/catalog';
import {localeOf,locales,copy} from '@/lib/i18n';
import {visualCopy} from '@/lib/visual/copy';
import {getExchange} from '@/lib/exchange';
import {localizeProductName} from '@/lib/product-names';
import Storefront from '@/components/storefront';
import {notFound} from 'next/navigation';
import {editorial} from '@/lib/editorial';
const origin='https://hipobuytab.com';
const pagePath=(lang:string,segments:string[])=>!segments.length&&lang==='en'?'/':'/'+[lang,...segments].join('/');
export const dynamic='force-dynamic';
export async function generateMetadata({params,searchParams}:{params:Promise<{slug?:string[]}>;searchParams:Promise<Record<string,string|undefined>>}){
 const {slug=[]}=await params;const locale=localeOf(slug[0]);const t=copy[locale];const section=slug[1]||'home';const names:Record<string,string>={home:t.spreadsheet,spreadsheet:t.spreadsheet,categories:t.categories,guides:t.guides,articles:t.articles,shipping:t.shipping,qc:t.qc,faq:t.faq,product:t.details,'image-search':visualCopy[locale].nav};
 const detail=section==='product'?await getProduct(slug[2]||''):null;
 const pageTitle=detail?.product?localizeProductName(detail.product.name,locale):names[section]||t.spreadsheet;
 const query=await searchParams;const segments=slug.slice(1);const canonical=origin+pagePath(locale,segments);
 const guide=editorial[locale].guides.find(g=>g.slug===slug[2]);
 return {title:`${guide?.title||pageTitle} | Hipobuy Tab`,description:guide?.summary||t.heroDesc,
 alternates:{canonical,languages:Object.fromEntries([...locales.map(l=>[l,origin+pagePath(l,segments)]),['x-default',origin+pagePath('en',segments)]])},
 robots:{index:!query.q&&!query.sort&&!query.page&&!query.category,follow:true},openGraph:{title:`${guide?.title||pageTitle} | Hipobuy Tab`,description:guide?.summary||t.heroDesc,url:canonical,type:'website'}};
}
export default async function Page({params,searchParams}:{params:Promise<{slug?:string[]}>;searchParams:Promise<Record<string,string|undefined>>}){
 const {slug=[]}=await params;const p=await searchParams;
 if(slug.length&& !locales.includes(slug[0] as never))notFound();
 const locale=localeOf(slug[0]);const section=slug[1]||'home';
 if(!['home','spreadsheet','categories','product','guides','articles','faq','shipping','qc','image-search'].includes(section))notFound();
 if(slug.length>3||(slug.length===3&&!['product','guides'].includes(section)))notFound();
 if(section==='guides'&&slug[2]&&!editorial[locale].guides.some(g=>g.slug===slug[2]))notFound();
 const exchangePromise=getExchange();
 const catalog=['home','spreadsheet','categories'].includes(section)?await getCatalog({q:p.q,category:Number(p.category)||1,sort:p.sort,page:Number(p.page)||1}):null;
 const detail=section==='product'?await getProduct(slug[2]||''):null;
 if(section==='product'&&detail?.error==='not-found')notFound();
 return <Storefront key={slug.join('/')+JSON.stringify(p)} locale={locale} section={section} slug={slug[2]} query={p} initialCatalog={catalog} initialDetail={detail} initialExchange={await exchangePromise}/>;
}
