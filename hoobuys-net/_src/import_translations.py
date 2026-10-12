"""Import complete translation assets and apply the coordinated privacy update."""
from pathlib import Path
from bs4 import BeautifulSoup,Comment
import json,hashlib,re,argparse
S=Path(__file__).parent
LANGS=['zh-CN','de','fr','es','it','pl','nl','pt']
def key(t):return hashlib.sha256(t.strip().encode()).hexdigest()[:12]
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
ap=argparse.ArgumentParser();ap.add_argument('input');args=ap.parse_args()
base=Path(args.input);merged={}
for lang in LANGS:
    out={}
    for i in range(21):
        source=json.loads((S/'chunks'/f'{i:02}.json').read_text());target=json.loads((base/lang/f'{i:02}.json').read_text())
        if source.keys()!=target.keys():raise ValueError(f'{lang}/{i:02}: incomplete translation')
        if any(not isinstance(v,str) or not v.strip() for v in target.values()):raise ValueError(f'{lang}/{i:02}: empty translation')
        out.update(target)
    merged[lang]=out

update=json.loads((S/'privacy_update.json').read_text())
p=S/'en/privacy.html';s=BeautifulSoup(p.read_text(),'html.parser')
for t in list(s.find_all(string=True)):
    if str(t).strip()==update['old']:t.replace_with(update['new']['en'])
    elif str(t).strip()=='Last updated August 13, 2026.':t.replace_with(update['date']['en'])
p.write_text(str(s))

# Rebuild the catalogue without rerunning the one-time layout migration.
cat={};membership={}
def translatable(t):return bool(re.search(r'[A-Za-z]',t)) and t not in ['hoobuys','.','net','HooBuys.net','QC','USD','cm','kg'] and not re.fullmatch(r'[\d\W]+',t)
for f in sorted((S/'en').glob('*.html')):
    soup=BeautifulSoup(f.read_text(),'html.parser');texts=[]
    for t in soup.find_all(string=True):
        if t.parent.name not in ['script','style'] and not isinstance(t,Comment) and translatable(str(t).strip()):texts.append(str(t).strip())
    for el in soup.find_all(True):
        for attr in ['alt','title','placeholder','aria-label']:
            if el.get(attr) and translatable(el[attr]):texts.append(el[attr])
        if el.name=='meta' and el.get('name')=='description':texts.append(el['content'])
    membership[f.stem]=[key(t) for t in texts]
    cat.update({key(t):t for t in texts})
write(S/'catalog.json',cat)
pages=json.loads((S/'pages.json').read_text());pages['strings']=membership;write(S/'pages.json',pages)
for lang,out in merged.items():
    out[key(update['new']['en'])]=update['new'][lang]
    out[key(update['date']['en'])]=update['date'][lang]
    missing=cat.keys()-out.keys()
    if missing:raise ValueError(f'{lang}: missing final strings {missing}')
    write(S/'i18n'/f'{lang}.json',{k:out[k] for k in cat})
print('Imported 8 complete translations; privacy description and date synchronized in 9 languages')
