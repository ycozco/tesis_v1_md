import { useEffect, useMemo, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import ForecastExplorer from '../components/ForecastExplorer.jsx'
import ResearchProcess from '../components/ResearchProcess.jsx'
import ResearchAI from '../components/ResearchAI.jsx'
import ResearchOverview from '../components/ResearchOverview.jsx'
import SourcePanel from '../components/SourcePanel.jsx'
import { loadResearchSnapshot } from '../lib/loadResearchSnapshot.js'
import { comparisonCsv } from '../lib/comparisonCsv.js'
import DateRangeControl from '../components/DateRangeControl.jsx'
import { comparisonSeries, observedDates, rangePreset, isoMonday } from '../lib/temporalFilters.js'
import { paddedDomain } from '../lib/revisionComparison.js'
import { marketName } from '../components/MarketChoices.jsx'

const products = { palta: 'Palta', uva: 'Uva fresca', arandano: 'Arándano' }
const number = (v, decimals = 2) => v == null ? 'Sin dato' : Number(v).toLocaleString('es-PE', { maximumFractionDigits: decimals })
const titles = { resumen: 'Panorama agroexportador', series: 'Explorar y comparar exportaciones', pronosticos: 'Pronósticos e incertidumbre', senales: 'Variaciones para revisar', reportes: 'Evidencia y reportes', fuentes: 'Datos y fuentes', proceso: 'Trazabilidad del resultado', ia: 'Asistente y respuestas archivadas' }
const descriptions = {
  resumen: 'Explora las exportaciones disponibles y distingue resultados piloto, fuentes y pruebas pendientes.',
  series: 'Compara el valor unitario FOB y el volumen por producto, destino y semana ISO.',
  pronosticos: 'Recorra el calendario, explore predicciones semanales y contraste los modelos con sus resultados observados.',
  senales: 'Observaciones seleccionadas por detectores con un presupuesto común. Requieren interpretación.',
  reportes: 'Estado de la evaluación documental y comprobación de afirmaciones.',
  fuentes: 'Procedencia, recuperación y límites de los datos utilizados.',
  proceso: 'Siga las etapas, compruebe archivos y consulte sus pendientes.',
  ia: 'Respuestas de Codex archivadas, borradores y procedencia de los proveedores.',
}
function Card({ label, value, detail }) {
  return <article className="research-kpi ui-card rounded-xl p-5"><p className="text-xs uppercase tracking-wider text-on-surface-variant">{label}</p><p className="font-headline-lg text-3xl text-primary mt-3 mb-2 break-words">{value}</p><p className="text-xs text-on-surface-variant leading-relaxed">{detail}</p></article>
}
function Empty({ children }) { return <div role="status" className="ui-panel rounded-xl p-8 text-on-surface-variant text-sm">{children}</div> }
function Table({ headings, children }) {
  return <div className="ui-panel rounded-xl overflow-x-auto" tabIndex={0} role="region" aria-label={headings.join(", ")}><table className="w-full text-sm text-left"><thead className="text-xs text-on-surface-variant border-b border-white/10"><tr>{headings.map(h => <th key={h} scope="col" className="p-4 font-medium whitespace-nowrap">{h}</th>)}</tr></thead><tbody className="divide-y divide-white/5">{children}</tbody></table></div>
}

export default function ResearchDashboard() {
  const [params, setParams] = useSearchParams()
  const view = titles[params.get('view')] ? params.get('view') : 'resumen'
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [attempt, setAttempt] = useState(0)
  const product = products[params.get('product')] ? params.get('product') : 'palta'
  const setProduct = value => setParams(current => { const next = new URLSearchParams(current); next.set('product', value); return next }, { replace: true })
  const destination = params.get('destination') ?? 'US'
  const setDestination = value => setParams(current => { const next = new URLSearchParams(current); next.set('destination', value); return next }, { replace: true })
  const compare = params.get('compare') ?? 'NL'
  const setCompare = value => setParams(current => { const next = new URLSearchParams(current); next.set('compare', value); return next }, { replace: true })
  const target = params.get('target') ?? 'unit_fob'
  const setTarget = value => setParams(current => { const next = new URLSearchParams(current); next.set('target', value); return next }, { replace: true })
  const availableDates = useMemo(() => data ? observedDates(data.weekly_rows, product, destination, target) : [], [data, product, destination, target])
  const defaults = rangePreset(availableDates, 12)
  const start = params.get('start') ?? defaults.start
  const end = params.get('end') ?? defaults.end
  const applyRange = range => setParams(current => { const next = new URLSearchParams(current); next.set('start', range.start); next.set('end', range.end); return next }, { replace: true })
  useEffect(() => {
    const abort = new AbortController()
    setError('')
    loadResearchSnapshot(`${import.meta.env.BASE_URL}research/snapshot.json`, abort.signal)
      .then(snapshot => { if (!abort.signal.aborted) setData(snapshot) })
      .catch(e => { if (!abort.signal.aborted) setError(e.message) })
    return () => abort.abort()
  }, [attempt])
  const markets = useMemo(() => data ? [...new Set(data.weekly_rows.filter(r => r[0] === product).map(r => r[1]))].sort() : [], [data, product])
  const selectedDestination = markets.includes(destination) ? destination : markets[0]
  const selectedCompare = markets.includes(compare) && compare !== selectedDestination ? compare : ''
  const series = useMemo(() => data ? comparisonSeries(data.weekly_rows, { product, destination: selectedDestination, compare: selectedCompare, target, start, end }) : [], [data, product, selectedDestination, selectedCompare, target, start, end])
  if (error) return <Empty>No se pudo cargar el corte documentado.<p className="mt-2">{error}</p><a className="inline-block mt-3 text-primary underline" href={`${import.meta.env.BASE_URL}research/snapshot.json`} target="_blank" rel="noreferrer">Comprobar archivo de datos ↗</a><button className="block mt-4 text-primary underline" onClick={() => setAttempt(a => a + 1)}>Reintentar</button></Empty>
  if (!data) return <Empty>Cargando el corte documentado…</Empty>
  const summary = data.manifest.views.conservadora
  const observed = series.filter(r => r.main != null).length
  const metrics = data.paired_metrics.filter(r => r.target === target)
  const signals = data.signals.filter(r => r.producto === product && r.destino === selectedDestination && r.target === target && r.emission.slice(0, 10) >= isoMonday(start) && r.emission.slice(0, 10) <= isoMonday(end))
  const unit = target === 'unit_fob' ? 'USD/kg' : 'kg'
  function exportComparison() {
    const csv = comparisonCsv(series, product, selectedDestination, selectedCompare, unit, summary.input_sha256)
    const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }))
    const link = document.createElement('a'); link.href = url; link.download = `comparacion-${product}-${selectedDestination}-${target}.csv`
    link.click(); URL.revokeObjectURL(url)
  }
  return <div key={view} className={`observatory-page observatory-view-${view} space-y-6 research-enter`}>
    <header className="research-page-heading"><p className="text-xs text-primary uppercase tracking-widest mb-2">{view === 'resumen' ? 'Observatorio de exportaciones peruanas' : 'AgroScope / Análisis e investigación'}</p>
      <div className="flex flex-wrap justify-between gap-3 items-start"><h1 className="font-headline-lg text-3xl md:text-4xl">{titles[view]}</h1><span className="research-cut">Corte local · {data.generated_on}</span></div>
      {<p className="text-on-surface-variant mt-3 text-sm leading-relaxed">{descriptions[view]}</p>}</header>
    <div role="status" className="research-notice text-sm"><strong>Cobertura parcial</strong><span>Las semanas sin registros permanecen desconocidas.</span><Link to="/dashboard?view=fuentes">Consultar alcance ↗</Link></div>
    {view === 'resumen' && <ResearchOverview data={data} />}
    {view === 'fuentes' && <SourcePanel data={data} />}
    {view === 'proceso' && <ResearchProcess data={data} />}
    {view === 'ia' && <ResearchAI data={data} />}
    {['series', 'senales'].includes(view) && <section aria-label="Filtros de series" className="ui-card rounded-xl p-4 grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
      <label className="text-xs text-on-surface-variant">Producto<select className="ui-input rounded-lg p-2.5 mt-2 w-full text-on-surface" value={product} onChange={e => setProduct(e.target.value)}>{Object.entries(products).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select></label>
      <label className="text-xs text-on-surface-variant">País de destino (código de la fuente)<select className="ui-input rounded-lg p-2.5 mt-2 w-full text-on-surface" value={selectedDestination || ''} onChange={e => setDestination(e.target.value)}>{markets.map(m => <option key={m} value={m}>{marketName(m)}</option>)}</select></label>
      {view === 'series' && <label className="text-xs text-on-surface-variant">Comparar con<select className="ui-input rounded-lg p-2.5 mt-2 w-full text-on-surface" value={selectedCompare} onChange={e => setCompare(e.target.value)}><option value="">Sin comparación</option>{markets.filter(m => m !== selectedDestination).map(m => <option key={m} value={m}>{marketName(m)}</option>)}</select></label>}
      <label className="text-xs text-on-surface-variant">Variable<select className="ui-input rounded-lg p-2.5 mt-2 w-full text-on-surface" value={target} onChange={e => setTarget(e.target.value)}><option value="unit_fob">Valor unitario FOB · USD/kg</option><option value="volume_kg">Volumen · kg</option></select></label>
      <div className="sm:col-span-2 xl:col-span-3"><DateRangeControl start={start} end={end} dates={availableDates} onApply={applyRange} label="Rango de series" /></div>
    </section>}
    {(!start || !end || start > end) && ['series', 'senales'].includes(view) && <p role="alert" className="text-error text-sm">Ingrese ambas fechas; la inicial debe ser anterior o igual a la final.</p>}
    {view === 'series' && <>
      <section className="grid sm:grid-cols-3 gap-4"><Card label="Serie seleccionada" value={`${products[product]} · ${selectedDestination}`} detail="Agregación por destino y semana de embarque" /><Card label="Semanas con registros" value={number(observed, 0)} detail="En el rango seleccionado, destino principal" /><Card label="Semanas desconocidas" value={number(series.length - observed, 0)} detail="En el rango solicitado; no equivalen a cero" /></section>
      {series.some(r => r.main != null || r.comparison != null) ? <section className="ui-card rounded-xl p-4 md:p-6" aria-label={`Serie semanal en ${unit}`}>
        <div className="flex flex-wrap justify-between gap-3 mb-5"><h2 className="font-headline-md text-lg">{target === 'unit_fob' ? 'Valor unitario FOB observado' : 'Volumen observado'}</h2><span className="text-xs text-on-surface-variant">{unit} · lunes de semana ISO</span></div>
        <div className="h-80 w-full"><ResponsiveContainer width="100%" height="100%"><LineChart accessibilityLayer data={series} margin={{ left: 8, right: 16, top: 8, bottom: 8 }}>
          <CartesianGrid stroke="#e2e8f0" strokeDasharray="3 3" vertical={false} /><XAxis dataKey="week" tick={{ fill: '#64748b', fontSize: 11 }} minTickGap={45} /><YAxis domain={paddedDomain(series.flatMap(r => [r.main, r.comparison]))} allowDataOverflow width={90} tick={{ fill: '#64748b', fontSize: 11 }} tickFormatter={v => number(v, target === 'unit_fob' ? 3 : 0)} />
          <Tooltip contentStyle={{ background: '#ffffff', color: '#17202a', border: '1px solid #dbe3ea', borderRadius: 8 }} formatter={(v, name) => [`${number(v)} ${unit}`, name]} />
          <Line type="linear" dataKey="main" name={selectedDestination} stroke="#176b4d" strokeWidth={2.5} dot={false} connectNulls={false} isAnimationActive={false} />
          {selectedCompare && <Line type="linear" dataKey="comparison" name={selectedCompare} stroke="#2563eb" strokeWidth={2.5} dot={false} connectNulls={false} isAnimationActive={false} />}
        </LineChart></ResponsiveContainer></div>
        <p className="text-xs text-on-surface-variant mt-4">{selectedDestination}: verde{selectedCompare ? ` · ${selectedCompare}: azul` : ''}. Los cortes de línea representan semanas desconocidas. FOB/kg = suma FOB / suma peso neto.</p>
      </section> : <Empty>No hay semanas recuperadas para estos filtros.</Empty>}
      <Table headings={['Semana ISO', `${selectedDestination} · ${unit}`, ...(selectedCompare ? [`${selectedCompare} · ${unit}`] : [])]}>{series.slice(-12).reverse().map(row => <tr key={row.week}><td className="p-4">{row.week}</td><td className="p-4 font-mono">{number(row.main)}</td>{selectedCompare && <td className="p-4 font-mono">{number(row.comparison)}</td>}</tr>)}</Table>
      <p className="text-xs text-on-surface-variant">Tabla: hasta las 12 semanas más recientes del rango seleccionado. Códigos de destino conservados tal como aparecen en la fuente.</p>
      <button onClick={exportComparison} disabled={!series.length} className="ui-input rounded-lg px-4 py-3 text-sm text-primary disabled:opacity-40">Exportar comparación completa CSV</button>
    </>}
    {view === 'pronosticos' && <>
      <ForecastExplorer data={data} />
      <details className="ui-panel rounded-xl p-5 space-y-4"><summary className="cursor-pointer text-primary">Métricas globales del piloto y estado del protocolo</summary>
      <section className="grid sm:grid-cols-3 gap-4"><Card label="Horizonte" value="1 semana" detail="Reajuste por fecha común de emisión" /><Card label="Intervalos 90 / 95 %" value="No evaluables" detail="Faltan 40 errores previos por serie para calibrar" /><Card label="Prueba final" value="No ejecutada" detail="No se ha ejecutado el test final; elegibilidad pendiente" /></section>
      <label className="ui-panel rounded-xl p-4 flex flex-wrap items-center gap-3 text-sm">Objetivo del contraste<select value={target} onChange={e => setTarget(e.target.value)} className="ui-input rounded-lg p-3 w-full sm:w-auto"><option value="unit_fob">Valor unitario FOB · USD/kg</option><option value="volume_kg">Volumen · kg</option></select></label>
      <p className="text-sm text-on-surface-variant">MAE macro por serie en desarrollo. Cada fila compara el modelo y la referencia sobre los mismos casos disponibles. Vista conservadora, L=0; una configuración piloto por biblioteca.</p>
      <Table headings={['Modelo', 'Referencia', 'Casos emparejados', `MAE modelo · ${unit}`, `MAE referencia · ${unit}`]}>{metrics.map(r => <tr key={`${r.model}-${r.reference}`}><td className="p-4">{r.model === 'xgb' ? 'XGBoost' : 'LightGBM'}</td><td className="p-4">{{ naive: 'Último valor', mean4: 'Media de 4 semanas', seasonal52: 'Estacional 52' }[r.reference]}</td><td className="p-4">{number(r.n_paired, 0)}</td><td className="p-4 font-mono">{number(r.model_macro_mae)}</td><td className="p-4 font-mono">{number(r.reference_macro_mae)}</td></tr>)}</Table>
      <Empty>Estos resultados prueban el funcionamiento del flujo. La selección y evaluación final requieren cobertura, grilla y calendario definitivos. SHAP explica el pronóstico supervisado; no demuestra causalidad.</Empty>
      </details>
    </>}
    {view === 'senales' && <>
      <p className="text-sm text-on-surface-variant leading-relaxed">Selecciones del ensemble de rangos de IF, LOF y ECOD en desarrollo. Comparten K=ceil(0,05 × N) por fecha y objetivo. El residuo actual se conoce después del cierre de su semana; no es una alerta en tiempo real ni prueba de irregularidad.</p>
      {signals.length ? <Table headings={['Semana objetivo', 'Producto / destino', 'Residuo normalizado', 'Población común', 'K']}>{signals.map((r, i) => <tr key={`${r.emission}-${i}`}><td className="p-4">{r.emission.slice(0, 10)}</td><td className="p-4">{products[r.producto]} / {r.destino}</td><td className="p-4 font-mono">{number(r.z)}</td><td className="p-4">{r.common_candidates}</td><td className="p-4">{r.K}</td></tr>)}</Table> : <Empty>No hay selecciones del piloto para estos filtros. Esto no demuestra ausencia de anomalías: también puede faltar historia suficiente.</Empty>}
      <p className="text-xs text-on-surface-variant">Pendiente: referencia estacional, persistencia e informe de casos indeterminados. Sin etiquetas reales no se presentan precisión ni F1.</p>
    </>}
    {view === 'reportes' && <>
      <section className="grid sm:grid-cols-3 gap-4"><Card label="Diseño controlado" value="30 casos" detail="Diez esquemas artificiales por producto; revisión humana de claves pendiente" /><Card label="Salidas finales previstas" value="180" detail="30 casos × dos configuraciones × tres repeticiones" /><Card label="Evaluación final" value="Pendiente" detail="El archivo Codex es un piloto expuesto y se consulta por separado" /></section>
      <section className="ui-card rounded-xl p-6 space-y-4"><h2 className="font-headline-md text-xl">De la afirmación a su evidencia</h2><p className="text-sm text-on-surface-variant">Cada afirmación debe enlazar hecho, documento, versión, semana, producto, destino y unidad. La tolerancia es media unidad del último decimal más 10⁻⁹. Una cifra coincidente no acredita su significado.</p><ol className="grid sm:grid-cols-3 gap-4 text-sm list-none"><li className="ui-panel rounded-lg p-4">1. Fijar las entradas y revisar las claves.</li><li className="ui-panel rounded-lg p-4">2. Congelar generador, corpus y recuperación.</li><li className="ui-panel rounded-lg p-4">3. Generar, contrastar y revisar las salidas.</li></ol><p className="text-sm text-on-surface-variant">La recuperación documental real, persistencia pgvector y evaluación factual continúan pendientes. Los recorridos técnicos y respuestas archivadas no sustituyen H4.</p><div className="flex flex-wrap gap-3"><Link className="ui-input research-button rounded-lg px-4 py-3 text-primary text-sm" to="/dashboard?view=ia">Consultar piloto Codex</Link><a className="ui-input research-button rounded-lg px-4 py-3 text-primary text-sm" href="https://docs.google.com/document/d/13cJUk1_AMrI-jsZj0s6a5XuTmE7wXZLFL-SNlPGxt8g/edit" target="_blank" rel="noreferrer">Tesis · §3.9.5.1 ↗</a></div></section>
    </>}
    {view === 'fuentes' && <>
      <section className="grid sm:grid-cols-3 gap-4"><Card label="Registros conciliados" value={number(summary.rows, 0)} detail="Vista conservadora; registros aduaneros, no series temporales" /><Card label="Combinaciones" value={summary.series} detail="Producto–destino en el panel recuperado" /><Card label="Celdas desconocidas" value={number(summary.unknown_cells, 0)} detail="No imputadas como exportaciones cero" /></section>
      <Table headings={['Fuente', 'Contenido del corte local', 'Uso y límite']}>
        <tr><td className="p-4">SUNAT</td><td className="p-4">22 paquetes en el panel</td><td className="p-4">Cobertura parcial; publicación no reconstruida</td></tr>
        <tr><td className="p-4">BCRP</td><td className="p-4">{data.bcrp.total_months} meses</td><td className="p-4">Respaldos hasta junio 2026; disponibilidad histórica sin validar</td></tr>
        <tr><td className="p-4">SISAP</td><td className="p-4">{number(data.sisap.numeric_prices, 0)} precios</td><td className="p-4">Palta y uva; unidades específicas por verificar</td></tr>
        <tr><td className="p-4">NASA POWER</td><td className="p-4">3.217 días · cuatro parámetros</td><td className="p-4">Punto de Arequipa; origen productivo sin justificar</td></tr>
      </Table>
      <section className="ui-card rounded-xl p-6"><h2 className="font-headline-md text-xl mb-3">Nueva recuperación histórica</h2><p className="text-sm text-on-surface-variant leading-relaxed">Los dos paquetes históricos adicionales ya se conciliaron en una versión ampliada: 24 paquetes y 101.546 registros. Los gráficos de esta vista mantienen el piloto anterior de 22 paquetes. Consulte Trazabilidad para verificar los siete artefactos actuales; cobertura y publicación histórica siguen pendientes.</p></section>
      <section className="ui-panel rounded-xl p-6"><h2 className="font-headline-md text-lg mb-3">Consultar procedencia</h2><ul className="flex flex-wrap gap-4 text-sm text-primary">{data.sources.map(s => <li key={s.name}><a href={s.url} target="_blank" rel="noreferrer" className="underline underline-offset-4">{s.name} ↗</a></li>)}</ul><a href={`${import.meta.env.BASE_URL}research/snapshot.json`} download="corte-investigacion.json" className="inline-block ui-input rounded-lg px-4 py-2 mt-5 text-sm">Descargar corte y referencias</a></section>
    </>}
  </div>
}
