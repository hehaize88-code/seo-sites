"""Build full local-language article drafts with official Argos models.

Model files are downloaded separately from argosopentech/argospm-index.
Generated translations are checked into this repository; production is static.
"""
import argparse
import concurrent.futures
import html
import json
import os
from pathlib import Path
import re
import time

os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import ctranslate2
import sentencepiece
from bs4 import BeautifulSoup, Comment

BASE = Path(__file__).resolve().parent
LANGS = ['de', 'fr', 'es', 'it', 'pl', 'nl', 'pt']
KEEP = re.compile(r'CSSBuys Store|CSSBuy|CSSBuys|Taobao|Weidian|Tmall|Yupoo|1688|cnfanssp\.com|USD|CNY|EUR|QC|W2C|Jordan|LACOSTE|Dior|Balenciaga|AMIRI|Louis Vuitton|Monogram|Gucci|Revenge|Moose Knuckles|[0-9]+(?:[.,][0-9]+)*')

def segments(text):
    # Sentence boundaries only; decimals and product identifiers remain intact.
    return re.split(r'(?<=[.!?])\s+(?=[A-Z“"0-9])', text)

def translate_language(lang, model_root):
    started = time.time()
    model = next((Path(model_root) / lang).rglob('model.bin')).parent.parent
    if (model / 'sentencepiece.model').exists():
        sp = sentencepiece.SentencePieceProcessor(model_file=str(model / 'sentencepiece.model'))
        encode = lambda s: sp.encode(s, out_type=str)
        decode = sp.decode
    else:
        from sacremoses import MosesTokenizer, MosesDetokenizer, MosesPunctNormalizer
        from subword_nmt.apply_bpe import BPE
        tokenizer = MosesTokenizer('en')
        detokenizer = MosesDetokenizer(lang)
        normalizer = MosesPunctNormalizer('en')
        with (model / 'bpe.model').open() as f:
            bpe = BPE(f)
        encode = lambda s: bpe.segment_tokens(tokenizer.tokenize(normalizer.normalize(s)))
        decode = lambda tokens: detokenizer.detokenize(' '.join(tokens).replace('@@ ', '').split(' '))
    tr = ctranslate2.Translator(str(model / 'model'), device='cpu', compute_type='int8', intra_threads=1, inter_threads=1)
    target = BASE / 'articles' / lang
    target.mkdir(parents=True, exist_ok=True)
    cache_file = BASE / 'translations' / f'{lang}.json'
    cache_file.parent.mkdir(exist_ok=True)
    cache = json.loads(cache_file.read_text()) if cache_file.exists() else {}
    overrides = json.loads((BASE / 'translation-overrides.json').read_text()).get(lang, {})
    cache.update(overrides)
    meta = json.loads((BASE / 'articles.json').read_text())
    source_strings = []
    soups = {}
    for slug in meta:
        soup = BeautifulSoup((BASE / 'articles' / 'en' / f'{slug}.html').read_text(), 'html.parser')
        soups[slug] = soup
        for node in soup.find_all(string=True):
            if isinstance(node, Comment) or node.parent.name in ['script', 'style']:
                continue
            text = str(node).strip()
            if re.search('[A-Za-z]', text):
                source_strings.append(text)
        source_strings.extend([meta[slug]['title'], meta[slug]['description']])
    extra = BASE / 'ui-source.json'
    if extra.exists():
        source_strings.extend(json.loads(extra.read_text()))
    source_strings = list(dict.fromkeys(source_strings))
    sentences = list(dict.fromkeys(s for text in source_strings for s in segments(text) if s not in cache))
    print(lang, 'pending sentences', len(sentences), flush=True)
    for start in range(0, len(sentences), 24):
        batch = sentences[start:start+24]
        tokens = [encode(s) for s in batch]
        results = tr.translate_batch(tokens, beam_size=3, max_batch_size=24, max_decoding_length=320, repetition_penalty=1.05)
        for source, result in zip(batch, results):
            translated = html.unescape(decode(result.hypotheses[0]).replace('▁', ' ')).strip()
            # Preserve literal platform spelling; translated grammar remains untouched.
            translated = re.sub(r'CSS\s*Buy|CssBuy|CSSbuy|CSSBUY|Cssbuy|CSS Acheter|CSS Compra|CSS kaufen', 'CSSBuy', translated)
            translated = re.sub(r'CSSBuys\s+Store', 'CSSBuys Store', translated)
            if not translated.strip():
                raise ValueError(f'Empty translation: {lang}: {source}')
            cache[source] = translated
        cache_file.write_text(json.dumps(cache, ensure_ascii=False, indent=2))
        if start % 240 == 0:
            print(lang, min(start+24, len(sentences)), '/', len(sentences), round(time.time()-started), 'seconds', flush=True)
    def convert(text):
        return ' '.join(cache.get(s, s) for s in segments(text))
    if extra.exists():
        (BASE / f'ui.{lang}.json').write_text(json.dumps({text: convert(text) for text in json.loads(extra.read_text())}, ensure_ascii=False, indent=2))
    out_meta = {}
    for slug, soup in soups.items():
        for node in list(soup.find_all(string=True)):
            if isinstance(node, Comment) or node.parent.name in ['script', 'style']:
                continue
            raw = str(node)
            text = raw.strip()
            if re.search('[A-Za-z]', text):
                node.replace_with((' ' if raw.startswith(' ') else '') + convert(text) + (' ' if raw.endswith(' ') else ''))
        (target / f'{slug}.html').write_text(str(soup))
        out_meta[slug] = {**meta[slug], 'title': convert(meta[slug]['title']), 'description': convert(meta[slug]['description'])}
    (BASE / f'articles.{lang}.json').write_text(json.dumps(out_meta, ensure_ascii=False, indent=2))
    print(lang, 'DONE', len(soups), 'articles', round(time.time()-started), 'seconds', flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--models', required=True)
    parser.add_argument('--languages', nargs='+', default=LANGS)
    args = parser.parse_args()
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as pool:
        jobs = [pool.submit(translate_language, lang, args.models) for lang in args.languages]
        for job in jobs:
            job.result()
