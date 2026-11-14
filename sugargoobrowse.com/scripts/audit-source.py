import subprocess,urllib.request,concurrent.futures,json,re,gzip,os,time
from datetime import datetime,timezone
meta=json.load(gzip.open('search/metadata.json.gz'));ids=set(r[0] for r in meta['records']);cache='/tmp/sugar-hm-audit';os.makedirs(cache,exist_ok=True)
def read(n):
 path=f'{cache}/{n}.html'
 for attempt in range(2):
  try:
   if os.path.exists(path):s=open(path).read()
   else:
    url='https://www.cnfanshm.com/AllProducts/'+('' if n==1 else f'list_1_{n}/')
    r=subprocess.run(['curl','-fLs','--max-time','20',url],capture_output=True,check=True);s=r.stdout.decode();open(path,'w').write(s)
   chunks=s.split('class="product-card')[1:];found=[]
   for c in chunks:
    m=re.search(r'/AllProducts/(\d+)\.html',c)
    if m:found.append(m[1])
   if not found:raise ValueError('empty page')
   return n,found,None
  except Exception as e:
   if attempt==1:return n,[],str(e)
   time.sleep(2)
allids=set();errors=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 for i,(n,found,error) in enumerate(ex.map(read,range(1,102)),1):
  allids.update(found)
  if error:errors.append([n,error])
  if i%20==0:print('Pages',i,'products',len(allids),'errors',len(errors),flush=True)
audit={'auditedAt':datetime.now(timezone.utc).isoformat(),'source':'https://cnfanshm.com','pages':101,'discoveredProducts':len(allids),'indexedProducts':len(ids),'images':len(meta['records']),'unindexedProducts':sorted(allids-ids),'indexOnlyProducts':sorted(ids-allids),'errors':errors,'imageSnapshotDate':meta['builtAt']}
json.dump(audit,open('search/audit.json','w'),indent=2);print(json.dumps({k:v for k,v in audit.items() if k!='indexOnlyProducts'}),flush=True)
