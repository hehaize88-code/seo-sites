import type {Metadata} from 'next';
import {localeOf} from '@/lib/i18n';
import '../globals.css';

export const metadata:Metadata={title:'Hipobuy Spreadsheet — Finds, Photos & Buying Guides',description:'Browse product finds, compare original photos and prices, and open listings in Hipobuy.',metadataBase:new URL('https://hipobuytab.com'),robots:{index:true,follow:true},icons:{icon:[{url:'/brands/hipobuy/favicon.png',type:'image/png',sizes:'32x32'}]}};

const googleAnalytics = `
if (!window.__hipobuyGa4 && /^(www\\.)?hipobuytab\\.com$/.test(window.location.hostname)) {
  window.__hipobuyGa4 = true;
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function(){window.dataLayer.push(arguments);};
  window.gtag('js', new Date());
  var tag = document.createElement('script');
  tag.async = true;
  tag.src = 'https://www.googletagmanager.com/gtm.js?id=GTM-PHGNPKB4';
  document.head.appendChild(tag);
}
`;

export default async function Layout({children,params}:{children:React.ReactNode;params:Promise<{slug?:string[]}>}) {
  const {slug}=await params;
  return (
    <html lang={localeOf(slug?.[0])}>
      <head>
        <script id="hipobuy-google-analytics" dangerouslySetInnerHTML={{__html:googleAnalytics}} />
      </head>
      <body>{children}</body>
    </html>
  );
}
