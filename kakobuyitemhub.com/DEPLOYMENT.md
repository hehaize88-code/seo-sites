# kakobuyitemhub.com deployment preparation

Target repository: hehaize88-code/seo-sites, folder kakobuyitemhub.com. Preserve all other domain folders.

1. Wrangler OAuth is authenticated to account 9010cea800ac2a140509889d88fe612e. Cloudflare connector remains unavailable; use Wrangler.
2. Run npm ci and npm run build, with no PREVIEW_SOURCE_BRIDGE. This source has no loopback source bridge.
3. Upload Worker using generated dist/server/wrangler.json without custom domains first. Test workers.dev catalogue, search, category pagination, product detail, official assets, GA4, mobile and article routes.
4. Image-search production hosting is unresolved: visual-service runs CPU CLIP on the local machine; no persistent public inference endpoint is configured. Do not claim deployment complete or bind the domain until this is resolved or the user explicitly accepts a different launch scope. Do not point production at the temporary tunnel.
5. Once staging passes, inspect DNS before adding both custom domains from wrangler.domains.json; merge routes into Wrangler config and rebuild/deploy. Preserve existing unrelated DNS/rules.
6. Middleware returns HTTP301 from www to apex, preserving pathname and query. Confirm www HTTPS certificate, HTTP/HTTPS redirects and root HTTPS200 externally. Redirect code is deployed to staging but custom domains are not yet attached.
7. Preview hosts remain noindex; apex pages use canonical domain and indexable robots. Search/results and untranslated locales remain noindex. Validate sitemap/robots and canonical on deployed hostname before signoff.

The copied visual-service and local image index are not a new product database. No model/index/cache/credentials are included in this deployment folder. Product data remains live from cnfanshm.com.

