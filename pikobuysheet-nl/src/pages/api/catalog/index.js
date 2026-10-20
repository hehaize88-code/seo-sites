import{apiResponse}from'../../../lib/source.mjs';
// Astro's preview route; the published Worker handles this endpoint live.
export function GET({request}){if(import.meta.env.PROD)return Response.json({runtime:true});return apiResponse(new URL(request.url));}
