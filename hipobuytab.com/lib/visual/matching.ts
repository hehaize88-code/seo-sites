export type VisualIndex = {version:number;vectors:string;imageKeys?:string[];dimension:number;indexedCount:number;catalogCount:number;failedCount:number;createdAt:string;ids:string[]};
export type VisualMatch = {id:string;score:number};
/** Cosine similarity of normalized CLS descriptors, never a match probability. */
export function nearest(vector:ArrayLike<number>,values:Int8Array,index:VisualIndex,limit=48):VisualMatch[]{
 if(index.dimension!==384||vector.length!==index.dimension||values.length!==index.ids.length*index.dimension)throw Error('index-invalid');
 const norm=Math.hypot(...Array.from(vector));if(!Number.isFinite(norm)||norm===0)throw Error('image-invalid');
 const matches:VisualMatch[]=[];
 for(let row=0;row<index.ids.length;row++){
  let dot=0,size=0;const offset=row*index.dimension;
  for(let col=0;col<index.dimension;col++){const v=values[offset+col];dot+=v*vector[col];size+=v*v;}
  const score=size?dot/(Math.sqrt(size)*norm):0;
  if(score>=0.50)matches.push({id:index.ids[row],score});
 }
 matches.sort((a,b)=>b.score-a.score||a.id.localeCompare(b.id));
 return matches[0]?.score>=0.60?matches.slice(0,limit):[];
}
