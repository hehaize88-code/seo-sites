import rate from '../content/exchange-rate.json';
export const exchangeRate=rate;
export function usd(raw:string){const clean=raw.trim().replace(/[,¥￥\s]/g,'').replace(/^(CNY|RMB)/i,'');if(!/^\d+(\.\d+)?$/.test(clean))return '—';return 'US$'+(Number(clean)*rate.rates.USD).toFixed(2);}
