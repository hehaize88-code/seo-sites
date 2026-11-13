import Shop from '../shop';
import {loadPage,pageMetadata} from '../../lib/page-data';
import {notFound} from 'next/navigation';
type Props={params:Promise<{path:string[]}>,searchParams:Promise<Record<string,string|undefined>>};
const allowed=['/spreadsheet','/categories','/image-search','/guides','/shipping','/qc','/faq','/saved'];
export async function generateMetadata({params,searchParams}:Props){return pageMetadata('/'+(await params).path.join('/'),await searchParams)}
export default async function Page({params,searchParams}:Props){const route='/'+(await params).path.join('/');if(!allowed.includes(route)&&!/^\/product\/\d{1,10}$/.test(route))notFound();return <Shop {...await loadPage(route,await searchParams)}/>}
