"""Reconcile source listing URLs and derive only image-search features. No product DB."""
import urllib.request,concurrent.futures,re,json,html,base64,time,collections
from pathlib import Path
from PIL import Image
from io import BytesIO
root=Path('/tmp/rizz-audit');root.mkdir(exist_ok=True)
base='https://cnfanshm.com'
def get(url):
 for n in range(3):
  try:return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'RizzitGO-source-index/1.0'}),timeout=35).read()
  except Exception:
   if n==2:raise
   time.sleep(1+n)
def page(n):
 f=root/f'list-{n}.html'
 if not f.exists():f.write_bytes(get(base+('/AllProducts/' if n==1 else f'/AllProducts/list_1_{n}/')))
 s=f.read_text();return n,set(re.findall(r'href="(/AllProducts/\d+\.html)"',s))
paths=set();fail=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for f in concurrent.futures.as_completed([ex.submit(page,n) for n in range(1,102)]):
  try:n,ps=f.result();paths.update(ps)
  except Exception as e:fail.append(str(e))
paths.update(re.findall(r'https://cnfanshm.com(/AllProducts/\d+\.html)',get(base+'/sitemap.xml').decode()))
for ident in ['4210','4209','4208','4207']:
 try:
  if b'class="product-gallery"' in get(base+'/AllProducts/'+ident+'.html'):paths.add('/AllProducts/'+ident+'.html')
 except Exception:pass
print('live listing IDs',len(paths),'failed pages',len(fail),flush=True)
# Existing derived fingerprints belong to the SAME cnfanshm source. Reuse bytes, never a product database at runtime.
oldroot=Path('/workspace/seo-sites-oopbuygrid/oopbuygrid.com/dist/public')
old=json.loads((oldroot/'image-index.json').read_text())['result']
lookup={}
for p in json.loads((oldroot/'products.json').read_text()):lookup[p['id']]=p['title']
ids={p.rsplit('/',1)[-1].split('.')[0] for p in paths}
localids={e['id'].replace('source-','') for e in old if not e['src'].startswith('http')}
urlmap={}
for ident in localids:
 f=root/(ident+'.html');h=f.read_text() if f.exists() else get(base+'/AllProducts/'+ident+'.html').decode();f.write_text(h)
 g=h.split('class="product-gallery"')[1].split('class="product-info"')[0]
 urls=list(dict.fromkeys(base+x if x.startswith('/') else x for x in re.findall(r'data-src="([^"]+)"',g)))
 urlmap[ident]=urls
items=collections.defaultdict(list);missing=[]
for e in old:
 ident=e['id'].replace('source-','')
 if ident not in ids:continue
 url=e['src']
 if not url.startswith('http'):
  ix=int(re.search(r'-(\d+)\.',url)[1]);u=urlmap.get(ident,[])
  if ix>=len(u):missing.append(url);continue
  url=u[ix]
 if not url.startswith(base+'/'):continue
 # Reduce previously decoded 12x12 RGB to 8x8 RGB, matching client signature dimensions.
 im=Image.frombytes('RGB',(12,12),base64.b64decode(e['rgb'])).resize((8,8),Image.Resampling.BILINEAR)
 sig=base64.b64encode(bytes(c>>3 for c in im.tobytes())).decode()
 items[ident].append([url,sig])
unknown=ids-set(items)
print('known products',len(items),'new',len(unknown),'images',sum(map(len,items.values())),flush=True)
# New records use every gallery image, never only the cover.
for ident in unknown:
 try:
  h=get(base+'/AllProducts/'+ident+'.html').decode();g=h.split('class="product-gallery"')[1].split('class="product-info"')[0]
  lookup['source-'+ident]=html.unescape(re.search(r'<h1[^>]*>(.*?)</h1>',h,re.S)[1])
  for u in dict.fromkeys(re.findall(r'data-src="([^"]+)"',g)):
   url=base+u if u.startswith('/') else u
   try:
    im=Image.open(BytesIO(get(url))).convert('RGB').resize((8,8),Image.Resampling.BILINEAR)
    items[ident].append([url,base64.b64encode(bytes(c>>3 for c in im.tobytes())).decode()])
   except Exception:missing.append(url)
 except Exception:missing.append('/AllProducts/'+ident+'.html')
result={'updated':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'fingerprintBaseline':'2026-11-13','total':len(ids),'products':len(items),'images':sum(map(len,items.values())),'missingImages':len(missing),'listingFailures':len(fail),'items':[['/AllProducts/'+ident+'.html',lookup.get('source-'+ident,'Product '+ident),entries] for ident,entries in items.items()]}
Path('worker/search-index.js').write_text('export const SEARCH_INDEX='+json.dumps(result,separators=(',',':'))+';\n')
(root/'audit.json').write_text(json.dumps({k:v for k,v in result.items() if k!='items'},indent=2));print({k:v for k,v in result.items() if k!='items'},flush=True)
