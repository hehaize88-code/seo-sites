export type VisualIndex={version:number;vectors:string;imageKeys:string[];dimension:number;indexedCount:number;catalogCount:number;indexedProductCount:number;detailCount:number;imageCount:number;failedCount:number;failedDetailCount:number;complete:boolean;createdAt:string;ids:string[];photos:number[];refs:{id:string;photo:number}[][]};
export type VisualMatch={id:string;score:number;photo:number;imageKey:string};
// Every source image competes; a product ranks by its strongest matching image.
export function nearest(vector:ArrayLike<number>,values:Int8Array,index:VisualIndex,limit=48):VisualMatch[]{
 if(index.dimension!==384||vector.length!==384||values.length!==index.ids.length*384)throw Error('index-invalid');
 const norm=Math.hypot(...Array.from(vector));if(!Number.isFinite(norm)||!norm)throw Error('image-invalid');
 const best=new Map<string,VisualMatch>();
 for(let row=0;row<index.ids.length;row++){
  let dot=0,size=0;for(let col=0;col<384;col++){const v=values[row*384+col];dot+=v*vector[col];size+=v*v;}
  const score=size?dot/(Math.sqrt(size)*norm):0;if(score<.5)continue;
  for(const ref of index.refs[row])if(score>(best.get(ref.id)?.score||0))best.set(ref.id,{...ref,score,imageKey:index.imageKeys[row]});
 }
 const matches=[...best.values()].sort((a,b)=>b.score-a.score||a.id.localeCompare(b.id));return matches[0]?.score>=.6?matches.slice(0,limit):[];
}
