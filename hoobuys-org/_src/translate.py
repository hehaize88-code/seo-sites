"""Offline full-text translations with official Argos models; no runtime dependency."""
from pathlib import Path
from bs4 import BeautifulSoup, Comment, Doctype
import json,re,html,os,time,argparse,concurrent.futures
S=Path(__file__).resolve().parent
SKIP={'English','简体中文','Deutsch','Français','Español','Italiano','Polski','Nederlands','Português','hoobuys','org','hoobuys.org','kg','QC','W2C','HooBuy','Taobao','Weidian','1688'}
def needed(s):return bool(re.search('[A-Za-z]',s)) and s not in SKIP
def parts(s):return re.split(r'(?<=[.!?])\s+(?=[A-Z“"0-9])',s)
def text_nodes(soup):return [n for n in soup.find_all(string=True) if not isinstance(n,(Comment,Doctype)) and n.parent.name not in ['script','style'] and not n.find_parent(attrs={'hreflang':True}) and needed(str(n).strip())]
def json_strings(j):
 out=[]
 if isinstance(j,dict):
  for k,v in j.items():
   if k in ['name','headline','description'] and isinstance(v,str) and needed(v):out.append(v)
   elif isinstance(v,(dict,list)):out+=json_strings(v)
 elif isinstance(j,list):
  for v in j:out+=json_strings(v)
 return out
def strings(doc):
 soup=BeautifulSoup(doc,'html.parser');out=[str(n).strip() for n in text_nodes(soup)]
 for n in soup.select('meta[name="description"],meta[property="og:title"],meta[property="og:description"]'):out.append(n['content'])
 for n in soup.find_all():
  for a in ['alt','aria-label','placeholder']:
   if n.get(a) and needed(n[a]):out.append(n[a])
 for n in soup.select('script[type="application/ld+json"]'):out+=json_strings(json.loads(n.string))
 return out

def clean(value,source,lang):
 from ftfy import fix_text
 value=fix_text(value).replace('▁',' ')
 value=re.sub(r'\s+',' ',value).strip()
 if 'HooBuy' in source or 'HooBuy' in source.replace('HoooBuy','HooBuy'):
  value=re.sub(r'HooAcheter|HooAchetez|HoooBuy|霍布依|呼和浩特|胡布伊|胡同|胡布伊', 'HooBuy',value)
 value=value.replace('😛','↗')
 if lang=='zh-CN':
  for a,b in {'田地':'字段','布料索赔':'面料说明','织物索赔':'面料说明','大小证据':'尺码依据','大小标签':'尺码标签','大小图表':'尺码表','陶宝':'淘宝','魏甸':'微店','HooBuy帽':'HooBuy 连帽卫衣','售货到货房航运':'卖家到仓库的国内运输'}.items():value=value.replace(a,b)
  if any(x in source.lower() for x in ['exact order','your order','order id','order record']):value=value.replace('顺序','订单')
 if '→' in source and '→' not in value:value=value.rstrip(' _+')+' →'
 if '↗' in source and '↗' not in value:value=value.rstrip(' _+')+' ↗'
 return value

