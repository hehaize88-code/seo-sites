'use client';
import {useEffect,useRef,useState,type ReactNode} from 'react';
import {Camera,ImagePlus,Upload,ShieldCheck,X,ArrowRight,RotateCcw,ScanSearch,LoaderCircle} from 'lucide-react';
import {visualCopy,imageCountLabel} from '@/lib/visual/copy';
import {localizeProductName} from '@/lib/product-names';
import {type Locale,t as uiText} from '@/lib/i18n';
import type {Product} from '@/lib/catalog';
import type {VisualIndex,VisualMatch} from '@/lib/visual/matching';
type Status='idle'|'preparing'|'loading'|'matching'|'details'|'done'|'cancelled'|'error';
export default function ImageSearch({locale,renderCard,initialFile}:{locale:Locale;renderCard:(p:Product,index:number)=>ReactNode;initialFile?:Blob|null}){
 const t=visualCopy[locale];
 const [status,setStatus]=useState<Status>('idle'),[error,setError]=useState(''),[progress,setProgress]=useState<number|null>(null),[preview,setPreview]=useState(''),[dragging,setDragging]=useState(false);
 const [products,setProducts]=useState<Product[]>([]),[matches,setMatches]=useState<VisualMatch[]>([]),[offset,setOffset]=useState(0),[partial,setPartial]=useState(false),[examples,setExamples]=useState<Product[]>([]),[meta,setMeta]=useState<VisualIndex|null>(null);
 const input=useRef<HTMLInputElement>(null),worker=useRef<Worker|null>(null),sequence=useRef(0),abort=useRef<AbortController|null>(null),lastImage=useRef<Blob|null>(null),lastExample=useRef<Product|null>(null),active=useRef(false);
 useEffect(()=>{if(initialFile)void selectImage(initialFile);},[initialFile]);
 const busy=['preparing','loading','matching','details'].includes(status);
 useEffect(()=>{const controller=new AbortController();fetch('/visual/index.json',{signal:controller.signal,cache:'no-cache'}).then(r=>r.ok?r.json() as Promise<VisualIndex>:null).then(setMeta).catch(()=>{});fetch('/api/catalog',{signal:controller.signal}).then(r=>r.ok?r.json() as Promise<{products:Product[]}>:null).then(data=>setExamples((data?.products||[]).filter((p:Product)=>p.image).slice(0,4))).catch(()=>{});return()=>{controller.abort();sequence.current++;worker.current?.terminate();abort.current?.abort();};},[]);
 useEffect(()=>()=>{if(preview.startsWith('blob:'))URL.revokeObjectURL(preview);},[preview]);
 useEffect(()=>{const onPaste=(e:ClipboardEvent)=>{if((e.target as HTMLElement)?.closest('input,textarea,[contenteditable="true"]'))return;const file=Array.from(e.clipboardData?.items||[]).find(item=>item.kind==='file'&&item.type.startsWith('image/'))?.getAsFile();if(file){e.preventDefault();void selectImage(file);}};document.addEventListener('paste',onPaste);return()=>document.removeEventListener('paste',onPaste);});
 function stop(){sequence.current++;active.current=false;abort.current?.abort();worker.current?.terminate();worker.current=null;setStatus('cancelled');setProgress(null);}
 function clear(){stop();lastImage.current=null;lastExample.current=null;setPreview('');setProducts([]);setMatches([]);setError('');setStatus('idle');setPartial(false);setOffset(0);}
 async function loadDetails(list:VisualMatch[],start:number,seq:number,replace=false){
  if(seq!==sequence.current)return;setStatus('details');setPartial(false);abort.current?.abort();const controller=new AbortController();abort.current=controller;
  try{
   const selected=list.slice(start,start+12);const response=await fetch('/api/visual-results',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({matches:selected}),signal:controller.signal});
   if(!response.ok)throw Error('unavailable');const data=await response.json() as {products:Product[];unavailable:number};if(seq!==sequence.current)return;
   const lookup=new Map<string,Product>((data.products||[]).map((p:Product)=>[p.recordId,p]));const ordered=selected.map(m=>lookup.get(m.id)).filter((p):p is Product=>Boolean(p));
   setProducts(ordered);setOffset(start+selected.length);setPartial(Boolean(data.unavailable));setStatus('done');active.current=false;
  }catch(e){if(seq!==sequence.current||controller.signal.aborted)return;setError(t.unavailable);setStatus('error');active.current=false;}
 }
 async function startSearch(image:Blob|null,seq:number,exampleProduct?:Product){
  if(seq!==sequence.current)return;
  setStatus('loading');setProgress(null);
  try{
   if(!worker.current)worker.current=new Worker('/visual/worker/search-worker.js?v=3',{type:'module'});
   const current=worker.current;
   current.onerror=()=>{if(seq!==sequence.current)return;setError(t.unavailable);setStatus('error');active.current=false;current.terminate();worker.current=null;};
   current.onmessage=(event:MessageEvent)=>{
    if(seq!==sequence.current)return;const data=event.data;
    if(data.type==='loading')setStatus('loading');
    if(data.type==='progress')setProgress(Math.max(0,Math.min(100,data.value)));
    if(data.type==='matching'){setStatus('matching');setProgress(null);}
    if(data.type==='error'){setError(data.code==='index-stale'?t.stale:/OffscreenCanvas|WebAssembly|SIMD/i.test(data.code)?t.browser:t.unavailable);setStatus('error');active.current=false;}
    if(data.type==='results'){
     const found=data.matches as VisualMatch[];setMatches(found);setOffset(0);
     if(found.length)void loadDetails(found,0,seq,true);else{setStatus('done');active.current=false;}
    }
   };
   if(exampleProduct){current.postMessage({exampleId:exampleProduct.recordId,imageUrl:exampleProduct.image});}else if(image){const buffer=await image.arrayBuffer();if(seq!==sequence.current)return;current.postMessage({image:buffer},[buffer]);}
  }catch(error){console.error('Image search could not start',error instanceof Error?error.message:'unknown');if(seq===sequence.current){setError(t.unavailable);setStatus('error');active.current=false;}}
 }
 async function selectImage(file:Blob){
  if(file.size>20*1024*1024){setError(t.large);return;}
  if(!['image/jpeg','image/png','image/webp','image/gif'].includes(file.type)){setError(t.invalid);return;}
  if(typeof createImageBitmap!=='function'||typeof Worker==='undefined'||typeof OffscreenCanvas==='undefined'){setError(t.browser);return;}
  if(active.current){worker.current?.terminate();worker.current=null;}
  const seq=++sequence.current;active.current=true;abort.current?.abort();setStatus('preparing');setProducts([]);setMatches([]);setPartial(false);setError('');setProgress(null);lastImage.current=null;lastExample.current=null;setPreview('');
  try{
   const bitmap=await createImageBitmap(file);if(seq!==sequence.current){bitmap.close();return;}
   if(bitmap.width*bitmap.height>40_000_000){bitmap.close();throw Error('large');}
   const scale=Math.min(1,1024/Math.max(bitmap.width,bitmap.height));const canvas=document.createElement('canvas');canvas.width=Math.max(1,Math.round(bitmap.width*scale));canvas.height=Math.max(1,Math.round(bitmap.height*scale));
   const ctx=canvas.getContext('2d',{willReadFrequently:true});if(!ctx){bitmap.close();throw Error('browser');}
   ctx.fillStyle='#fff';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.drawImage(bitmap,0,0,canvas.width,canvas.height);bitmap.close();
   const pixels=ctx.getImageData(0,0,canvas.width,canvas.height).data;let sum=0,square=0,n=0;for(let i=0;i<pixels.length;i+=64){const value=(pixels[i]+pixels[i+1]+pixels[i+2])/3;sum+=value;square+=value*value;n++;}if(square/n-(sum/n)**2<10)throw Error('blank');
   const resized=await new Promise<Blob>((resolve,reject)=>canvas.toBlob(blob=>blob?resolve(blob):reject(Error('unreadable')),'image/jpeg',.92));
   if(seq!==sequence.current)return;lastImage.current=resized;setPreview(URL.createObjectURL(resized));await startSearch(resized,seq);
  }catch(e){if(seq!==sequence.current)return;const code=e instanceof Error?e.message:'';setError(code==='blank'?t.blank:code==='large'?t.large:code==='browser'?t.browser:t.unreadable);setStatus('error');active.current=false;}
 }
 async function example(p:Product){
  if(active.current)stop();const seq=++sequence.current;abort.current?.abort();setError('');setProducts([]);setMatches([]);setPartial(false);active.current=true;lastImage.current=null;lastExample.current=p;setPreview(p.image);await startSearch(null,seq,p);
 }
 function retry(){if(lastImage.current){if(active.current)stop();const seq=++sequence.current;setError('');setProducts([]);setMatches([]);setPartial(false);active.current=true;void startSearch(lastImage.current,seq);}else if(lastExample.current){void example(lastExample.current);}else input.current?.click();}
 const statusText=status==='preparing'?t.preparing:status==='loading'?t.loading:status==='matching'?t.matching:status==='details'?t.details:status==='cancelled'?t.cancelled:'';
 const coverage=meta?t.coverage.replace('{count}',meta.indexedProductCount.toLocaleString(locale)).replace('{date}',new Intl.DateTimeFormat(locale==='zh'?'zh-CN':locale,{dateStyle:'medium'}).format(new Date(meta.createdAt))):'';
 return <section className="wrap visual-search-page">
  <div className="visual-heading"><span className="eyebrow"><Camera size={16}/>{t.eyebrow}</span><h1>{t.title}</h1><p>{t.intro}</p></div>
  <input ref={input} className="visually-hidden" type="file" accept="image/jpeg,image/png,image/webp,image/gif" aria-label={t.upload} onChange={event=>{const file=event.target.files?.[0];if(file)void selectImage(file);event.target.value='';}}/>
  <div className={'visual-search-layout '+(preview?'has-image':'')}>
   <aside className="visual-input-panel">
    <div className={'visual-dropzone '+(dragging?'dragging':'')+(preview?' has-preview':'')} onDragOver={event=>{event.preventDefault();setDragging(true);}} onDragLeave={()=>setDragging(false)} onDrop={event=>{event.preventDefault();setDragging(false);const file=event.dataTransfer.files[0];if(file)void selectImage(file);}}>
     {preview?<><div className="visual-reference"><span>{t.reference}</span><button className="icon-button" onClick={clear} aria-label={t.remove}><X size={18}/></button></div><img className="visual-query-photo" src={preview} alt={t.reference}/><button className="button secondary" onClick={()=>input.current?.click()}><ImagePlus size={17}/>{t.change}</button></>:<><div className="visual-upload-symbol"><ScanSearch size={39}/></div><h2>{t.upload}</h2><p>{t.drop}</p><button className="button primary" onClick={()=>input.current?.click()}><Upload size={18}/>{t.upload}</button><small>{t.formats}</small></>}
    </div>
    <p className="visual-privacy"><ShieldCheck size={16}/>{t.privacy}</p>
    <p className="visual-tip">{t.tip}</p>
    <p className="visual-download-note">{t.firstUse}</p>
    {coverage&&<p className="visual-coverage">{coverage}<span>{meta?.indexedCount.toLocaleString(locale)} / {meta?.imageCount.toLocaleString(locale)} {imageCountLabel[locale]}</span>{Boolean(meta?.failedCount||meta?.failedDetailCount)&&<span>{t.limited}</span>}</p>}
   </aside>
   <div className="visual-results-panel">
    <div className="visual-status" role="status" aria-live="polite" aria-atomic="true">
     {busy&&<><LoaderCircle className="visual-spinner" size={22}/><span>{statusText}{status==='loading'&&progress!==null?` ${progress}%`:''}</span><button onClick={stop}>{t.cancel}</button></>}
     {status==='cancelled'&&<><span>{t.cancelled}</span><button onClick={retry}>{t.retry}</button></>}
     {error&&<div className="visual-error" role="alert"><p>{error}</p><button className="text-link" onClick={retry}><RotateCcw size={16}/>{t.retry}</button></div>}
    </div>
    {busy&&status==='loading'&&<div className="visual-progress" role="progressbar" aria-label={t.loading} aria-valuemin={0} aria-valuemax={100} aria-valuenow={progress??undefined}><span style={progress===null?undefined:{width:progress+'%'}} className={progress===null?'indeterminate':''}/></div>}
    {products.length>0&&<><div className="visual-results-heading"><h2>{t.results}</h2><span>{t.count.replace('{count}',String(products.length))}</span></div><p className="visual-results-note">{t.resultNote}</p><div className="product-grid visual-result-grid">{products.map((p,index)=>renderCard(p,index))}</div></>}
    {partial&&<div className="visual-partial"><p>{t.partial}</p><button className="text-link" onClick={retry}>{t.retry}</button></div>}
    {status==='done'&&!matches.length&&<div className="visual-empty"><ScanSearch size={39}/><h2>{t.empty}</h2><p>{t.emptyNote}</p><a className="text-link" href={'/'+locale+'/spreadsheet'}>{t.browse}<ArrowRight size={16}/></a></div>}
    {status==='done'&&matches.length>12&&<nav className="pagination visual-pagination" aria-label={uiText(locale,'page')}><button disabled={offset<=12} onClick={()=>{active.current=true;void loadDetails(matches,Math.max(0,Math.floor((offset-1)/12)*12-12),sequence.current,true);document.querySelector('.visual-results-heading')?.scrollIntoView({block:'start'});}}>{uiText(locale,'previous')}</button><span>{uiText(locale,'page')} {Math.ceil(offset/12)} / {Math.ceil(matches.length/12)}</span><button disabled={offset>=matches.length} onClick={()=>{active.current=true;void loadDetails(matches,offset,sequence.current,true);document.querySelector('.visual-results-heading')?.scrollIntoView({block:'start'});}}>{uiText(locale,'next')}</button></nav>}
    {!preview&&!busy&&<div className="visual-example-section"><div className="visual-example-heading"><span className="eyebrow">USFANS</span><h2>{t.examples}</h2></div><div className="visual-example-grid">{examples.map(p=><button className="visual-example" key={p.recordId} onClick={()=>void example(p)} aria-label={t.example+' — '+localizeProductName(p.name,locale)}><img src={p.image} alt={localizeProductName(p.name,locale)} referrerPolicy="no-referrer"/><span>{localizeProductName(p.name,locale)}<ArrowRight size={16}/></span></button>)}</div>{!examples.length&&<a className="text-link" href={'/'+locale+'/spreadsheet'}>{t.browse}<ArrowRight size={16}/></a>}</div>}
   </div>
  </div>
 </section>;
}
