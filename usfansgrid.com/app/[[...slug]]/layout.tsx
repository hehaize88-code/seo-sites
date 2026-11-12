import {localeOf} from '../../lib/i18n';
import '../globals.css';
export default async function Layout({children,params}:{children:React.ReactNode;params:Promise<{slug?:string[]}>}){const {slug=[]}=await params;return <html lang={localeOf(slug[0])}><body>{children}</body></html>;}
