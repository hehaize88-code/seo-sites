import assert from 'node:assert/strict';
import {catalogParams,catalogUrl} from '../src/lib/catalog-state.mjs';
import {categoryRoute,categorySuffix} from '../src/lib/catalog-routes.mjs';

assert.equal(catalogParams('spreadsheet/shoes','?sort=price-asc&page=2&product=6045').toString(),'sort=price-asc&page=2&category=shoes');
assert.equal(catalogParams('spreadsheet/tshirts','?category=shoes').get('category'),'tshirts');
assert.equal(catalogParams('spreadsheet','?category=jackets').get('category'),'jackets');
assert.equal(catalogParams('spreadsheet/shoes','?q=hoodie&category=shoes').get('category'),null);
assert.equal(catalogParams('spreadsheet','?q=%20%20&category=jackets').get('category'),'jackets');
const next=catalogUrl('https://pikobuysheet.nl/de/spreadsheet/shoes/?product=6045&sort=popular',{page:2});
assert.equal(next.pathname,'/de/spreadsheet/shoes/');
assert.equal(next.search,'?sort=popular&page=2');
assert.equal(catalogParams('spreadsheet/shoes',next.search).get('category'),'shoes');
assert.equal(catalogUrl(next,{page:1}).search,'?sort=popular');
assert.equal(categoryRoute('shoes')+categorySuffix('shoes'),'spreadsheet/shoes');
assert.equal(categoryRoute('jackets')+categorySuffix('jackets'),'spreadsheet?category=jackets');
assert.equal(categoryRoute('all')+categorySuffix('all'),'spreadsheet');
console.log('PASS: clean category routes, legacy filters, search reset, sorting and pagination retain the correct category.');
