import {translator} from './i18n';
import articles from '../content/articles.json';
export const guides=articles;
export const editorialCopy=(pair:string[],lang:string)=>translator(lang)(pair[0],pair[1]);
