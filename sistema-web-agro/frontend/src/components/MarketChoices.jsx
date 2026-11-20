import { useMemo, useState } from 'react'
const regions = new Intl.DisplayNames(['es'],{type:'region'})
export const marketName = code => /^[A-Z]{2}$/.test(code)?`${regions.of(code)} (${code})`:code
export default function MarketChoices({ rows, product, start, end, selected, onSelect }) {
  const [search,setSearch]=useState(''),[all,setAll]=useState(false)
  const markets=useMemo(()=>{const map=new Map();for(const r of rows){if(r[0]!==product)continue;if(!map.has(r[1]))map.set(r[1],{code:r[1],fob:0,count:0,last:null});if((!start||r[2]>=start)&&(!end||r[2]<=end)&&r[5]!=null){const m=map.get(r[1]);m.fob+=r[5];m.count++;m.last=!m.last||r[2]>m.last?r[2]:m.last}}return [...map.values()].sort((a,b)=>b.fob-a.fob||a.code.localeCompare(b.code))},[rows,product,start,end])
  const filtered=markets.filter(m=>marketName(m.code).toLowerCase().includes(search.toLowerCase()))
  return <section className="ui-panel rounded-xl p-5 space-y-4" aria-label="Destinos disponibles">
    <div className="flex flex-wrap justify-between gap-3"><div><h3 className="font-headline-md text-xl">Explore otros destinos</h3><p className="text-xs text-on-surface-variant mt-2">{markets.length} destinos del producto · {markets.filter(m=>m.count).length} con registros en el rango. Puede cambiar de país sin perder las fechas.</p></div><button className="ui-input rounded-lg px-4 py-2 text-sm text-primary" aria-pressed={!selected} onClick={()=>onSelect('')}>Todos los destinos</button></div>
    <label className="text-sm block">Buscar país o código<input className="ui-input rounded-lg p-3 mt-2 w-full" value={search} onChange={e=>setSearch(e.target.value)} placeholder="Países Bajos, China, España, NL…" /></label>
    <div className="grid sm:grid-cols-2 xl:grid-cols-4 gap-3">{(all||search?filtered:filtered.slice(0,8)).map(m=><button key={m.code} className={`ui-input rounded-lg p-3 text-left ${selected===m.code?'border-primary text-primary':''}`} aria-pressed={selected===m.code} onClick={()=>onSelect(m.code)}><strong className="text-sm">{marketName(m.code)}</strong><span className="block text-xs text-on-surface-variant mt-2">{m.count?`${m.count} semanas con registros · última: ${m.last}`:'Sin registros en este rango'}</span></button>)}</div>
    {!filtered.length&&<p role="status" className="text-sm">No hay destinos que coincidan con la búsqueda.</p>}
    {!search&&filtered.length>8&&<button className="text-primary text-sm underline" onClick={()=>setAll(!all)}>{all?'Mostrar principales destinos':`Mostrar los ${markets.length} destinos`}</button>}
  </section>
}
