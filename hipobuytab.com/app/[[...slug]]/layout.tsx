import type {Metadata} from 'next';
import {localeOf} from '@/lib/i18n';
import '../globals.css';
export const metadata:Metadata={title:'Hipobuy Spreadsheet — Finds, Photos & Buying Guides',description:'Browse product finds, compare original photos and prices, and open listings in Hipobuy.',metadataBase:new URL('https://hipobuytab.com'),robots:{index:true,follow:true},icons:{icon:[{url:'/brands/hipobuy/favicon.png',type:'image/png',sizes:'32x32'}]}};
export default async function Layout({children,params}:{children:React.ReactNode;params:Promise<{slug?:string[]}>}){const {slug}=await params;return <html lang={localeOf(slug?.[0])}><body>{children}</body></html>}
