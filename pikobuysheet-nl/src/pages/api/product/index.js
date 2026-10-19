import{apiResponse}from'../../../lib/source.mjs';
export function GET({request}){if(import.meta.env.PROD)return Response.json({runtime:true});return apiResponse(new URL(request.url));}
