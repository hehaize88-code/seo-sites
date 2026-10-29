import {landingCategories} from './catalog-routes.mjs';

export function catalogParams(route, search) {
  const params = new URLSearchParams(search);
  params.delete('product');
  const category = route.startsWith('spreadsheet/') ? route.split('/')[1] : null;
  if (params.get('q')?.trim()) params.delete('category');
  else if (landingCategories.includes(category)) params.set('category', category);
  return params;
}

export function catalogUrl(currentUrl, values) {
  const url = new URL(currentUrl);
  for (const [key, value] of Object.entries(values)) {
    if (value && value !== 'all' && !(key === 'page' && value === 1)) url.searchParams.set(key, String(value));
    else url.searchParams.delete(key);
  }
  url.searchParams.delete('product');
  return url;
}
