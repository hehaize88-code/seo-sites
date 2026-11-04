import {parcelWeight,parcelBudget} from './planning-math.mjs';
const locale=document.documentElement.lang||'en';
const number=new Intl.NumberFormat(locale,{maximumFractionDigits:3});
const currency=new Intl.NumberFormat(locale,{style:'currency',currency:'CNY'});
function track(name){if(typeof window.gtag==='function')window.gtag('event',name,{language:locale});}
document.querySelectorAll('[data-weight-form]').forEach(form=>{
  form.addEventListener('submit',event=>{
    event.preventDefault();const error=form.querySelector('.tool-error');error.textContent='';
    try {
      const values={};for(const key of ['actual','length','width','height','divisor','increment'])values[key]=Number(form.elements.namedItem(key).value);
      values.rule=form.elements.namedItem('rule').value;
      const result=parcelWeight(values);
      for(const [key,value]of Object.entries(result))form.querySelector(`[data-weight-result="${key}"]`).textContent=number.format(value)+' kg';
      track('calculate_shipping_weight');
    }catch(_){error.textContent=form.dataset.error;for(const x of form.querySelectorAll('[data-weight-result]'))x.textContent='—';}
  });
});
document.querySelectorAll('[data-budget-form]').forEach(form=>{
  form.addEventListener('submit',event=>{
    event.preventDefault();const error=form.querySelector('.tool-error');error.textContent='';
    try{
      const result=parcelBudget(Array.from({length:8},(_,i)=>Number(form.elements.namedItem('cost'+i).value)));
      form.querySelector('[data-budget-result]').textContent=currency.format(result);track('calculate_order_budget');
    }catch(e){error.textContent=e.message==='credit'?form.dataset.creditError:form.dataset.error;form.querySelector('[data-budget-result]').textContent='—';}
  });
});
