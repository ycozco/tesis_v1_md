import React, { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import useReducedMotion from '../lib/useReducedMotion.js'

const products = { palta: 'Palta', uva: 'Uva fresca', arandano: 'Arándano' }
const fmt = (v, digits = 2) => v == null ? 'No disponible' : v.toLocaleString('es-PE', { maximumFractionDigits: digits })
export default function ResearchOverview({ data }) {
  const [product, setProduct] = useState('palta')
  const [destination, setDestination] = useState('')
  const [start, setStart] = useState('')
  const [end, setEnd] = useState('')
  const reduced = useReducedMotion()
  const markets = [...new Set(data.weekly_rows.filter(r => r[0] === product).map(r => r[1]))].sort()
  const selected = markets.includes(destination) ? destination : ''
  const invalid = Boolean(start && end && start > end)
  const rows = useMemo(() => invalid ? [] : data.weekly_rows.filter(r => r[0] === product && (!selected || r[1] === selected) && (!start || r[2] >= start) && (!end || r[2] <= end)), [data, product, selected, start, end, invalid])
  const observed = rows.filter(r => r[6] === 'observed_partial' && Number.isFinite(r[4]) && Number.isFinite(r[5]))
  const volume = observed.length ? observed.reduce((sum, r) => sum + r[4], 0) : null
  const fob = observed.length ? observed.reduce((sum, r) => sum + r[5], 0) : null
  const ratio = volume > 0 ? fob / volume : null
  const timeline = new Map()
  for (const r of rows) {
    if (!timeline.has(r[2])) timeline.set(r[2], { week: r[2], fob: 0, volume: 0, count: 0, unknown: 0 })
    if (r[6] === 'unknown') timeline.get(r[2]).unknown++
    if (r[6] === 'observed_partial' && Number.isFinite(r[4]) && Number.isFinite(r[5])) {
      const t = timeline.get(r[2]); t.fob += r[5]; t.volume += r[4]; t.count++
    }
  }
  const chart = [...timeline.values()].sort((a, b) => a.week.localeCompare(b.week)).map(r => ({ ...r, fob: r.count ? r.fob : null, volume: r.count ? r.volume : null, value: r.count && r.volume > 0 ? r.fob / r.volume : null }))
  const unknown = rows.filter(r => r[6] === 'unknown').length
  const byDestination = new Map()
  for (const r of observed) byDestination.set(r[1], (byDestination.get(r[1]) || 0) + r[5])
  const ranking = [...byDestination].map(([destination, fob]) => ({ destination, fob })).sort((a, b) => b.fob - a.fob).slice(0, 8)
  const source = data.sources.find(s => s.name.includes('SUNAT'))
  const compact = v => new Intl.NumberFormat('es-PE', { notation: 'compact', maximumFractionDigits: 1 }).format(v)
  const sourceLink = <p className="text-xs text-on-surface-variant mt-4">Fuente: {source ? <a href={source.url} target="_blank" rel="noreferrer" className="text-primary underline">{source.name} ↗</a> : 'SUNAT'} · elaboración semanal del piloto. <a className="text-primary underline" href={`${import.meta.env.BASE_URL}research/snapshot.json`} download>Datos y referencias ↓</a></p>
  function Trend({ title, field, unit, color }) {
    return <section className="glass-card rounded-xl p-5 min-w-0"><h2 className="font-headline-md text-xl mb-2">{title}</h2><p className="text-xs text-on-surface-variant mb-4">{unit} por semana · solo registros recuperados</p>{observed.length ? <div style={{ height: 230, width: '100%' }}><ResponsiveContainer><LineChart data={chart}><CartesianGrid stroke="#3f4a3f" vertical={false} /><XAxis dataKey="week" minTickGap={80} tick={{ fill: '#becabc', fontSize: 10 }} /><YAxis width={58} tickFormatter={compact} tick={{ fill: '#becabc', fontSize: 10 }} /><Tooltip contentStyle={{ background: '#171d17', border: '1px solid #3f4a3f' }} formatter={v => [`${fmt(v)} ${unit}`, title]} /><Line dataKey={field} stroke={color} dot={false} connectNulls={false} strokeWidth={2} isAnimationActive={!reduced} animationDuration={250} /></LineChart></ResponsiveContainer></div> : <p className="py-8 text-sm">Sin observaciones para estos filtros.</p>}{sourceLink}</section>
  }
  return <div className="space-y-6 research-enter">
    <section className="glass-panel rounded-xl p-5 space-y-4" aria-label="Filtros del resumen">
      <div className="flex flex-wrap justify-between gap-2"><h2 className="font-headline-md text-xl">Resultados históricos disponibles</h2><span className="text-xs text-primary">Piloto gráfico · {fmt(data.manifest.views.conservadora.rows, 0)} registros</span></div>
      <div className="grid sm:grid-cols-2 xl:grid-cols-4 gap-4">
        <label className="text-xs text-on-surface-variant">Producto<select className="glass-input rounded-lg p-3 mt-2 w-full" value={product} onChange={e => setProduct(e.target.value)}>{Object.entries(products).map(([id, name]) => <option key={id} value={id}>{name}</option>)}</select></label>
        <label className="text-xs text-on-surface-variant">País de destino<select className="glass-input rounded-lg p-3 mt-2 w-full" value={selected} onChange={e => setDestination(e.target.value)}><option value="">Todos los destinos disponibles</option>{markets.map(m => <option key={m}>{m}</option>)}</select></label>
        <label className="text-xs text-on-surface-variant">Desde · sin fecha incluye todo<input type="date" className="glass-input rounded-lg p-3 mt-2 w-full" value={start} onChange={e => setStart(e.target.value)} /></label>
        <label className="text-xs text-on-surface-variant">Hasta · sin fecha incluye todo<input type="date" className="glass-input rounded-lg p-3 mt-2 w-full" value={end} onChange={e => setEnd(e.target.value)} /></label>
      </div>
      <p className="text-xs text-on-surface-variant">{products[product]} · {selected || 'todos los destinos'} · {chart.length ? `${chart[0].week} a ${chart[chart.length - 1].week}` : 'sin semanas disponibles'}. Semanas según fecha de embarque; códigos de país conservados de la fuente.</p>
      {invalid && <p role="alert" className="text-error text-sm">La fecha inicial debe ser anterior o igual a la final.</p>}
    </section>
    <div className="glass-panel rounded-xl px-5 py-3 flex flex-wrap gap-x-6 gap-y-2 text-xs text-on-surface-variant"><span>FOB: <strong className="text-on-surface">{fmt(fob)} USD</strong></span><span>Volumen: <strong className="text-on-surface">{fmt(volume)} kg</strong></span><span>Valor unitario: <strong className="text-on-surface">{fmt(ratio)} USD/kg</strong></span></div>
    <div className="grid xl:grid-cols-2 gap-5"><Trend title="Valor FOB recuperado" field="fob" unit="USD" color="#76db8f" /><Trend title="Volumen recuperado" field="volume" unit="kg" color="#89ceff" /></div>
    <div className="grid xl:grid-cols-2 gap-5">
      <section className="glass-card rounded-xl p-5 min-w-0"><h2 className="font-headline-md text-xl mb-2">Destinos por FOB recuperado</h2><p className="text-xs text-on-surface-variant mb-4">Hasta ocho destinos de la selección · no representa el mercado completo</p>{ranking.length ? <div style={{ height: 260 }}><ResponsiveContainer><BarChart data={ranking} layout="vertical" margin={{ left: 0, right: 16 }}><CartesianGrid stroke="#3f4a3f" horizontal={false} /><XAxis type="number" tickFormatter={compact} tick={{ fill: '#becabc', fontSize: 10 }} /><YAxis dataKey="destination" type="category" width={40} tick={{ fill: '#becabc', fontSize: 11 }} /><Tooltip contentStyle={{ background: '#171d17' }} formatter={v => [`${fmt(v)} USD`, 'FOB']} /><Bar dataKey="fob" fill="#76db8f" isAnimationActive={!reduced} animationDuration={250} /></BarChart></ResponsiveContainer></div> : <p className="py-8 text-sm">Sin destinos observados.</p>}{sourceLink}</section>
      <section className="glass-card rounded-xl p-5 min-w-0"><h2 className="font-headline-md text-xl mb-2">Disponibilidad dentro del panel</h2><p className="text-xs text-on-surface-variant mb-4">Celdas por semana: verde con registros parciales; gris desconocidas. No certifica cobertura completa.</p>{chart.length ? <div style={{ height: 260 }}><ResponsiveContainer><BarChart data={chart}><XAxis dataKey="week" minTickGap={80} tick={{ fill: '#becabc', fontSize: 10 }} /><YAxis allowDecimals={false} tick={{ fill: '#becabc', fontSize: 10 }} width={35} /><Tooltip contentStyle={{ background: '#171d17' }} /><Bar dataKey="count" name="Con registros parciales" stackId="coverage" fill="#76db8f" isAnimationActive={!reduced} /><Bar dataKey="unknown" name="Desconocidas" stackId="coverage" fill="#889487" isAnimationActive={!reduced} /></BarChart></ResponsiveContainer></div> : <p className="py-8 text-sm">Sin celdas en la selección.</p>}<p className="text-xs text-on-surface-variant mt-3">{fmt(observed.length, 0)} con registros · {fmt(unknown, 0)} desconocidas. Ausencia de registro no significa exportación cero.</p>{sourceLink}</section>
    </div>
    <section className="glass-card rounded-xl p-5"><h2 className="font-headline-md text-xl mb-2">Evolución del valor unitario observado</h2><p className="text-xs text-on-surface-variant mb-5">USD/kg · razón de sumas por semana para los destinos seleccionados. La composición de destinos puede cambiar; los huecos no se conectan.</p>
      {observed.length ? <div style={{ height: 288, width: "100%", minWidth: 0 }}><ResponsiveContainer width="100%" height="100%"><LineChart data={chart}><CartesianGrid stroke="#3f4a3f" vertical={false} /><XAxis dataKey="week" minTickGap={60} tick={{ fill: '#becabc', fontSize: 10 }} /><YAxis width={65} tick={{ fill: '#becabc', fontSize: 11 }} /><Tooltip contentStyle={{ background: '#171d17', border: '1px solid #3f4a3f' }} formatter={v => [`${fmt(v)} USD/kg`, 'Valor unitario']} /><Line dataKey="value" stroke="#76db8f" strokeWidth={2} dot={false} connectNulls={false} isAnimationActive={!reduced} animationDuration={250} /></LineChart></ResponsiveContainer></div> : <p role="status" className="py-8 text-on-surface-variant">No hay observaciones válidas para estos filtros.</p>}
      {sourceLink}
    </section>
    <section className="glass-panel rounded-xl p-5"><h2 className="font-headline-md text-xl mb-3">Alcance de los datos</h2><p className="text-sm text-on-surface-variant leading-relaxed">Los totales corresponden a registros recuperados con cobertura parcial, no al total del mercado. Las celdas desconocidas no se imputan como cero. El conteo describe el panel disponible y no certifica semanas completas. La colección ampliada de 101.546 registros permanece separada de este piloto gráfico.</p><div className="flex flex-wrap gap-4 mt-4 text-sm text-primary"><Link className="underline" to="/dashboard?view=fuentes">Fuentes y enlaces ↗</Link><Link className="underline" to="/dashboard?view=proceso">Verificar versión y archivos ↗</Link></div></section>
    <section><h2 className="font-headline-md text-xl mb-4">Estado de los resultados de la tesis</h2><div className="grid sm:grid-cols-2 gap-4">{[
      ['H1 · Pronóstico', 'Evaluación final pendiente', 'Sin pronóstico futuro certificado ni intervalos finales. Faltan elegibilidad temporal, selección y calendario.', 'pronosticos'],
      ['H2 · Aporte contextual', 'No evaluable en la colección actual', 'La disponibilidad temporal compatible no se pudo acreditar. No confirma ni refuta un efecto.', 'proceso'],
      ['H3 · Señales', 'Piloto técnico artificial', 'Motor probado con 189 casos artificiales; caracterización histórica final pendiente.', 'senales'],
      ['H4 · Reportes', 'Piloto expuesto; evaluación pendiente', 'Tres respuestas Codex archivadas. Faltan revisión humana y las 180 salidas finales controladas.', 'ia'],
    ].map(([title, status, detail, view]) => <article className="glass-card rounded-xl p-5" key={title}><h3 className="text-lg font-semibold">{title}</h3><p className="text-primary text-sm mt-2">{status}</p><p className="text-sm text-on-surface-variant mt-3 leading-relaxed">{detail}</p><Link className="inline-block mt-4 text-sm text-primary underline" to={`/dashboard?view=${view}`}>Consultar evidencia ↗</Link></article>)}</div></section>
  </div>
}
