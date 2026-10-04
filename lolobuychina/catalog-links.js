/* Resolve only established catalogue mappings; never invent a product route. */
(function(){
  const origin='https://cnfanshm.com';
  const products=[{"t": "Shorts-1", "cat": "Pants / Shorts", "id": "7777809164", "price": 159, "qc": 838, "img": "https://cnfanshm.com/uploads/allimg/20260529/1-260529130550J0.webp", "url": "https://cnfanshm.com/AllProducts/6079.html", "tag": "Today"}, {"t": "Shoes-1", "cat": "Shoes", "id": "7777852466", "price": 345, "qc": 543, "img": "https://cnfanshm.com/uploads/allimg/20260529/1-260529130339D6.webp", "url": "https://cnfanshm.com/AllProducts/6078.html", "tag": "Popular"}, {"t": "Sweatshirts-1", "cat": "Sweatshirts", "id": "7765045446", "price": 219, "qc": 721, "img": "https://cnfanshm.com/uploads/allimg/20260513/1-260513093301E8.webp", "url": "https://cnfanshm.com/AllProducts/6077.html", "tag": "New"}, {"t": "Pants/Shorts-1", "cat": "Pants / Shorts", "id": "7762102963", "price": 275, "qc": 503, "img": "https://cnfanshm.com/uploads/allimg/20260513/1-26051309302B41.webp", "url": "https://cnfanshm.com/AllProducts/6076.html", "tag": "QC"}, {"t": "Pants/Shorts-2", "cat": "Pants / Shorts", "id": "7755087953", "price": 189, "qc": 871, "img": "https://cnfanshm.com/uploads/allimg/20260506/1-260506102930T0.webp", "url": "https://cnfanshm.com/AllProducts/6075.html", "tag": "Hot"}, {"t": "Sweatshirts-2", "cat": "Sweatshirts", "id": "7755070499", "price": 169, "qc": 648, "img": "https://cnfanshm.com/uploads/allimg/20260506/1-260506102T2143.webp", "url": "https://cnfanshm.com/AllProducts/6074.html", "tag": "New"}, {"t": "Shoes-60", "cat": "Shoes", "id": "7711153142", "price": 168, "qc": 782, "img": "https://cnfanshm.com/uploads/allimg/20260416/1-260416231241P9.jpg", "url": "https://cnfanshm.com/AllProducts/6071.html", "tag": "QC"}, {"t": "Shoes-59", "cat": "Shoes", "id": "7711145274", "price": 500, "qc": 511, "img": "https://cnfanshm.com/uploads/allimg/20260416/1-26041623123LM.jpg", "url": "https://cnfanshm.com/AllProducts/6070.html", "tag": "Hot"}];
  function search(q){return origin+'/search.html?keywords='+encodeURIComponent(q)+'&channelid=2'}
  function resolve(value){
    let raw=String(value||'').trim();if(!raw)return null;
    let id='',source='',native=false;
    try{
      let u=new URL(raw);
      if(!['https:','http:'].includes(u.protocol))return search(raw);
      if(u.hostname==='cnfanshm.com'||u.hostname==='www.cnfanshm.com'){
        const m=u.pathname.match(/^\/AllProducts\/(\d+)\.html$/i);
        if(m){id=m[1];native=true;}
      } else {
        if(u.searchParams.has('url')){try{u=new URL(u.searchParams.get('url'))}catch(e){}}
        if(/(^|\.)weidian\.com$/.test(u.hostname)){source='weidian';id=u.searchParams.get('itemID')||u.searchParams.get('itemId')||''}
        else if(/(^|\.)(taobao|tmall)\.com$/.test(u.hostname)){source='taobao';id=u.searchParams.get('id')||''}
        else if(/(^|\.)1688\.com$/.test(u.hostname)){source='1688';const m=u.pathname.match(/\/offer\/(\d+)\.html/);id=m?m[1]:''}
      }
    }catch(e){if(/^\d+$/.test(raw))id=raw;}
    const match=products.find(p=>native?p.url===origin+'/AllProducts/'+id+'.html':(!source||source==='weidian')&&p.id===id);
    if(match)return match.url;
    const named=products.filter(p=>p.t.toLowerCase()===raw.toLowerCase());
    if(named.length===1)return named[0].url;
    return search(id||raw);
  }
  window.LBC={resolve};
})();
