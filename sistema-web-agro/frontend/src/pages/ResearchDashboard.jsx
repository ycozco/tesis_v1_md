import React, { useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import ResearchProcess from '../components/ResearchProcess.jsx'
import ResearchAI from '../components/ResearchAI.jsx'
import useReducedMotion from '../lib/useReducedMotion.js'
import { comparisonCsv } from '../lib/comparisonCsv.js'

const products = { palta: 'Palta', uva: 'Uva fresca', arandano: 'Arándano' }
const number = (v, decimals = 2) => v == null ? 'Sin dato' : Number(v).toLocaleString('es-PE', { maximumFractionDigits: decimals })
const titles = { series: 'Series y comparación', pronosticos: 'Pronóstico semanal', senales: 'Señales exploratorias', reportes: 'Reportes y evidencia', fuentes: 'Fuentes y cobertura', proceso: 'Proceso y auditoría', ia: 'IA y reportes' }
const descriptions = {
  series: 'Compara el valor unitario FOB y el volumen por producto, destino y semana ISO.',
  pronosticos: 'Contraste retrospectivo de modelos y referencias simples, solo en desarrollo.',
  senales: 'Observaciones seleccionadas por detectores con un presupuesto común. Requieren interpretación.',
  reportes: 'Estado de la evaluación documental y comprobación de afirmaciones.',
  fuentes: 'Procedencia, recuperación y límites de los datos utilizados.',
  proceso: 'Siga las etapas, compruebe archivos y consulte sus pendientes.',
  ia: 'Respuestas de Codex archivadas, borradores y procedencia de los proveedores.',
}
function Card({ label, value, detail }) {
  return <article className="glass-card rounded-xl p-5"><p className="text-xs uppercase tracking-wider text-on-surface-variant">{label}</p><p className="font-headline-lg text-3xl text-primary mt-3 mb-2 break-words">{value}</p><p className="text-xs text-on-surface-variant leading-relaxed">{detail}</p></article>
}
function Empty({ children }) { return <div role="status" className="glass-panel rounded-xl p-8 text-on-surface-variant text-sm">{children}</div> }
function Table({ headings, children }) {
  return <div className="glass-panel rounded-xl overflow-x-auto"><table className="w-full text-sm text-left"><thead className="text-xs text-on-surface-variant border-b border-white/10"><tr>{headings.map(h => <th key={h} scope="col" className="p-4 font-medium whitespace-nowrap">{h}</th>)}</tr></thead><tbody className="divide-y divide-white/5">{children}</tbody></table></div>
}

export default function ResearchDashboard() {
  const reducedMotion = useReducedMotion()
  const [params] = useSearchParams()
  const view = titles[params.get('view')] ? params.get('view') : 'series'
  const [data, setData] = useState(null)
  const [error, setError] = useState(false)
  const [attempt, setAttempt] = useState(0)
  const [product, setProduct] = useState('palta')
  const [destination, setDestination] = useState('US')
  const [compare, setCompare] = useState('NL')
  const [target, setTarget] = useState('unit_fob')
  const [start, setStart] = useState('2025-10-20')
  const [end, setEnd] = useState('2026-10-19')
  useEffect(() => {
    const abort = new AbortController()
    setError(false)
    fetch(`${import.meta.env.BASE_URL}research/snapshot.json`, { signal: abort.signal })
      .then(r => { if (!r.ok) throw new Error('unavailable'); return r.json() })
      .then(snapshot => { if (snapshot.schema_version !== 1 || !Array.isArray(snapshot.weekly_rows)) throw new Error('schema'); setData(snapshot) })
      .catch(e => { if (e.name !== 'AbortError') setError(true) })
    return () => abort.abort()
  }, [attempt])
  const markets = useMemo(() => data ? [...new Set(data.weekly_rows.filter(r => r[0] === product).map(r => r[1]))].sort() : [], [data, product])
  const selectedDestination = markets.includes(destination) ? destination : markets[0]
  const selectedCompare = markets.includes(compare) && compare !== selectedDestination ? compare : ''
  const series = useMemo(() => {
    if (!data || !start || !end || start > end) return []
    const weeks = new Map()
    const monday = new Date(`${start}T00:00:00Z`)
    const last = new Date(`${end}T00:00:00Z`)
    monday.setUTCDate(monday.getUTCDate() + (8 - monday.getUTCDay()) % 7)
    for (let date = monday; date <= last; date.setUTCDate(date.getUTCDate() + 7)) {
      const week = date.toISOString().slice(0, 10)
      weeks.set(week, { week, main: null, comparison: null })
    }
    for (const row of data.weekly_rows) {
      const [p, d, week, unit, volume] = row
      if (p !== product || week < start || week > end || ![selectedDestination, selectedCompare].includes(d)) continue
      if (!weeks.has(week)) weeks.set(week, { week, main: null, comparison: null })
      weeks.get(week)[d === selectedDestination ? 'main' : 'comparison'] = target === 'unit_fob' ? unit : volume
    }
    return [...weeks.values()].sort((a, b) => a.week.localeCompare(b.week))
  }, [data, product, selectedDestination, selectedCompare, target, start, end])
  if (error) return <Empty>No se pudo cargar el corte documentado. No se muestran cifras de reemplazo.<button className="block mt-4 text-primary underline" onClick={() => setAttempt(a => a + 1)}>Reintentar</button></Empty>
  if (!data) return <Empty>Cargando el corte documentado…</Empty>
  const summary = data.manifest.views.conservadora
  const observed = series.filter(r => r.main != null).length
  const metrics = data.paired_metrics.filter(r => r.target === target)
  const signals = data.signals.filter(r => r.producto === product && r.destino === selectedDestination && r.target === target && r.emission.slice(0, 10) >= start && r.emission.slice(0, 10) <= end)
  const unit = target === 'unit_fob' ? 'USD/kg' : 'kg'
  function exportComparison() {
    const csv = comparisonCsv(series, product, selectedDestination, selectedCompare, unit, summary.input_sha256)
    const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }))
    const link = document.createElement('a'); link.href = url; link.download = `comparacion-${product}-${selectedDestination}-${target}.csv`
    link.click(); URL.revokeObjectURL(url)
  }
  return <div className="space-y-6 research-enter">
    <header><p className="text-xs text-primary uppercase tracking-widest mb-2">Sistema de información y pronóstico</p>
      <div className="flex flex-wrap justify-between gap-3 items-start"><h1 className="font-headline-lg text-3xl md:text-4xl">{titles[view]}</h1><span className="glass-panel rounded-full px-3 py-2 text-xs text-primary border border-primary/20">Corte · 01 nov 2026</span></div>
      <p className="text-on-surface-variant mt-3 text-sm leading-relaxed">{descriptions[view]}</p></header>
    <div role="status" className="glass-panel rounded-xl px-4 py-3 text-sm text-on-surface-variant border-l-2 border-primary"><strong className="text-on-surface">Piloto de desarrollo · cobertura parcial.</strong> Las semanas sin registros permanecen desconocidas. La prueba final no se ha ejecutado.</div>
    {view === 'proceso' && <ResearchProcess data={data} />}
    {view === 'ia' && <ResearchAI />}
    {['series', 'senales'].includes(view) && <section aria-label="Filtros de series" className="glass-card rounded-xl p-4 grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
      <label className="text-xs text-on-surface-variant">Producto<select className="glass-input rounded-lg p-2.5 mt-2 w-full text-on-surface" value={product} onChange={e => setProduct(e.target.value)}>{Object.entries(products).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select></label>
      <label className="text-xs text-on-surface-variant">Destino (código de origen)<select className="glass-input rounded-lg p-2.5 mt-2 w-full text-on-surface" value={selectedDestination || ''} onChange={e => setDestination(e.target.value)}>{markets.map(m => <option key={m}>{m}</option>)}</select></label>
      {view === 'series' && <label className="text-xs text-on-surface-variant">Comparar con<select className="glass-input rounded-lg p-2.5 mt-2 w-full text-on-surface" value={selectedCompare} onChange={e => setCompare(e.target.value)}><option value="">Sin comparación</option>{markets.filter(m => m !== selectedDestination).map(m => <option key={m}>{m}</option>)}</select></label>}
      <label className="text-xs text-on-surface-variant">Variable<select className="glass-input rounded-lg p-2.5 mt-2 w-full text-on-surface" value={target} onChange={e => setTarget(e.target.value)}><option value="unit_fob">Valor unitario FOB · USD/kg</option><option value="volume_kg">Volumen · kg</option></select></label>
      <label className="text-xs text-on-surface-variant">Desde<input className="glass-input rounded-lg p-2.5 mt-2 w-full text-on-surface" type="date" value={start} onInput={e => setStart(e.currentTarget.value)} onChange={e => setStart(e.target.value)} /></label>
      <label className="text-xs text-on-surface-variant">Hasta<input className="glass-input rounded-lg p-2.5 mt-2 w-full text-on-surface" type="date" value={end} onInput={e => setEnd(e.currentTarget.value)} onChange={e => setEnd(e.target.value)} /></label>
    </section>}
    {(!start || !end || start > end) && ['series', 'senales'].includes(view) && <p role="alert" className="text-error text-sm">Ingrese ambas fechas; la inicial debe ser anterior o igual a la final.</p>}
    {view === 'series' && <>
      <section className="grid sm:grid-cols-3 gap-4"><Card label="Serie seleccionada" value={`${products[product]} · ${selectedDestination}`} detail="Agregación por destino y semana de embarque" /><Card label="Semanas con registros" value={number(observed, 0)} detail="En el rango seleccionado, destino principal" /><Card label="Semanas desconocidas" value={number(series.length - observed, 0)} detail="En el rango solicitado; no equivalen a cero" /></section>
      {series.some(r => r.main != null || r.comparison != null) ? <section className="glass-card rounded-xl p-4 md:p-6" aria-label={`Serie semanal en ${unit}`}>
        <div className="flex flex-wrap justify-between gap-3 mb-5"><h2 className="font-headline-md text-lg">{target === 'unit_fob' ? 'Valor unitario FOB observado' : 'Volumen observado'}</h2><span className="text-xs text-on-surface-variant">{unit} · lunes de semana ISO</span></div>
        <div className="h-80 w-full"><ResponsiveContainer width="100%" height="100%"><LineChart data={series} margin={{ left: 8, right: 16, top: 8, bottom: 8 }}>
          <CartesianGrid stroke="#3f4a3f" strokeDasharray="3 3" vertical={false} /><XAxis dataKey="week" tick={{ fill: '#becabc', fontSize: 11 }} minTickGap={45} /><YAxis width={78} tick={{ fill: '#becabc', fontSize: 11 }} tickFormatter={v => number(v, 0)} />
          <Tooltip contentStyle={{ background: '#171d17', border: '1px solid #3f4a3f', borderRadius: 8 }} formatter={(v, name) => [`${number(v)} ${unit}`, name]} />
          <Line type="linear" dataKey="main" name={selectedDestination} stroke="#76db8f" strokeWidth={2} dot={false} connectNulls={false} isAnimationActive={!reducedMotion} animationDuration={180} />
          {selectedCompare && <Line type="linear" dataKey="comparison" name={selectedCompare} stroke="#89ceff" strokeWidth={2} dot={false} connectNulls={false} isAnimationActive={!reducedMotion} animationDuration={180} />}
        </LineChart></ResponsiveContainer></div>
        <p className="text-xs text-on-surface-variant mt-4">{selectedDestination}: verde{selectedCompare ? ` · ${selectedCompare}: azul` : ''}. Los cortes de línea representan semanas desconocidas. FOB/kg = suma FOB / suma peso neto.</p>
      </section> : <Empty>No hay semanas recuperadas para estos filtros.</Empty>}
      <Table headings={['Semana ISO', `${selectedDestination} · ${unit}`, ...(selectedCompare ? [`${selectedCompare} · ${unit}`] : [])]}>{series.slice(-12).reverse().map(row => <tr key={row.week}><td className="p-4">{row.week}</td><td className="p-4 font-mono">{number(row.main)}</td>{selectedCompare && <td className="p-4 font-mono">{number(row.comparison)}</td>}</tr>)}</Table>
      <p className="text-xs text-on-surface-variant">Tabla: hasta las 12 semanas más recientes del rango seleccionado. Códigos de destino conservados tal como aparecen en la fuente.</p>
      <button onClick={exportComparison} disabled={!series.length} className="glass-input rounded-lg px-4 py-3 text-sm text-primary disabled:opacity-40">Exportar comparación completa CSV</button>
    </>}
    {view === 'pronosticos' && <>
      <section className="grid sm:grid-cols-3 gap-4"><Card label="Horizonte" value="1 semana" detail="Reajuste por fecha común de emisión" /><Card label="Intervalos 90 / 95 %" value="No evaluables" detail="Faltan 40 errores previos por serie para calibrar" /><Card label="Prueba final" value="Reservada" detail="Sin predicciones ni métricas del test" /></section>
      <label className="block text-sm">Objetivo del contraste<select value={target} onChange={e => setTarget(e.target.value)} className="glass-input rounded-lg p-3 ml-3"><option value="unit_fob">Valor unitario FOB · USD/kg</option><option value="volume_kg">Volumen · kg</option></select></label>
      <p className="text-sm text-on-surface-variant">MAE macro por serie en desarrollo. Cada fila compara el modelo y la referencia sobre los mismos casos disponibles. Vista conservadora, L=0; una configuración piloto por biblioteca.</p>
      <Table headings={['Modelo', 'Referencia', 'Casos emparejados', `MAE modelo · ${unit}`, `MAE referencia · ${unit}`]}>{metrics.map(r => <tr key={`${r.model}-${r.reference}`}><td className="p-4">{r.model === 'xgb' ? 'XGBoost' : 'LightGBM'}</td><td className="p-4">{{ naive: 'Último valor', mean4: 'Media de 4 semanas', seasonal52: 'Estacional 52' }[r.reference]}</td><td className="p-4">{number(r.n_paired, 0)}</td><td className="p-4 font-mono">{number(r.model_macro_mae)}</td><td className="p-4 font-mono">{number(r.reference_macro_mae)}</td></tr>)}</Table>
      <Empty>Estos resultados prueban el funcionamiento del flujo. La selección y evaluación final requieren cobertura, grilla y calendario definitivos. SHAP explica el pronóstico supervisado; no demuestra causalidad.</Empty>
    </>}
    {view === 'senales' && <>
      <p className="text-sm text-on-surface-variant leading-relaxed">Selecciones del ensemble de rangos de IF, LOF y ECOD en desarrollo. Comparten K=ceil(0,05 × N) por fecha y objetivo. El residuo actual se conoce después del cierre de su semana; no es una alerta en tiempo real ni prueba de irregularidad.</p>
      {signals.length ? <Table headings={['Semana objetivo', 'Producto / destino', 'Residuo normalizado', 'Población común', 'K']}>{signals.map((r, i) => <tr key={`${r.emission}-${i}`}><td className="p-4">{r.emission.slice(0, 10)}</td><td className="p-4">{products[r.producto]} / {r.destino}</td><td className="p-4 font-mono">{number(r.z)}</td><td className="p-4">{r.common_candidates}</td><td className="p-4">{r.K}</td></tr>)}</Table> : <Empty>No hay selecciones del piloto para estos filtros. Esto no demuestra ausencia de anomalías: también puede faltar historia suficiente.</Empty>}
      <p className="text-xs text-on-surface-variant">Pendiente: referencia estacional, persistencia e informe de casos indeterminados. Sin etiquetas reales no se presentan precisión ni F1.</p>
    </>}
    {view === 'reportes' && <>
      <section className="grid sm:grid-cols-3 gap-4"><Card label="Casos preparados" value={data.h4.h4_cases_prepared} detail="Diez por producto, con hechos de agregados reales" /><Card label="Ejecuciones planificadas" value={data.h4.h4_slots_prepared} detail="Dos configuraciones × tres repeticiones × 30 casos" /><Card label="Reportes generados" value={data.h4.h4_outputs_generated} detail="La evaluación H4 todavía no se ha ejecutado" /></section>
      <section className="glass-card rounded-xl p-6 space-y-4"><h2 className="font-headline-md text-xl">Qué debe respaldar cada afirmación</h2><p className="text-sm text-on-surface-variant">Hecho identificado, fuente, semana, producto, destino y unidad. Para dos decimales se admite una diferencia absoluta máxima de 0,005; encontrar una cifra en un texto no acredita su significado.</p><p className="text-sm text-on-surface-variant">Recuperación léxica BM25 probada con documentos locales. Recuperación densa, persistencia pgvector, generación emparejada y evaluación factual a ciegas pendientes.</p></section>
    </>}
    {view === 'fuentes' && <>
      <section className="grid sm:grid-cols-3 gap-4"><Card label="Registros conciliados" value={number(summary.rows, 0)} detail="Vista conservadora; registros aduaneros, no series temporales" /><Card label="Combinaciones" value={summary.series} detail="Producto–destino en el panel recuperado" /><Card label="Celdas desconocidas" value={number(summary.unknown_cells, 0)} detail="No imputadas como exportaciones cero" /></section>
      <Table headings={['Fuente', 'Contenido recuperado', 'Uso y límite']}>
        <tr><td className="p-4">SUNAT</td><td className="p-4">22 paquetes en el panel</td><td className="p-4">Cobertura parcial; publicación no reconstruida</td></tr>
        <tr><td className="p-4">BCRP</td><td className="p-4">{data.bcrp.total_months} meses</td><td className="p-4">Respaldos hasta junio 2026; disponibilidad histórica sin validar</td></tr>
        <tr><td className="p-4">SISAP</td><td className="p-4">{number(data.sisap.numeric_prices, 0)} precios</td><td className="p-4">Palta y uva; unidades específicas por verificar</td></tr>
        <tr><td className="p-4">NASA POWER</td><td className="p-4">3.217 días · cuatro parámetros</td><td className="p-4">Punto de Arequipa; origen productivo sin justificar</td></tr>
      </Table>
      <section className="glass-card rounded-xl p-6"><h2 className="font-headline-md text-xl mb-3">Nueva recuperación histórica</h2><p className="text-sm text-on-surface-variant leading-relaxed">Dos paquetes adicionales, de 2022 y 2023: {number(data.pending_search.candidate_rows, 0)} filas candidatas. Aún no se integran en series ni métricas; requieren conciliación y auditoría de cobertura. Cuatro enlaces exploratorios anteriores devolvieron 404.</p></section>
      <section className="glass-panel rounded-xl p-6"><h2 className="font-headline-md text-lg mb-3">Consultar procedencia</h2><ul className="flex flex-wrap gap-4 text-sm text-primary">{data.sources.map(s => <li key={s.name}><a href={s.url} target="_blank" rel="noreferrer" className="underline underline-offset-4">{s.name} ↗</a></li>)}</ul><a href={`${import.meta.env.BASE_URL}research/snapshot.json`} download="corte-investigacion.json" className="inline-block glass-input rounded-lg px-4 py-2 mt-5 text-sm">Descargar corte y referencias</a></section>
    </>}
  </div>
}
