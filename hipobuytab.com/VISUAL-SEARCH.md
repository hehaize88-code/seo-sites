# Image search

This preview searches derived visual features of cnfanshm.com catalog cover images. It does not create a product database, image library, upload service, or administration system. Names, prices, photos and purchase URLs are retrieved from the existing live source adapter when displaying results.

The user's image is decoded, resized and processed in a browser Web Worker. Example photos reuse their existing descriptors for the same similarity ranking, without downloading the model or proxying images. A source-image URL hash guards against stale examples. The photo is never posted to a server. The browser downloads a pinned DINOv2-small q8 model and ONNX Runtime, plus a compact image-feature index. The first use transfers approximately 50 MB; subsequent searches reuse the model session and browser cache. This requires a recent browser with WebAssembly SIMD, Web Workers and OffscreenCanvas. Inference runs with one WASM thread and needs no cross-origin isolation.

## Index format and limits

`public/visual/index.json` contains model provenance, build time, coverage counts, a content-addressed vector filename, source record IDs, and hashes of the source image URLs. The binary file stores 384-dimensional quantized CLS features. No product titles, prices, images, credentials or user data are stored in these files. The model is pinned to Xenova/dinov2-small revision `c2bb04a51fab207c420665f1946016107bffc701`; model weights originate from Meta DINOv2 (Apache 2.0). Runtime license files accompany the artifacts.

Results rank cosine similarity, not an identity probability. Search covers source catalog cover images included in the current index, not all marketplace inventory. New source items become searchable after rebuilding the index. Failed image records are counted rather than fabricated. Product removals and price changes are respected at result rendering through the live source adapter. Selecting a result opens the existing localized detail page, including currency conversion and buying links.

## Rebuild

1. Install dependencies using the Sites dependency helper with `ONNXRUNTIME_NODE_INSTALL_CUDA=skip` (the CPU runtime is sufficient).
2. Run `node scripts/prepare-visual-model.mjs` to fetch the pinned model and copy its runtime assets.
3. For a fresh source scan, delete the rebuildable `work/visual/catalog.json` checkpoint, then run `node scripts/build-visual-index.mjs`. Existing feature checkpoints are reused when record IDs and source image URLs agree. Delete `work/visual/vectors.jsonl` for a full refresh when images change at an unchanged URL.
4. Check the `indexedCount`, `catalogCount`, `failedCount`, and `complete` fields. The script records image failures in ignored `work/visual/failures.json`.
5. Run the type check and build, then publish the normal Site archive. The index is delivered as static files; there is no hosted database or recurring paid inference API.

The crawler follows the source's pagination to completion, with bounded image prefetching and retries. Its working files are ignored. Keep source scraping and feature generation out of request-time handlers and Cloudflare Worker builds.

## Validation

`node --experimental-strip-types scripts/test-visual-search.mjs` checks actual source-photo and cropped-photo retrieval against downloaded public test fixtures in `/workspace/shared/hipobuy-search-tests`. Fixtures are test-only, are not deployed, and must be freshly fetched when reproducing the test. It also checks malformed indices and empty descriptors. Browser QA exercises file selection, cancellation, empty image validation, example search, and result links. No synthetic product data is used.
