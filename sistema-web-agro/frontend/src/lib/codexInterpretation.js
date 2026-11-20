import { addWeek, weekGrid } from './revisionComparison.js'
const months = {ENE:'01',FEB:'02',MAR:'03',ABR:'04',MAY:'05',JUN:'06',JUL:'07',AGO:'08',SEP:'09',OCT:'10',NOV:'11',DIC:'12'}
export function samePeriodContext(context, start, end, product) {
  const weeks=weekGrid(start,end)
  const prev=weeks.map(w=>addWeek(w,-weeks.length))
  function climate(dates){
    const records=dates.map(w=>context.weather.weekly.find(r=>r.week===w)).filter(Boolean)
    const expected=dates.length*7
    const result={weeks:dates.length,records:records.length,expected}
    for(const key of ['T2M_MAX','T2M_MIN','PRECTOTCORR','RH2M']){
      const valid=records.filter(r=>r[key]!=null&&r.days[key]>0)
      const days=valid.reduce((s,r)=>s+r.days[key],0)
      result[key]={days,complete:expected>0&&days===expected,value:days?key==='PRECTOTCORR'?valid.reduce((s,r)=>s+r[key],0):valid.reduce((s,r)=>s+r[key]*r.days[key],0)/days:null}
    }
    return result
  }
  const monthSet=new Set()
  for(const week of weeks){monthSet.add(week.slice(0,7));monthSet.add(new Date(Date.parse(week+'T00:00:00Z')+6*86400000).toISOString().slice(0,7))}
  return {weeks,climate:climate(weeks),previousClimate:climate(prev),previousStart:prev[0],previousEnd:prev.at(-1),exchange:context.exchange.filter(r=>monthSet.has(r.month)),months:[...monthSet].sort(),local:context.local_prices.filter(r=>{const [month,year]=r.periodo_fuente.split('-');return r.producto===product&&monthSet.has(year+'-'+months[month])})}
}
export function experimentalNarrative(job) {
  const results=Object.entries(job.results||{}).filter(([,r])=>r.status==='completed')
  const candidates=results.flatMap(([library,r])=>(r.models||[]).map(m=>({...m,library,actual:r.actual,weeks:r.weeks}))).filter(m=>Number.isFinite(m.mae))
  if(!candidates.length)return {models:[],paragraphs:['La ejecución todavía no ofrece resultados completos para interpretar.']}
  const ordered=candidates.slice().sort((a,b)=>a.mae-b.mae)
  const best=ordered[0],unit=job.config.target==='unit_fob'?'USD/kg':'kg'
  const fmt=v=>Number(v).toLocaleString('es-PE',{maximumFractionDigits:3})
  const above=candidates.filter(m=>m.values.every((v,i)=>v>m.actual[i])).length
  const baseline=candidates.find(m=>m.library==='statsforecast'&&m.model==='Naive')
  return {models:candidates.map(m=>({name:m.model,library:m.library==='autogluon'?'AutoGluon TimeSeries':'StatsForecast',version:job.versions[m.library==='autogluon'?'autogluon.timeseries':'statsforecast'],url:m.library==='autogluon'?'https://auto.gluon.ai/stable/tutorials/timeseries/forecasting-model-zoo.html':'https://github.com/Nixtla/statsforecast'})),paragraphs:[
    `En el bloque reservado de ${job.validation_weeks.length} ${job.validation_weeks.length===1?'semana':'semanas'}, ${best.model} (${best.library}) obtuvo el menor error absoluto medio entre los métodos completados: ${fmt(best.mae)} ${unit}. Esta comparación utiliza el mismo bloque externo, no datos de ajuste.`,
    `${above} de ${candidates.length} métodos sobreestimaron todos los valores del bloque. ${above===candidates.length?'El patrón compartido sugiere un cambio que los modelos no anticiparon en este contraste; no identifica por sí mismo su causa.':'Los métodos reaccionaron de manera distinta; conviene estudiar el error por semana antes de elegir una configuración.'}`,
    baseline?`La referencia Naive tuvo un MAE de ${fmt(baseline.mae)} ${unit}. ${best.model==='Naive'?'La mayor complejidad de los otros modelos no aportó una mejora en este bloque; la persistencia es la referencia que deben superar en más ventanas.':'La mejora de un método en este bloque debe confirmarse en más ventanas temporales antes de adoptarlo.'}`:'No hay referencia Naive completada para contrastar la complejidad del modelo.',
    'El clima, el dólar y los precios locales que se muestran debajo son contexto retrospectivo por fecha. Ninguno fue incorporado como variable explicativa a estos ajustes univariados; no se les atribuye el error del modelo ni un efecto causal.'
  ]}
}
