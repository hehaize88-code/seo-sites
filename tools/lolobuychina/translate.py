"""Optional offline draft translation. Normal builds use the committed translations."""
import os
os.environ.setdefault('OMP_NUM_THREADS','1')
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import argparse,json,re,time,html,concurrent.futures
from pathlib import Path
from bs4 import BeautifulSoup,Comment
import ctranslate2,sentencepiece
B=Path(__file__).resolve().parent
LANGS=['de','fr','es','it','pt','ja','ko','zh']
UI=['Home','Finds','Directory','W2C Links','QC Photos','Shipping','Articles','FAQ','Search','Search product link, source ID or keyword','Product link, source ID or keyword','View product','Check current price','Source ID','Shoes','Sweatshirts','T-Shirts','Jackets','Pants / Shorts','Headwear','Accessories','Jersey','Electronics','Browse category','Read article','Related reading','Updated 31 October 2026','Independent buying guide','LoloBuyChina Editorial','Main navigation','Choose language','Skip to content','Page not found','The requested page is unavailable. Choose a guide or return to the homepage.','Back to home','Independent product discovery and buying guides. Not operated by LoloBuy.','Link and ordering guides','QC, sizing and buyer evidence','Shipping and cost planning','Orders, returns and tracking','Contents','Product discovery','LoloBuyChina']
def pieces(s):return re.split(r'(?<=[.!?])\s+(?=[A-Z“"0-9])',s)
def sources():
 c=json.loads((B/'content.en.json').read_text());out=list(UI)
 for p in c.values():
  out.extend([p['title'],p['description']])
  soup=BeautifulSoup(p['body'],'html.parser')
  out.extend(str(n).strip() for n in soup.find_all(string=True) if n.parent.name not in ['code','script','style'] and not isinstance(n,Comment) and re.search('[A-Za-z]',str(n)) and not str(n).strip().startswith('__'))
 return list(dict.fromkeys(out))
def translate(lang,modelroot):
 root=next((Path(modelroot)/lang).rglob('model.bin')).parent.parent
 sp=sentencepiece.SentencePieceProcessor(model_file=str(root/'sentencepiece.model'))
 tr=ctranslate2.Translator(str(root/'model'),device='cpu',compute_type='int8',intra_threads=2,inter_threads=1)
 out=B/'translations';out.mkdir(exist_ok=True)
 file=out/f'{lang}.json';cache=json.loads(file.read_text()) if file.exists() else {}
 needed=list(dict.fromkeys(s for text in sources() for s in pieces(text) if s not in cache))
 print(lang,'pending',len(needed),flush=True);start=time.time()
 for i in range(0,len(needed),32):
  batch=needed[i:i+32];results=tr.translate_batch([sp.encode(s,out_type=str) for s in batch],beam_size=3,max_batch_size=32,max_decoding_length=384,repetition_penalty=1.05)
  for source,result in zip(batch,results):
   v=html.unescape(sp.decode(result.hypotheses[0])).strip()
   v=re.sub(r'(?i)lolo\s*buy\s*china','LoloBuyChina',v)
   v=re.sub(r'(?i)lolo\s*buy','LoloBuy',v)
   cache[source]=v
  file.write_text(json.dumps(cache,ensure_ascii=False,indent=2))
  if i%320==0:print(lang,i+len(batch),'/',len(needed),round(time.time()-start),'s',flush=True)
 print(lang,'DONE',round(time.time()-start),'s',flush=True)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--models',required=True);a.add_argument('--languages',nargs='+',default=LANGS);args=a.parse_args()
 with concurrent.futures.ProcessPoolExecutor(max_workers=4) as pool:
  for f in [pool.submit(translate,l,args.models) for l in args.languages]:f.result()
