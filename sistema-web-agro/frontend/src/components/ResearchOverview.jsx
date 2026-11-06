import React, { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { AreaChart, Area, Brush, BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import ResearchIcon from './ResearchIcon.jsx'
import SourcePanel from './SourcePanel.jsx'
import useReducedMotion from '../lib/useReducedMotion.js'

const products = { palta: 'Palta', uva: 'Uva fresca', arandano: 'Arándano' }
const countryNames = new Intl.DisplayNames(['es'], { type: 'region' })
const country = code => /^[A-Z]{2}$/.test(code) ? `${countryNames.of(code)} (${code})` : code
const fmt = (v, digits = 2) => v == null ? 'No disponible' : v.toLocaleString('es-PE', { maximumFractionDigits: digits })
function Info({ title = 'Información', children }) {
  return <details className="research-info text-xs text-on-surface-variant mt-3"><summary className="cursor-pointer text-primary py-2"><ResearchIcon name="info" />{title}</summary><div className="glass-panel rounded-lg p-3 mt-1 leading-relaxed">{children}</div></details>
}
export default function ResearchOverview({ data }) {
  const [product, setProduct] = useState('palta')
  const [destination, setDestination] = useState('')
  const [start, setStart] = useState('')
  const [end, setEnd] = useState('')
  const reduced = useReducedMotion()
  const [animate, setAnimate] = useState(true)
  const [replay, setReplay] = useState(0)
  const [frequency, setFrequency] = useState('week')
  const [metric, setMetric] = useState('fob')
  const [report, setReport] = useState(null)
  const motion = animate && !reduced
  const chartKey = `${product}-${destination}-${start}-${end}-${frequency}-${replay}`
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
    const period = frequency === 'month' ? r[2].slice(0, 7) : r[2]
    if (!timeline.has(period)) timeline.set(period, { week: period, fob: 0, volume: 0, count: 0, unknown: 0 })
    if (r[6] === 'unknown') timeline.get(period).unknown++
    if (r[6] === 'observed_partial' && Number.isFinite(r[4]) && Number.isFinite(r[5])) {
      const t = timeline.get(period); t.fob += r[5]; t.volume += r[4]; t.count++
    }
  }
  const chart = [...timeline.values()].sort((a, b) => a.week.localeCompare(b.week)).map(r => ({ ...r, fob: r.count ? r.fob : null, volume: r.count ? r.volume : null, value: r.count && r.volume > 0 ? r.fob / r.volume : null }))
  const unknown = rows.filter(r => r[6] === 'unknown').length
  const byDestination = new Map()
  for (const r of observed) byDestination.set(r[1], (byDestination.get(r[1]) || 0) + r[5])
  const ranking = [...byDestination].map(([destination, fob]) => ({ destination, fob })).sort((a, b) => b.fob - a.fob).slice(0, 8)
  const source = data.sources.find(s => s.name.includes('SUNAT'))
  const compact = v => new Intl.NumberFormat('es-PE', { notation: 'compact', maximumFractionDigits: 1 }).format(v)

  const color = { palta: '#6b8e23', uva: '#7c3aed', arandano: '#2563eb' }[product]
  const range = chart.length ? `${chart[0].week} — ${chart[chart.length - 1].week}` : 'Sin datos para esta selección'
  const cells = observed.length + unknown
  const coverage = cells ? observed.length / cells * 100 : null
  const axis = { fill: '#64748b', fontSize: 11 }
  const tooltip = { background: '#fff', color: '#17202a', border: '1px solid #dbe3ea', borderRadius: 8 }
  const sourceLink = <footer className="research-chart-source"><span>Fuente: {source ? <a href={source.url} target="_blank" rel="noreferrer">{source.name} ↗</a> : 'SUNAT'} · corte {data.generated_on}</span><a href={`${import.meta.env.BASE_URL}research/snapshot.json`} download>Descargar datos ↓</a></footer>
  const prepareReport = () => setReport({ product, destination: selected, start, end, frequency, fob, volume, ratio, observed: observed.length, unknown, ranking, chart, hash: data.manifest.views.conservadora.input_sha256 })
  function downloadReport() {
    const payload = { ...report, kind: 'local_calculated_report_not_ai_generation', source: source?.url, final_experiment: false }
    const url = URL.createObjectURL(new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' }))
    const link = document.createElement('a'); link.href = url; link.download = `reporte-${report.product}.json`; link.click(); URL.revokeObjectURL(url)
  }
  const chartHeading = (icon, title, detail) => <div className="research-chart-heading"><h2 className="research-chart-title text-lg font-semibold"><span className="research-icon-badge tone-green"><ResearchIcon name={icon} /></span>{title}</h2><p className="text-xs text-on-surface-variant mt-2">{detail}</p></div>
  return <div className="space-y-5 research-enter">
    <section className="glass-panel rounded-xl p-5 space-y-4" aria-label="Filtros del resumen">
      <div className="flex flex-wrap items-center justify-between gap-3"><h2 className="research-chart-title text-lg font-semibold"><ResearchIcon name="dashboard" />Consulta de exportaciones</h2><button className="text-primary text-sm underline underline-offset-4" onClick={() => { setProduct('palta'); setDestination(''); setStart(''); setEnd(''); setFrequency('week') }}>Restablecer filtros</button></div>
      <div className="grid sm:grid-cols-2 xl:grid-cols-4 gap-4">
        <label className="text-xs text-on-surface-variant">Producto<select className="glass-input rounded-lg p-3 mt-2 w-full" value={product} onChange={e => setProduct(e.target.value)}>{Object.entries(products).map(([id, name]) => <option key={id} value={id}>{name}</option>)}</select></label>
        <label className="text-xs text-on-surface-variant">País de destino<select className="glass-input rounded-lg p-3 mt-2 w-full" value={selected} onChange={e => setDestination(e.target.value)}><option value="">Todos los destinos disponibles</option>{markets.map(m => <option key={m} value={m}>{country(m)}</option>)}</select></label>
        <label className="text-xs text-on-surface-variant">Desde<input type="date" className="glass-input rounded-lg p-3 mt-2 w-full" value={start} onChange={e => setStart(e.target.value)} /></label>
        <label className="text-xs text-on-surface-variant">Hasta<input type="date" className="glass-input rounded-lg p-3 mt-2 w-full" value={end} onChange={e => setEnd(e.target.value)} /></label>
      </div>
      <div className="flex flex-wrap items-center justify-between gap-3 text-xs">
        <p className="text-on-surface-variant"><span className="research-product-dot" style={{ background: color }} />{products[product]} · {selected ? country(selected) : 'Todos los destinos'} · {range}</p>
        <label className="text-on-surface-variant">Agrupación<select aria-label="Agrupación temporal" className="glass-input rounded-lg px-3 py-2 ml-2" value={frequency} onChange={e => setFrequency(e.target.value)}><option value="week">Semanal</option><option value="month">Mensual · por lunes de semana</option></select></label>
      </div>
      <Info title="Periodo y método de agrupación">Sin fechas se incluye todo el periodo disponible. La agrupación mensual asigna cada semana al mes de su lunes; puede diferir del total por fecha diaria de embarque. Las celdas corresponden a combinaciones de producto, destino y semana.</Info>
      {invalid && <p role="alert" className="research-warning text-sm">La fecha inicial debe ser anterior o igual a la final.</p>}
    </section>

    <section className="research-kpi-grid" aria-label="Indicadores de la selección">
      {[
        ['Valor exportado recuperado', fob, 'USD FOB', 'Suma de los registros disponibles', ''],
        ['Peso neto exportado', volume, 'kg', 'Peso neto de los registros disponibles', 'research-kpi-blue'],
        ['Valor unitario FOB', ratio, 'USD/kg', 'Valor FOB total / peso neto total', 'research-kpi-purple'],
        ['Cobertura de datos', coverage, '%', `${fmt(observed.length, 0)} de ${fmt(cells, 0)} celdas con registros`, 'research-kpi-warning'],
      ].map(([label, value, unit, detail, tone]) => <article key={label} className={`research-kpi glass-card rounded-xl p-5 ${tone}`}><p className="text-xs text-on-surface-variant">{label}</p><div className="research-kpi-value">{value == null ? 'Sin datos' : unit === 'USD/kg' || unit === '%' ? fmt(value, unit === '%' ? 1 : 2) : compact(value)}<small>{unit}</small></div><p className="text-xs text-on-surface-variant">{detail}</p>{value != null && unit !== '%' && <details className="mt-2 text-xs text-on-surface-variant"><summary className="cursor-pointer">Valor completo</summary>{fmt(value)} {unit}</details>}</article>)}
    </section>
    <p className="text-xs text-on-surface-variant">Periodo: {range} · Cobertura parcial. Los totales corresponden a la selección recuperada.</p>

    <div className="research-analysis-grid">
      <section className="glass-card research-plot rounded-xl p-5 min-w-0" aria-label="Evolución de las exportaciones">
        <div className="flex flex-wrap justify-between items-center gap-3 mb-4">{chartHeading(metric === 'fob' ? 'fob' : 'volume', 'Evolución de las exportaciones', frequency === 'week' ? 'Serie semanal · lunes de semana ISO' : 'Semanas agrupadas por el mes de su lunes')}
          <div role="tablist" aria-label="Indicador del gráfico" className="research-segmented">{[['fob', 'Valor FOB'], ['volume', 'Peso neto']].map(([id, label]) => <button key={id} role="tab" id={`overview-tab-${id}`} aria-selected={metric === id} aria-controls="overview-metric-panel" onClick={() => setMetric(id)}>{label}</button>)}</div>
        </div>
        <div role="tabpanel" id="overview-metric-panel" aria-labelledby={`overview-tab-${metric}`}>
          {observed.length ? <div className="research-chart-large"><ResponsiveContainer width="100%" height="100%"><AreaChart key={chartKey + metric} data={chart} margin={{ left: 0, right: 12, top: 8, bottom: 0 }}>
            <defs><linearGradient id="overview-fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={color} stopOpacity={0.24} /><stop offset="100%" stopColor={color} stopOpacity={0.02} /></linearGradient></defs>
            <CartesianGrid stroke="#e2e8f0" vertical={false} strokeDasharray="3 3" /><XAxis dataKey="week" minTickGap={60} tick={axis} /><YAxis width={62} tickFormatter={compact} tick={axis} />
            <Tooltip contentStyle={tooltip} formatter={v => [`${fmt(v)} ${metric === 'fob' ? 'USD' : 'kg'}`, metric === 'fob' ? 'Valor FOB' : 'Peso neto']} />
            <Area type="linear" dataKey={metric} stroke={color} fill="url(#overview-fill)" strokeWidth={2.5} dot={false} connectNulls={false} isAnimationActive={motion} animationDuration={250} />
            <Brush dataKey="week" height={22} stroke="#94a3b8" fill="#f8fafc" tickFormatter={v => v.slice(0, 7)} />
          </AreaChart></ResponsiveContainer></div> : <p role="status" className="research-chart-empty">No hay registros para estos filtros. Amplíe el periodo o cambie el destino.</p>}
        </div>
        <Info title="Cómo leer el gráfico">Arrastre la franja inferior para ampliar un tramo del periodo. Los cortes de línea representan ausencia de registros. La selección de la franja afecta al gráfico; los indicadores resumen el rango de los filtros.</Info>{sourceLink}
      </section>

      <section className="glass-card research-plot rounded-xl p-5 min-w-0">
        {chartHeading('markets', 'Principales destinos', 'Hasta 8 destinos por valor FOB · USD')}
        {ranking.length ? <div className="research-chart-large"><ResponsiveContainer width="100%" height="100%"><BarChart data={ranking} layout="vertical" margin={{ left: 0, right: 20 }}>
          <CartesianGrid stroke="#e2e8f0" horizontal={false} /><XAxis type="number" tickFormatter={compact} tick={axis} /><YAxis dataKey="destination" type="category" width={105} tickFormatter={v => country(v).replace(/ \(.*\)/, '')} tick={axis} />
          <Tooltip labelFormatter={country} contentStyle={tooltip} formatter={v => [`${fmt(v)} USD`, 'Valor FOB']} /><Bar dataKey="fob" fill={color} radius={[0, 4, 4, 0]} isAnimationActive={motion} animationDuration={250} />
        </BarChart></ResponsiveContainer></div> : <p className="research-chart-empty">No hay destinos con registros para esta selección.</p>}
        <Link className="text-sm text-primary underline underline-offset-4" to="/dashboard?view=series">Comparar dos destinos ↗</Link>{sourceLink}
      </section>
    </div>

    <div className="research-support-grid">
      <section className="glass-card research-plot rounded-xl p-5 min-w-0">
        {chartHeading('unit', 'Valor unitario FOB', 'USD/kg · razón de sumas por periodo')}
        {observed.length ? <div className="research-chart-medium"><ResponsiveContainer width="100%" height="100%"><LineChart data={chart}><CartesianGrid stroke="#e2e8f0" vertical={false} /><XAxis dataKey="week" minTickGap={70} tick={axis} /><YAxis width={45} tick={axis} /><Tooltip contentStyle={tooltip} formatter={v => [`${fmt(v)} USD/kg`, 'Valor unitario FOB']} /><Line dataKey="value" stroke="#2563eb" strokeWidth={2.5} dot={false} connectNulls={false} isAnimationActive={motion} animationDuration={250} /></LineChart></ResponsiveContainer></div> : <p className="research-chart-empty">Sin observaciones válidas.</p>}
        <Info title="Interpretación del valor unitario">Se calcula dividiendo el valor FOB por el peso neto. Puede cambiar por la composición de destinos y operaciones; no equivale a una cotización de mercado.</Info>{sourceLink}
      </section>
      <section className="glass-card research-plot rounded-xl p-5 min-w-0">
        {chartHeading('coverage', 'Cobertura de datos', 'Celdas producto–destino–semana · selección actual')}
        <p className="text-xs text-on-surface-variant my-3"><span className="text-primary">● Con registros parciales</span> · <span style={{ color: '#64748b' }}>● Sin registros recuperados</span></p>
        {chart.length ? <div className="research-chart-medium"><ResponsiveContainer width="100%" height="100%"><BarChart data={chart}><XAxis dataKey="week" minTickGap={70} tick={axis} /><YAxis allowDecimals={false} tick={axis} width={38} /><Tooltip contentStyle={tooltip} /><Bar dataKey="count" name="Con registros parciales" stackId="coverage" fill="#176b4d" isAnimationActive={motion} /><Bar dataKey="unknown" name="Sin registros recuperados" stackId="coverage" fill="#cbd5e1" isAnimationActive={motion} /></BarChart></ResponsiveContainer></div> : <p className="research-chart-empty">Sin celdas en la selección.</p>}
        <p className="text-xs text-on-surface-variant mt-3">{fmt(observed.length, 0)} con registros · {fmt(unknown, 0)} sin registros recuperados. La ausencia no equivale a cero exportaciones.</p>{sourceLink}
      </section>
    </div>

    <section className="research-report-panel glass-card rounded-xl p-5">
      <div><h2 className="research-chart-title text-lg font-semibold"><ResearchIcon name="source" />Reporte de esta selección</h2><p className="text-sm text-on-surface-variant mt-2">Conserve los indicadores, las series y sus referencias en un archivo descargable.</p></div>
      <button disabled={!observed.length || invalid} className="research-action rounded-lg px-5 py-3 text-sm disabled:opacity-40" onClick={prepareReport}>Generar reporte de esta selección</button>
      {report && <article className="research-prepared-report space-y-3" aria-live="polite"><h3 className="font-semibold">Reporte preparado · {products[report.product]} · {report.destination ? country(report.destination) : 'Todos los destinos'}</h3><p className="text-sm text-on-surface-variant">{report.start || 'Inicio disponible'} — {report.end || 'Fin disponible'} · {report.frequency === 'week' ? 'Semanal' : 'Semanas agrupadas por mes'}</p><p className="text-sm">Valor FOB: {fmt(report.fob)} USD · Peso neto: {fmt(report.volume)} kg · Valor unitario: {fmt(report.ratio)} USD/kg</p><button onClick={downloadReport} className="glass-input rounded-lg px-4 py-2 text-primary text-sm">Descargar reporte y datos · JSON ↓</button><p className="text-xs text-on-surface-variant">El archivo conserva la selección al generarlo, incluso si cambia los filtros después.</p></article>}
      <details className="research-info text-xs text-on-surface-variant research-report-details"><summary className="cursor-pointer py-2">Alcance del reporte</summary><p>Resumen calculado con los registros del corte local. Incluye el hash de entrada para comprobar su procedencia.</p></details>
    </section>
    <SourcePanel data={data} />
    <details className="glass-panel rounded-xl p-5 research-info text-sm text-on-surface-variant"><summary className="cursor-pointer font-semibold">Estado de la investigación y evidencia</summary><p className="mt-3">El piloto tiene cobertura parcial y la evaluación final permanece pendiente.</p><div className="grid sm:grid-cols-2 xl:grid-cols-4 gap-4 mt-4">{[
      ['Pronóstico', 'Evaluación final pendiente', 'pronosticos'],
      ['Aporte contextual', 'Elegibilidad temporal no acreditada', 'proceso'],
      ['Variaciones para revisar', 'Caracterización histórica pendiente', 'senales'],
      ['Reportes documentados', 'Pilotos disponibles; evaluación pendiente', 'ia'],
    ].map(([title, detail, view]) => <Link key={title} to={`/dashboard?view=${view}`} className="research-source-card"><strong className="text-on-surface">{title} ↗</strong><p className="text-xs mt-2">{detail}</p></Link>)}</div></details>
    <details className="research-info text-xs text-on-surface-variant"><summary className="cursor-pointer py-2">Preferencias de visualización</summary><label className="flex items-center gap-2 mt-2"><input type="checkbox" checked={animate} disabled={reduced} onChange={e => setAnimate(e.target.checked)} />Animar gráficos{reduced ? ' · movimiento reducido del sistema' : ''}</label><button disabled={!motion} onClick={() => setReplay(r => r + 1)} className="text-primary underline mt-3">Repetir animación</button></details>
  </div>
}
