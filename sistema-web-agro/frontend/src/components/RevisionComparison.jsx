import React, { useMemo, useState } from 'react'
import { CartesianGrid, Line, LineChart, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { addWeek, paddedDomain, seriesAnalysis } from '../lib/revisionComparison.js'
import DateRangeControl from './DateRangeControl.jsx'
import { isoMonday, observedDates, rangeError } from '../lib/temporalFilters.js'
const names = { palta: 'Palta', uva: 'Uva fresca', arandano: 'Arándano' }
const labels = { unit_fob: ['Valor unitario FOB', 'USD/kg'], volume_kg: ['Volumen registrado', 'kg'], fob_usd: ['FOB total registrado', 'USD'] }
const colors = ['#23834b', '#007bb5', '#a35bc2', '#ce7224', '#d34c68', '#00877d', '#6f65bd', '#7c6724']
const num = (v, digits = 2) => Number(v).toLocaleString('es-PE', { maximumFractionDigits: digits })
const dateLabel = date => new Intl.DateTimeFormat('es-PE', { day: '2-digit', month: 'short', year: 'numeric', timeZone: 'UTC' }).format(new Date(date + 'T00:00:00Z'))
export default function RevisionComparison({ item, data }) {
  const [metric, setMetric] = useState('unit_fob')
  const [start, setStart] = useState(item.previous_week)
  const [end, setEnd] = useState(item.week)
  const [product, setProduct] = useState(item.product)
  const [destination, setDestination] = useState('US')
  const [selected, setSelected] = useState([{ product: item.product, destination: 'US', color: colors[0] }])
  const indexed = selected.length > 1
  const [horizon, setHorizon] = useState(0)
  const markets = useMemo(() => [...new Set(data.weekly_rows.filter(r => r[0] === product).map(r => r[1]))].sort(), [data, product])
  const dest = markets.includes(destination) ? destination : markets[0]
  const analyses = useMemo(() => selected.map(s => ({ ...s, ...seriesAnalysis(data.weekly_rows, s.product, s.destination, metric, isoMonday(start), isoMonday(end)) })), [data, selected, metric, start, end])
  const duplicate = selected.some(s => s.product === product && s.destination === dest)
  const invalid = Boolean(rangeError(start, end))
  const chart = useMemo(() => {
    const dates = analyses[0]?.grid || []
    const rows = dates.map(week => ({ week }))
    if (horizon && dates.length) for (let n = 1; n <= horizon; n++) rows.push({ week: addWeek(dates.at(-1), n) })
    for (const [i, s] of analyses.entries()) {
      const base = s.first?.value
      const convert = value => value == null ? null : indexed ? base > 0 ? value / base * 100 : null : value
      for (const row of rows) {
        row['s' + i] = row.week <= s.anchor ? convert(s.lookup.get(row.week)) : null
        row['p' + i] = horizon && s.ready && row.week >= s.anchor ? convert(s.estimate) : null
      }
    }
    return rows
  }, [analyses, horizon, indexed])
  const domain = paddedDomain(chart.flatMap(r => Object.entries(r).filter(([k]) => k !== 'week').map(([, v]) => v)))
  const unit = indexed ? 'Índice · primera observación = 100' : labels[metric][1]
  function add() { if (!duplicate && dest && selected.length < 8) setSelected([...selected, { product, destination: dest, color: colors.find(c => !selected.some(s => s.color === c)) }]) }
  return <section className="ui-card rounded-xl p-4 md:p-6 space-y-5" aria-label="Comparativa de productos y destinos">
    <h3 className="font-headline-md text-xl">Comparar evolución y estimaciones semanales</h3>
    <div className="grid sm:grid-cols-2 xl:grid-cols-4 gap-4">
      <label className="text-sm">Variable<select className="ui-input rounded-lg p-3 mt-2 w-full" value={metric} onChange={e => setMetric(e.target.value)}>{Object.entries(labels).map(([k, v]) => <option key={k} value={k}>{v[0]}</option>)}</select></label>
      <label className="text-sm">Estimación de referencia<select className="ui-input rounded-lg p-3 mt-2 w-full" value={horizon} onChange={e => setHorizon(Number(e.target.value))}><option value={0}>Sin estimación</option>{[1, 2, 3, 4].map(n => <option key={n} value={n}>{n} semana(s) después del cierre</option>)}</select></label>
    </div>
    <DateRangeControl start={start} end={end} onApply={range=>{setStart(range.start);setEnd(range.end)}} dates={observedDates(data.weekly_rows,selected[0]?.product||item.product,selected[0]?.destination||'US',metric)} label="Rango de la comparativa del archivo" />
    <div className="ui-panel rounded-lg p-4 flex flex-wrap items-end gap-4">
      <label className="text-sm flex-1 min-w-0">Añadir producto<select className="ui-input rounded-lg p-3 mt-2 w-full" value={product} onChange={e => setProduct(e.target.value)}>{Object.entries(names).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select></label>
      <label className="text-sm flex-1 min-w-0">Destino<select className="ui-input rounded-lg p-3 mt-2 w-full" value={dest || ''} onChange={e => setDestination(e.target.value)}>{markets.map(m => <option key={m}>{m}</option>)}</select></label>
      <button onClick={add} disabled={duplicate || !dest || selected.length >= 8} className="ui-input rounded-lg p-3 text-primary disabled:opacity-40">{duplicate ? 'Ya está en el gráfico' : 'Añadir comparativa'}</button>
    </div>
    <p className="text-sm text-on-surface-variant">Periodo sincronizado · escala automática. Con varias series se comparan los cambios en base 100 para que sus magnitudes no oculten las variaciones.</p>
    <div className="flex flex-wrap gap-3" aria-label="Series visibles; pulse para quitar">{selected.map((s, i) => <button key={s.product + s.destination} onClick={() => setSelected(selected.filter((_, index) => index !== i))} className="ui-input rounded-lg px-3 py-2 text-sm" style={{ borderColor: s.color }} aria-label={`Quitar ${names[s.product]} ${s.destination}`}><span style={{ color: s.color }}>●</span> {names[s.product]} · {s.destination} ×</button>)}</div>
    {invalid ? <p role="alert" className="text-error">Seleccione un periodo válido.</p> : selected.length === 0 ? <p role="status">Añada un producto y destino para comenzar.</p> : <>
      <p className="text-sm text-on-surface-variant">{dateLabel(start)} a {dateLabel(end)} · {unit}. Escala automática ajustada a los valores visibles; el eje puede no empezar en cero.</p>
      <div className="h-96 w-full min-w-0"><ResponsiveContainer width="100%" height="100%"><LineChart accessibilityLayer data={chart} margin={{ left: 12, right: 28, top: 16, bottom: 18 }}><CartesianGrid stroke="#889487" strokeDasharray="3 3" opacity={.25} /><XAxis dataKey="week" minTickGap={40} tickFormatter={w => dateLabel(w)} tick={{ fill: '#64748b', fontSize: 11 }} /><YAxis domain={domain} allowDataOverflow width={95} tickFormatter={v => num(v, Math.abs(v) < 20 ? 3 : 0)} tick={{ fill: '#64748b', fontSize: 11 }} /><Tooltip labelFormatter={dateLabel} formatter={(v, name) => [num(v, 3) + ' ' + (indexed ? 'índice' : labels[metric][1]), name]} contentStyle={{ color: '#1b211b', background: '#fff' }} />{horizon > 0 && analyses[0]?.anchor && <ReferenceLine x={analyses[0].anchor} stroke="#889487" label="Cierre" />}{analyses.map((s, i) => <React.Fragment key={s.product + s.destination}><Line name={`${names[s.product]} · ${s.destination} observado`} type="linear" dataKey={'s' + i} stroke={s.color} strokeWidth={3} connectNulls={false} dot={{ r: 3 }} isAnimationActive={false} />{horizon > 0 && s.ready && <Line name={`${names[s.product]} · ${s.destination} referencia`} dataKey={'p' + i} stroke={s.color} strokeDasharray="6 5" dot={{ r: 3 }} isAnimationActive={false} />}</React.Fragment>)}</LineChart></ResponsiveContainer></div>
      <p className="text-xs text-on-surface-variant">Línea continua: observaciones parciales. Cortes: sin registro, nunca cero ni valor arrastrado. Discontinua: estimación de persistencia, no observación. Cada color identifica una serie, no su riesgo. Base 100 permite comparar cambios cuando las magnitudes son muy distintas.</p>
      <div className="grid lg:grid-cols-2 gap-4">{analyses.map(s => <article key={s.product + s.destination} className="ui-panel rounded-lg p-4 text-sm space-y-3"><h4 className="font-semibold" style={{ color: s.color }}>{names[s.product]} · {s.destination}</h4><p>{s.observed.length} de {s.grid.length} semanas con registros; {s.missing} desconocidas.</p>{s.observed.length >= 2 ? <><p>{labels[metric][0]}: {num(s.first.value, 3)} → {num(s.last.value, 3)} {labels[metric][1]}, del {dateLabel(s.first.week)} al {dateLabel(s.last.week)}. Diferencia absoluta: {num(s.last.value - s.first.value, 3)} {labels[metric][1]}.</p><p className={s.delta < 0 ? 'text-error' : 'text-primary'}>{s.delta == null ? 'Porcentaje no calculable: base cero.' : `${s.delta > 0 ? '↑ Subida' : s.delta < 0 ? '↓ Bajada' : '→ Sin cambio'}: ${num(Math.abs(s.delta), 3)} % entre extremos observados.`}</p><p>{s.delta === 0 ? 'La igualdad corresponde a los agregados disponibles; no significa ausencia de registros ni garantiza que cada operación tenga el mismo precio.' : 'La diferencia describe los registros disponibles; cambios de cobertura o composición pueden influir. No demuestra una causa ni una tendencia sostenida.'}</p></> : <p>No hay dos observaciones en este periodo para medir una variación.</p>}{horizon > 0 && (s.ready ? <div><p className="text-tertiary">Referencia semanal de persistencia: {num(s.estimate, 3)} {labels[metric][1]} por semana.</p><ul className="mt-2 space-y-1">{Array.from({ length: horizon }, (_, i) => <li key={i}>{dateLabel(addWeek(s.anchor, i + 1))}: {num(s.estimate, 3)} {labels[metric][1]} (estimado)</li>)}</ul><p className="text-xs text-on-surface-variant mt-2">Último valor al cierre, con cuatro semanas consecutivas previas verificadas. Referencia simple sin ajuste estacional ni intervalo calibrado; no es un modelo entrenado ni un resultado final de tesis. Puede quedar desactualizada fuera del corte.</p></div> : <p className="text-tertiary">No se estima: faltan cuatro observaciones semanales consecutivas hasta el cierre elegido. No se rellenan huecos.</p>)}</article>)}</div>
    </>}
    <p className="text-xs text-on-surface-variant">Fuente: SUNAT/ADUANET, corte {data.generated_on}. Semanas identificadas por su lunes ISO. Última semana incluida en el corte: {data.manifest.calendar.last_target}. No hay observaciones de noviembre en este archivo.</p>
  </section>
}
