import './globals.css';
export const metadata={metadataBase:new URL('https://superbuygrid.com'),title:'Superbuy Grid | Spreadsheet & Product Finds',description:'Browse product galleries, compare seller prices and open original listings with Superbuy.',robots:{index:true,follow:true},icons:{icon:'/favicon.svg?v=official-superbuy',apple:'/brand/apple-touch-icon.png'}};
export default function Layout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
