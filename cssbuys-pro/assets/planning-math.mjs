export function parcelWeight({actual,length,width,height,divisor,increment,rule='max'}) {
  const values=[actual,length,width,height,divisor,increment];
  if(values.some(x=>!Number.isFinite(x)||x<=0||x>1000000)||!['max','actual'].includes(rule)) throw new RangeError('invalid');
  const volume=length*width*height/divisor;
  const basis=rule==='actual'?actual:Math.max(actual,volume);
  const billed=Math.ceil(basis/increment-1e-10)*increment;
  if(!Number.isFinite(billed))throw new RangeError('invalid');
  return {volume,basis,billed};
}
export function parcelBudget(values) {
  if(values.length!==8||values.some(x=>!Number.isFinite(x)||x<0||x>1e9)) throw new RangeError('invalid');
  const cents=values.map(x=>Math.round(x*100));
  const gross=cents.slice(0,7).reduce((a,b)=>a+b,0);
  if(cents[7]>gross) throw new RangeError('credit');
  return (gross-cents[7])/100;
}
