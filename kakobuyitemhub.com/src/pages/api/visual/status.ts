import type {APIRoute} from 'astro';import status from '../../../content/visual-status.json';
export const GET:APIRoute=()=>Response.json({...status,mode:'browser'},{headers:{'Cache-Control':'public, max-age=300'}});
