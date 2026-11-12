import {notFound} from 'next/navigation';
import {headers} from 'next/headers';
import {SITE_ORIGIN,isProductionHost,languageAlternates} from '../../lib/site';
import type {Metadata} from 'next';
import {getCatalog,getProduct,Product,Catalog} from '../../lib/catalog';
import {localeOf,locales,t} from '../../lib/i18n';
import {localizeProductName} from '../../lib/product-names';
import Storefront from '../../components/storefront';
type Props={params:Promise<{slug?:string[]}>;searchParams:Promise<Record<string,string|string[]|undefined>>};
export async function generateMetadata({params,searchParams}:Props):Promise<Metadata>{
 const {slug=[]}=await params,query=await searchParams,l=localeOf(slug[0]),page=slug[1]||'home';
 let title=t(l,page==='how-to-buy'?'how':page==='image-search'?'imageSearch':page==='home'?'edition':page);
 if(page==='product'&&slug[2]){const result=await getProduct(slug[2]);title=result.product?localizeProductName(result.product.name,l):t(l,'missing');}
 const path=slug.slice(1).join('/'),canonical=SITE_ORIGIN+'/'+l+(path?'/'+path:'');
 const index=isProductionHost((await headers()).get('host'))&&page!=='saved'&&!query.q&&!query.category&&!query.sort&&!query.page;
 return {title:`${title} | USFans Grid`,description:t(l,'intro'),alternates:{canonical,languages:languageAlternates(path)},robots:{index,follow:true},icons:{icon:'/favicon.png'},openGraph:{title:`${title} | USFans Grid`,description:t(l,'intro'),url:canonical,type:'website'}};
}
export default async function Page({params,searchParams}:Props){
 const {slug=[]}=await params,query=await searchParams;if(slug.length&& !locales.includes(slug[0] as any))notFound();
 const locale=localeOf(slug[0]),page=slug[1]||'home';if(!['home','spreadsheet','categories','product','qc','shipping','faq','guides','how-to-buy','saved','about','privacy','image-search'].includes(page))notFound();
 const q=String(query.q||''),category=String(query.category||'all'),sort=String(query.sort||'new'),currentPage=Number(query.page)||1;
 let catalog:Catalog={products:[],page:currentPage,hasNext:false};let product:Product|null=null,error:string|undefined;
 if(page==='product'){if(slug.length!==3)notFound();const result=await getProduct(slug[2]);product=result.product;error=result.error;if(!product&&error==='not-found')notFound();}
 else if(['home','spreadsheet','categories'].includes(page))catalog=await getCatalog({q:page==='spreadsheet'?q:'',category:page==='spreadsheet'?category:'all',sort:page==='spreadsheet'?sort:'new',page:page==='spreadsheet'?currentPage:1});
 return <Storefront locale={locale} page={page} catalog={catalog} product={product} error={error} q={q} category={category} sort={sort}/>;
}
