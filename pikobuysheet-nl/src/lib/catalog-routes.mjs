// Publish only three focused category landing pages initially. Other filters
// remain useful catalog controls without multiplying indexable thin pages.
export const landingCategories = ['shoes', 'sweatshirts', 'tshirts'];
export function categoryRoute(key) {
  return landingCategories.includes(key) ? `spreadsheet/${key}` : 'spreadsheet';
}
export function categorySuffix(key) {
  return key === 'all' || landingCategories.includes(key) ? '' : `?category=${key}`;
}
