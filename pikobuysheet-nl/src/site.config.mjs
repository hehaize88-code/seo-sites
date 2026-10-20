export const site = {
  domain: 'https://pikobuysheet.nl',
  title: 'PikobuySheet',
  source: 'https://www.cnfanshp.com',
  register: 'https://www.pikobuy.com/?mode=register&redirect=/home',
  pageSize: 20,
};
export const categories = [
  ['all','/AllProducts/'],['shoes','/shoes/'],['sweatshirts','/hoodies-sweaters/'],
  ['tshirts','/t-shirts/'],['jackets','/jackets/'],['pants','/pants-shorts/'],
  ['headwear','/headwear/'],['accessories','/accessories/'],['sets','/short-sets/'],
  ['electronics','/electronics/'],['other','/other-stuff/'],['jerseys','/jersey/'],
];
export function purchaseUrl(productId) {
  if (!/^\d{6,20}$/.test(productId || '')) return null;
  const url = new URL('https://www.pikobuy.com/product/detail');
  url.searchParams.set('productUrl', `https://weidian.com/item.html?itemID=${productId}`);
  return url.toString();
}