def render_localized(doc,lang,slug,cache,langs,names,route):
 soup=BeautifulSoup(doc,'html.parser');origin='https://hoobuys.org'
 overrides_file=S/'overrides.json';overrides=json.loads(overrides_file.read_text()).get(lang,{}) if overrides_file.exists() else {}
 if lang=='zh-CN':overrides.update(json.loads((S/'zh-review.json').read_text()))
 known=set(json.loads((S/'english-pages.json').read_text()))
 def convert(s):
  if lang=='en' or not needed(s):return s
  if s in overrides:return overrides[s]
  result=[]
  for segment in parts(s):
   if not needed(segment):result.append(segment)
   elif segment in overrides:result.append(overrides[segment])
   elif segment in cache:result.append(cache[segment])
   else:raise ValueError('Missing translation '+lang+': '+segment[:100])
  return clean(' '.join(result),s,lang)
 if lang!='en':
  for n in text_nodes(soup):
   raw=str(n);n.replace_with((' ' if raw.startswith(' ') else '')+convert(raw.strip())+(' ' if raw.endswith(' ') else ''))
  for n in soup.select('meta[name="description"],meta[property="og:title"],meta[property="og:description"]'):n['content']=convert(n['content'])
  for n in soup.find_all():
   for a in ['alt','aria-label','placeholder']:
    if n.get(a):n[a]=convert(n[a])
 def local_url(u):
  if u.startswith(origin):u=u[len(origin):]
  if u.startswith('/') and not u.startswith('//'):
   from urllib.parse import urlsplit
   v=urlsplit(u);p=v.path.strip('/').removesuffix('.html')
   if p in ['', 'index'] or p in known:return route(lang,p or 'index')+('?' +v.query if v.query else '')+('#'+v.fragment if v.fragment else '')
  return u
 soup.html['lang']=lang
 for a in soup.select('a[href]'):
  if not a.get('hreflang'):a['href']=local_url(a['href'])
 url=origin+route(lang,slug)
 soup.select_one('link[rel="canonical"]')['href']=url;soup.select_one('meta[property="og:url"]')['content']=url
 if slug!='404':
  for l in langs+['x-default']:soup.head.append(soup.new_tag('link',rel='alternate',hreflang=l,href=origin+route('en' if l=='x-default' else l,slug)))
 picker=soup.select_one('.language-picker');picker.summary.string=names[lang]
 for a in picker.select('a[hreflang]'):
  a.attrs.pop('aria-current',None)
  if a['hreflang']==lang:a['aria-current']='page'
 def fix(j):
  if isinstance(j,dict):
   for k,v in j.items():
    if k in ['name','headline','description'] and isinstance(v,str):j[k]=convert(v)
    elif k=='inLanguage' and isinstance(v,str):j[k]=lang
    elif k in ['url','@id','item','mainEntityOfPage'] and isinstance(v,str) and v.startswith(origin):j[k]=origin+local_url(v)
    elif isinstance(v,(dict,list)):fix(v)
  elif isinstance(j,list):
   for v in j:fix(v)
 for n in soup.select('script[type="application/ld+json"]'):
  j=json.loads(n.string);fix(j);n.string=json.dumps(j,ensure_ascii=False)
 return str(soup)

def run_language(lang,models):
 os.environ['OMP_NUM_THREADS']='1';os.environ['OPENBLAS_NUM_THREADS']='1'
 import ctranslate2,sentencepiece
 from sacremoses import MosesTokenizer,MosesDetokenizer,MosesPunctNormalizer
 from subword_nmt.apply_bpe import BPE
 code='zh' if lang=='zh-CN' else lang;model=next((Path(models)/code).rglob('model.bin')).parent.parent
 if (model/'sentencepiece.model').exists():
  sp=sentencepiece.SentencePieceProcessor(model_file=str(model/'sentencepiece.model'));encode=lambda x:sp.encode(x,out_type=str);decode=sp.decode
 else:
  tok=MosesTokenizer('en');detok=MosesDetokenizer(code);norm=MosesPunctNormalizer('en')
  with (model/'bpe.model').open() as f:bpe=BPE(f)
  encode=lambda x:bpe.segment_tokens(tok.tokenize(norm.normalize(x)));decode=lambda x:detok.detokenize(' '.join(x).replace('@@ ','').split(' '))
 tr=ctranslate2.Translator(str(model/'model'),device='cpu',compute_type='int8',intra_threads=2,inter_threads=1)
 cache_file=S/'translations'/(lang+'.json');cache_file.parent.mkdir(exist_ok=True);cache=json.loads(cache_file.read_text()) if cache_file.exists() else {}
 pages=json.loads((S/'english-pages.json').read_text());all_strings=list(dict.fromkeys(s for doc in pages.values() for s in strings(doc)))
 sentences=list(dict.fromkeys(s for t in all_strings for s in parts(t) if needed(s) and s not in cache))
 started=time.time();print(lang,'pending',len(sentences),flush=True)
 for start in range(0,len(sentences),32):
  batch=sentences[start:start+32];results=tr.translate_batch([encode(s) for s in batch],beam_size=3,max_batch_size=32,max_decoding_length=384,repetition_penalty=1.05)
  for source,result in zip(batch,results):
   translated=html.unescape(decode(result.hypotheses[0])).strip();translated=re.sub(r'\bHoo\s*Buy\b|\bHoobuy\b','HooBuy',translated,flags=re.I)
   if not translated:raise ValueError('Empty '+lang+': '+source)
   cache[source]=translated
  cache_file.write_text(json.dumps(cache,ensure_ascii=False,indent=2))
  if start%320==0:print(lang,min(start+32,len(sentences)),'/',len(sentences),round(time.time()-started),'seconds',flush=True)
 print(lang,'DONE',round(time.time()-started),'seconds',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--models',required=True);p.add_argument('--languages',nargs='+',default=['zh-CN','de','fr','es','it','pl','nl','pt']);a=p.parse_args()
 with concurrent.futures.ProcessPoolExecutor(max_workers=4) as pool:
  tasks=[pool.submit(run_language,l,a.models) for l in a.languages]
  for t in tasks:t.result()
