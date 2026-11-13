import Shop from './shop';
import {loadPage,pageMetadata} from '../lib/page-data';
type Props={searchParams:Promise<Record<string,string|undefined>>};
export async function generateMetadata({searchParams}:Props){return pageMetadata('/',await searchParams)}
export default async function Page({searchParams}:Props){return <Shop {...await loadPage('/',await searchParams)}/>}
