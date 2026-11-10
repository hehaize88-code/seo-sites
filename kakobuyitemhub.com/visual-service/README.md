# Image search service — preview implementation

The user explicitly approved a feature index on 2026-11-10. cnfanshm does NOT have an existing visual-search service.

## Data boundary
- `.visual-index/index.json`: source product IDs, source image URLs, normalized 512-dimensional CLIP vectors; model/update metadata. No titles, prices, product copies, image files or uploaded images.
- `.visual-cache/`: downloaded public inference model files, not customer images. Ignored by Git.
- Result titles/prices are fetched live from cnfanshm product pages. Original images remain hosted there.
- User images decoded in memory and not written to disk. No external inference provider is called. Do not log request bodies.

## Current scope and quality
- 300 products, source catalogue pages 1–5, one listing image per product. Partial catalogue, not full-site or multi-photo indexing.
- CLIP image embeddings (Xenova/clip-vit-base-patch32 q8, CPU); cosine ranking. The 0.5 candidate cutoff is heuristic, not a calibrated confidence percentage. Maximum eight live-resolved results. Similarity does not guarantee identical goods.
- Six public API queries over three source products (6067,6041,5971), each original and 8% edge-cropped/recompressed, returned its ID first. Latency 2.1–3.8 seconds in these tests. This is a narrow retrieval sanity check, not an accuracy benchmark for arbitrary user photos.
- Invalid JPEG bytes return 400 and unsupported media type 415. Client limits input to 10 MB, resizes to 1024px JPEG; server limits payload to 5 MB and decoded images to 25M pixels. Single active inference and basic per-client rate limiting.
- Frontend supports upload/drop/paste, preview, cancel, retry, status, coverage count and result links. Eight locale translations included. Browser interaction testing remains unavailable; HTTP/build/API checks completed.

## Operation
`npm run visual:index` creates/resumes the 300-product feature index. It requires outbound access to cnfanshm and first-run model downloads from Hugging Face. `npm run visual:serve` runs the loopback inference API on port 4323. The explicit preview gateway routes only /api/visual POST and /api/visual/status GET to it; other preview pages go to Astro.

This is a local CPU-backed preview behind the existing temporary Cloudflare Tunnel. It is NOT a deployed Cloudflare Worker inference service. Permanent deployment requires an inference host or a separately evaluated CF-compatible inference option and scheduled index refresh. Do not assume installing these Node dependencies makes the CPU model runnable inside a Cloudflare Worker. No paid cloud resources have been created. Expand catalogue/gallery coverage and evaluate unrelated-photo rejection before production.

## Update: complete catalogue traversal
The fixed five-page cap is removed. The current builder follows source Next links, detects pagination cycles/repeated content, retries requests, reuses unchanged vectors and checkpoints progress. The current scan discovered 6027 eligible primary-image products in 101 pages. See progress.json rather than the historical 300-item section above for current coverage. Completion with image failures must be reported as incomplete coverage, and gallery images remain outside this index.
