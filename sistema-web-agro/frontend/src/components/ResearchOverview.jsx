import { MarketContextCards } from './MarketContext.jsx'
import { Button } from './ui/button.jsx'
import { Tabs, TabsList, TabsTrigger, TabsContent } from './ui/tabs.jsx'
import { useMemo, useState } from 'react'
import MarketChoices from './MarketChoices.jsx'
import PriceSummary from './PriceSummary.jsx'
import { paddedDomain } from '../lib/revisionComparison.js'
import { Link, useSearchParams } from 'react-router-dom'
import { AreaChart, Area, Brush, BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import ResearchIcon from './ResearchIcon.jsx'
import SourcePanel from './SourcePanel.jsx'
import useReducedMotion from '../lib/useReducedMotion.js'
import DateRangeControl from './DateRangeControl.jsx'
import { isoMonday, observedDates, rangePreset } from '../lib/temporalFilters.js'

const products = { palta: 'Palta', uva: 'Uva fresca', arandano: 'Arándano' }
const countryNames = new Intl.DisplayNames(['es'], { type: 'region' })
const country = code => /^[A-Z]{2}$/.test(code) ? `${countryNames.of(code)} (${code})` : code
const fmt = (v, digits = 2) => v == null ? 'No disponible' : v.toLocaleString('es-PE', { maximumFractionDigits: digits })
function Info({ title = 'Información', children }) {
  return <details className="research-info text-xs text-on-surface-variant mt-3"><summary className="cursor-pointer text-primary py-2"><ResearchIcon name="info" />{title}</summary><div className="ui-panel rounded-lg p-3 mt-1 leading-relaxed">{children}</div></details>
}
export default function ResearchOverview({ data }) {
  const [params, setParams] = useSearchParams()
  function viewUrl(view) { const query = new URLSearchParams(params); query.set('view', view); return `/dashboard?${query}` }
  const product = Object.keys(products).includes(params.get('product')) ? params.get('product') : 'palta'
  const destination = params.get('destination') ?? ''
  const dates = useMemo(() => observedDates(data.weekly_rows, product, destination), [data, product, destination])
  const defaults = rangePreset(dates, 12)
  function update(key, value) { setParams(current => { const next = new URLSearchParams(current); next.set(key, value); return next }, { replace: true }) }
  const setProduct = value => update('product', value)
  const setDestination = value => update('destination', value)
  const start = params.get('start') ?? defaults.start
  const end = params.get('end') ?? defaults.end
  function applyRange(range) {
    setParams(current => { const next = new URLSearchParams(current); next.set('start', range.start); next.set('end', range.end); return next }, { replace: true })
  }
  const reduced = useReducedMotion()
  const [animate, setAnimate] = useState(true)
  const [replay, setReplay] = useState(0)
  const [frequency, setFrequency] = useState('week')
  const [metric, setMetric] = useState('value')
  const [report, setReport] = useState(null)
  const motion = animate && !reduced
  const chartKey = `${product}-${destination}-${start}-${end}-${frequency}-${replay}`
  const markets = [...new Set(data.weekly_rows.filter(r => r[0] === product).map(r => r[1]))].sort()
  const selected = markets.includes(destination) ? destination : ''
  const invalid = Boolean(start && end && start > end)
  const weekStart = isoMonday(start), weekEnd = isoMonday(end)
  const rows = useMemo(() => invalid ? [] : data.weekly_rows.filter(r => r[0] === product && (!selected || r[1] === selected) && (!weekStart || r[2] >= weekStart) && (!weekEnd || r[2] <= weekEnd)), [data, product, selected, weekStart, weekEnd, invalid])
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
    <MarketContextCards/>
    <div className="observatory-section-label"><span>Corte de investigación · {data.generated_on}</span><h2>Panorama de exportaciones</h2></div>
    <section className="observatory-toolbar" aria-label="Filtros del resumen">
      <div className="observatory-products" aria-label="Producto seleccionado">{Object.entries(products).map(([id,name])=><button key={id} aria-pressed={product===id} onClick={()=>setProduct(id)}><span style={{background:{palta:'#748744',uva:'#80649d',arandano:'#507da8'}[id]}}/>{name}</button>)}</div>
      <div className="observatory-toolbar-fields"><label>Destino<select aria-label="País de destino" value={selected} onChange={e=>setDestination(e.target.value)}><option value="">Todos los destinos</option>{markets.map(m=><option key={m} value={m}>{country(m)}</option>)}</select></label>
      <label>Periodo<select aria-label="Periodo del panorama" value="custom" onChange={e=>{if(e.target.value!=='custom')applyRange(rangePreset(dates,Number(e.target.value)))}}><option value="custom">{start} — {end}</option><option value="4">Últimas 4 semanas</option><option value="12">Últimas 12 semanas</option><option value="26">Últimos 6 meses aprox.</option><option value="0">Todo el histórico</option></select></label>
      <details className="observatory-custom-period"><summary>Ajustar fechas</summary><div><DateRangeControl start={start} end={end} onApply={applyRange} dates={dates} label="Rango del panorama" /><label className="text-sm">Agrupación<select aria-label="Agrupación temporal" className="ui-input p-2 ml-3" value={frequency} onChange={e=>setFrequency(e.target.value)}><option value="week">Semanal</option><option value="month">Mensual · por lunes de semana</option></select></label><Info title="Periodo y método de agrupación">Las semanas se asignan al mes de su lunes. La agrupación puede diferir del total por fecha diaria de embarque. Las celdas son combinaciones de producto, destino y semana.</Info></div></details></div>
      {invalid&&<p role="alert" className="text-error text-sm">La fecha inicial debe ser anterior o igual a la final.</p>}
    </section>
    <section className="research-kpi-grid" aria-label="Indicadores de la selección">
      {[
        ['Valor exportado recuperado', fob, 'USD FOB', 'Registros recuperados · selección actual', ''],
        ['Peso neto exportado', volume, 'kg', 'Acumulado en el periodo seleccionado', 'research-kpi-blue'],
        ['Valor unitario FOB', ratio, 'USD/kg', 'Valor FOB total / peso neto total', 'research-kpi-purple'],
        ['Cobertura de datos', coverage, '%', `${fmt(observed.length, 0)} de ${fmt(cells, 0)} celdas con registros`, 'research-kpi-warning'],
      ].map(([label, value, unit, detail, tone]) => <article key={label} className={`research-kpi ui-card rounded-xl p-5 ${tone}`}><p className="text-xs text-on-surface-variant">{label}</p><div className="research-kpi-value">{value == null ? 'Sin datos' : unit === 'USD/kg' || unit === '%' ? fmt(value, unit === '%' ? 1 : 2) : compact(value)}<small>{unit}</small></div><p className="text-xs text-on-surface-variant">{detail}</p>{value != null && unit !== '%' && <details className="mt-2 text-xs text-on-surface-variant"><summary className="cursor-pointer">Valor completo</summary>{fmt(value)} {unit}</details>}</article>)}
    </section>
    <p className="text-xs text-on-surface-variant">Periodo: {range} · Cobertura parcial. Los totales corresponden a la selección recuperada.</p>

    <div className="observatory-section-label"><span>01 / Evolución y destinos</span><h2>Las exportaciones, en perspectiva</h2></div>
    <div className="research-analysis-grid">
      <Tabs value={metric} onValueChange={setMetric} asChild><section className="ui-card research-plot rounded-xl p-5 min-w-0" aria-label="Evolución de las exportaciones">
        <div className="flex flex-wrap justify-between items-center gap-3 mb-4">{chartHeading(metric === 'fob' ? 'fob' : 'volume', 'Evolución de la selección', frequency === 'week' ? 'Serie semanal · lunes de semana ISO' : 'Semanas agrupadas por el mes de su lunes')}
          <TabsList aria-label="Indicador del gráfico">{[['value','Precio FOB · USD/kg'], ['fob', 'FOB total · USD'], ['volume', 'Peso neto · kg']].map(([id, label]) => <TabsTrigger key={id} value={id}>{label}</TabsTrigger>)}</TabsList>
        </div>
        <TabsContent value={metric}>
          {observed.length ? <div className="research-chart-large"><ResponsiveContainer width="100%" height="100%"><AreaChart accessibilityLayer key={chartKey + metric} data={chart} margin={{ left: 0, right: 12, top: 8, bottom: 0 }}>
            <defs><linearGradient id="overview-fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={color} stopOpacity={0.24} /><stop offset="100%" stopColor={color} stopOpacity={0.02} /></linearGradient></defs>
            <CartesianGrid stroke="#e2e8f0" vertical={false} strokeDasharray="3 3" /><XAxis dataKey="week" minTickGap={60} tick={axis} /><YAxis domain={paddedDomain(chart.map(r=>r[metric]))} allowDataOverflow width={75} tickFormatter={metric === 'value' ? v => fmt(v,3) : compact} tick={axis} />
            <Tooltip contentStyle={tooltip} formatter={v => [`${fmt(v)} ${metric === 'value' ? 'USD/kg' : metric === 'fob' ? 'USD' : 'kg'}`, metric === 'value' ? 'Valor unitario FOB' : metric === 'fob' ? 'Valor FOB' : 'Peso neto']} />
            <Area type="linear" dataKey={metric} stroke={color} fill="url(#overview-fill)" strokeWidth={2.5} dot={false} connectNulls={false} isAnimationActive={motion} animationDuration={250} />
            <Brush dataKey="week" height={22} stroke="#94a3b8" fill="#f8fafc" tickFormatter={v => v.slice(0, 7)} />
          </AreaChart></ResponsiveContainer></div> : <p role="status" className="research-chart-empty">No hay registros para estos filtros. Amplíe el periodo o cambie el destino.</p>}
        </TabsContent>
        <Info title="Cómo leer el gráfico">El eje se ajusta automáticamente a los valores visibles y puede no comenzar en cero. Arrastre la franja inferior para ampliar un tramo del periodo. Los cortes de línea representan ausencia de registros. La selección de la franja afecta al gráfico; los indicadores resumen el rango de los filtros.</Info>{sourceLink}
      </section></Tabs>

      <section className="ui-card research-plot rounded-xl p-5 min-w-0">
        {chartHeading('markets', 'Principales destinos', 'Hasta 8 destinos por valor FOB · USD')}
        {ranking.length ? <div className="research-chart-large"><ResponsiveContainer width="100%" height="100%"><BarChart accessibilityLayer data={ranking} layout="vertical" margin={{ left: 0, right: 20 }}>
          <CartesianGrid stroke="#e2e8f0" horizontal={false} /><XAxis type="number" tickFormatter={compact} tick={axis} /><YAxis dataKey="destination" type="category" width={105} tickFormatter={v => country(v).replace(/ \(.*\)/, '')} tick={axis} />
          <Tooltip labelFormatter={country} contentStyle={tooltip} formatter={v => [`${fmt(v)} USD`, 'Valor FOB']} /><Bar dataKey="fob" fill={color} radius={[0, 4, 4, 0]} isAnimationActive={motion} animationDuration={250} />
        </BarChart></ResponsiveContainer></div> : <p className="research-chart-empty">No hay destinos con registros para esta selección.</p>}
        <Link className="text-sm text-primary underline underline-offset-4" to={`/dashboard?view=series&product=${product}&destination=${selected||'US'}&start=${start}&end=${end}`}>Comparar dos destinos ↗</Link>{sourceLink}
      </section>
    </div>

    <div className="research-support-grid">
      <section className="ui-card research-plot rounded-xl p-5 min-w-0">
        {chartHeading('unit', 'Valor unitario FOB', 'USD/kg · razón de sumas por periodo')}
        {observed.length ? <div className="research-chart-medium"><ResponsiveContainer width="100%" height="100%"><LineChart accessibilityLayer data={chart}><CartesianGrid stroke="#e2e8f0" vertical={false} /><XAxis dataKey="week" minTickGap={70} tick={axis} /><YAxis domain={paddedDomain(chart.map(r=>r.value))} allowDataOverflow width={70} tickFormatter={v=>fmt(v,3)} tick={axis} /><Tooltip contentStyle={tooltip} formatter={v => [`${fmt(v)} USD/kg`, 'Valor unitario FOB']} /><Line dataKey="value" stroke="#2563eb" strokeWidth={2.5} dot={false} connectNulls={false} isAnimationActive={motion} animationDuration={250} /></LineChart></ResponsiveContainer></div> : <p className="research-chart-empty">Sin observaciones válidas.</p>}
        <Info title="Interpretación del valor unitario">Se calcula dividiendo el valor FOB por el peso neto. Puede cambiar por la composición de destinos y operaciones; no equivale a una cotización de mercado.</Info>{sourceLink}
      </section>
      <section className="ui-card research-plot rounded-xl p-5 min-w-0">
        {chartHeading('coverage', 'Cobertura de datos', 'Celdas producto–destino–semana · selección actual')}
        <p className="text-xs text-on-surface-variant my-3"><span className="text-primary">● Con registros parciales</span> · <span style={{ color: '#64748b' }}>● Sin registros recuperados</span></p>
        {chart.length ? <div className="research-chart-medium"><ResponsiveContainer width="100%" height="100%"><BarChart accessibilityLayer data={chart}><XAxis dataKey="week" minTickGap={70} tick={axis} /><YAxis allowDecimals={false} tick={axis} width={38} /><Tooltip contentStyle={tooltip} /><Bar dataKey="count" name="Con registros parciales" stackId="coverage" fill="#176b4d" isAnimationActive={motion} /><Bar dataKey="unknown" name="Sin registros recuperados" stackId="coverage" fill="#cbd5e1" isAnimationActive={motion} /></BarChart></ResponsiveContainer></div> : <p className="research-chart-empty">Sin celdas en la selección.</p>}
        <p className="text-xs text-on-surface-variant mt-3">{fmt(observed.length, 0)} con registros · {fmt(unknown, 0)} sin registros recuperados. La ausencia no equivale a cero exportaciones.</p>{sourceLink}
      </section>
    </div>

    <section className="observatory-detail-section"><div className="observatory-section-label"><span>02 / Lectura del mercado</span><h2>El contexto detrás de las cifras</h2><p>Compare el cierre semanal y consulte los destinos de la selección.</p></div>
    <PriceSummary rows={rows} start={weekStart} end={weekEnd} selected={selected} product={product} />
    <details className="ui-panel rounded-xl p-5"><summary className="cursor-pointer font-semibold">Explorar todos los destinos disponibles</summary><div className="mt-4"><MarketChoices rows={data.weekly_rows} product={product} start={weekStart} end={weekEnd} selected={selected} onSelect={setDestination}/></div></details></section>
    <section className="research-report-panel ui-card rounded-xl p-5">
      <div><h2 className="research-chart-title text-lg font-semibold"><ResearchIcon name="source" />Reporte de esta selección</h2><p className="text-sm text-on-surface-variant mt-2">Conserve los indicadores, las series y sus referencias en un archivo descargable.</p></div>
      <Button disabled={!observed.length || invalid} onClick={prepareReport}>Generar reporte de esta selección</Button>
      {report && <article className="research-prepared-report space-y-3" aria-live="polite"><h3 className="font-semibold">Reporte preparado · {products[report.product]} · {report.destination ? country(report.destination) : 'Todos los destinos'}</h3><p className="text-sm text-on-surface-variant">{report.start || 'Inicio disponible'} — {report.end || 'Fin disponible'} · {report.frequency === 'week' ? 'Semanal' : 'Semanas agrupadas por mes'}</p><p className="text-sm">Valor FOB: {fmt(report.fob)} USD · Peso neto: {fmt(report.volume)} kg · Valor unitario: {fmt(report.ratio)} USD/kg</p><button onClick={downloadReport} className="ui-input rounded-lg px-4 py-2 text-primary text-sm">Descargar reporte y datos · JSON ↓</button><p className="text-xs text-on-surface-variant">El archivo conserva la selección al generarlo, incluso si cambia los filtros después.</p></article>}
      <details className="research-info text-xs text-on-surface-variant research-report-details"><summary className="cursor-pointer py-2">Alcance del reporte</summary><p>Resumen calculado con los registros del corte local. Incluye el hash de entrada para comprobar su procedencia.</p></details>
    </section>
    <details className="ui-panel rounded-xl p-5"><summary className="cursor-pointer text-primary">Fuentes, disponibilidad y contexto de los datos</summary><div className="mt-4"><SourcePanel data={data} /></div></details>
    <details className="ui-panel rounded-xl p-5 research-info text-sm text-on-surface-variant"><summary className="cursor-pointer font-semibold">Estado de la investigación y evidencia</summary><p className="mt-3">El piloto tiene cobertura parcial y la evaluación final permanece pendiente.</p><div className="grid sm:grid-cols-2 xl:grid-cols-4 gap-4 mt-4">{[
      ['Pronóstico', 'Evaluación final pendiente', 'pronosticos'],
      ['Aporte contextual', 'Elegibilidad temporal no acreditada', 'proceso'],
      ['Variaciones para revisar', 'Caracterización histórica pendiente', 'senales'],
      ['Reportes documentados', 'Pilotos disponibles; evaluación pendiente', 'ia'],
    ].map(([title, detail, view]) => <Link key={title} to={viewUrl(view)} className="research-source-card"><strong className="text-on-surface">{title} ↗</strong><p className="text-xs mt-2">{detail}</p></Link>)}</div></details>
    <details className="research-info text-xs text-on-surface-variant"><summary className="cursor-pointer py-2">Preferencias de visualización</summary><label className="flex items-center gap-2 mt-2"><input type="checkbox" checked={animate} disabled={reduced} onChange={e => setAnimate(e.target.checked)} />Animar gráficos{reduced ? ' · movimiento reducido del sistema' : ''}</label><button disabled={!motion} onClick={() => setReplay(r => r + 1)} className="text-primary underline mt-3">Repetir animación</button></details>
  </div>
}
