import { useEffect, useState } from 'react'
import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { paddedDomain } from '../lib/revisionComparison.js'
const colors=['#2563eb','#b45309','#7c3aed','#0891b2','#be185d','#64748b']
const number=v=>v==null?'Sin dato':Number(v).toLocaleString('es-PE',{maximumFractionDigits:3})
export default function TrainingChart({job}) {
  const [hidden,setHidden]=useState([])
  useEffect(()=>setHidden([]),[job.id])
  const results=Object.entries(job.results||{}).filter(([,r])=>r.status==='completed')
  const models=results.flatMap(([lib,r])=>(r.models||[]).map(m=>({...m,id:lib+'/'+m.model,weeks:r.weeks})))
  if(!models.length)return null
  const visible=models.filter(m=>!hidden.includes(m.id))
  const actual=new Map(results.flatMap(([,r])=>r.weeks.map((w,i)=>[w,r.actual[i]])))
  const graph=[...actual].sort(([a],[b])=>a.localeCompare(b)).map(([week,observed])=>({week,observed,...Object.fromEntries(visible.map(m=>[m.id,m.values[m.weeks.indexOf(week)]??null]))}))
  const unit=job.config.target==='unit_fob'?'USD/kg':'kg'
  return <section className="ui-panel rounded-xl p-4 space-y-3" aria-label="Gráfico del entrenamiento seleccionado">
    <h3 className="font-semibold">Estimado frente a observado · {job.validation_weeks.length} semana(s) reservadas</h3>
    <p className="text-xs text-on-surface-variant">Resultados de esta ejecución; no reemplazan los archivos de XGBoost/LightGBM. Una sola semana se representa con puntos, sin inventar una tendencia.</p>
    <div className="flex flex-wrap gap-2" aria-label="Métodos experimentales visibles">{models.map((m,i)=><button key={m.id} aria-pressed={!hidden.includes(m.id)} className="ui-input rounded-lg px-3 py-2 text-xs" style={{borderColor:colors[i%colors.length],opacity:hidden.includes(m.id)?.55:1}} onClick={()=>setHidden(current=>current.includes(m.id)?current.filter(id=>id!==m.id):[...current,m.id])}>{m.id}</button>)}</div>
    <div className="h-80 w-full min-w-0"><ResponsiveContainer width="100%" height="100%"><LineChart accessibilityLayer data={graph} margin={{left:8,right:25,top:15,bottom:10}}><CartesianGrid stroke="#dbe3ea" strokeDasharray="3 3"/><XAxis dataKey="week" minTickGap={45} tick={{fontSize:11}}/><YAxis domain={paddedDomain(graph.flatMap(r=>[r.observed,...visible.map(m=>r[m.id])]))} allowDataOverflow width={85} tickFormatter={number} tick={{fontSize:11}}/><Tooltip formatter={(v,n)=>[number(v)+' '+unit,n]}/><Line dataKey="observed" name="Observado" stroke="#176b4d" strokeWidth={3} dot={{r:5}} isAnimationActive={false}/>{visible.map(m=><Line key={m.id} dataKey={m.id} name={m.id} stroke={colors[models.indexOf(m)%colors.length]} strokeWidth={2} strokeDasharray="5 4" dot={{r:4}} isAnimationActive={false}/>)}</LineChart></ResponsiveContainer></div>
    <p className="text-xs text-on-surface-variant">Verde: observado. Trazos de colores: métodos. Escala automática en {unit}; sin intervalos calibrados.</p>
  </section>
}
