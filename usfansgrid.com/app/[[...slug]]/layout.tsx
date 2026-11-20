import Script from 'next/script';
import { localeOf } from '../../lib/i18n';
import '../globals.css';

const measurementId = 'G-PTM0C3JGRP';

export default async function Layout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ slug?: string[] }>;
}) {
  const { slug = [] } = await params;
  return (
    <html lang={localeOf(slug[0])}>
      <body>
        {children}
        <Script src={`https://www.googletagmanager.com/gtag/js?id=${measurementId}`} />
        <Script id="usfansgrid-analytics">
          {`window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '${measurementId}');`}
        </Script>
      </body>
    </html>
  );
}
