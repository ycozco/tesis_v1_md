import React from 'react'
import RevisionComparison from './RevisionComparison.jsx'
import ResearchNews from './ResearchNews.jsx'
import { Link } from 'react-router-dom'
import revision from '../../public/research/codex-revision-2026-11-06.json'

const names = { palta: 'Palta', uva: 'Uva fresca', arandano: 'Arándano' }
const num = (v, digits = 2) => Number(v).toLocaleString('es-PE', { maximumFractionDigits: digits })
export default function CodexRevision({ data }) {
  const [selected, setSelected] = React.useState(revision.cases[0].id)
  const item = revision.cases.find(c => c.id === selected)
  const fobDelta = (item.observed.fob_usd / item.previous.fob_usd - 1) * 100
  return <section className="ui-card rounded-xl p-5 md:p-6 space-y-5" aria-label="Revisión Codex de observaciones recientes">
    <div className="flex flex-wrap items-start justify-between gap-4">
      <div><span className="inline-block ui-input rounded-lg px-3 py-2 text-xs text-primary">{revision.tag}</span><h2 className="font-headline-md text-2xl mt-3">Lectura de los casos más recientes</h2><p className="text-sm text-on-surface-variant mt-2">Revisión: {revision.reviewed_on} · Datos del corte: {revision.snapshot_date} · EE. UU.</p></div>
      <a href={`${import.meta.env.BASE_URL}research/codex-revision-2026-11-06.json`} download className="ui-input rounded-lg px-4 py-3 text-sm text-primary">Descargar revisión y evidencia</a>
    </div>
    <div className="grid md:grid-cols-3 gap-3">{Object.entries(revision.data_status).map(([key, value], i) => <div key={key} className="ui-panel rounded-lg p-4"><h3 className="text-primary text-sm font-semibold">{['Datos obtenidos', 'Datos tratados', 'Proyecciones piloto'][i]}</h3><p className="text-sm text-on-surface-variant mt-2">{value}</p></div>)}</div>
    <p className="text-sm text-on-surface-variant">{revision.selection}</p>
    <div className="flex flex-wrap gap-3" role="group" aria-label="Elegir caso reciente">{revision.cases.map(c => <button key={c.id} aria-pressed={c.id === selected} onClick={() => setSelected(c.id)} className={`ui-input rounded-lg px-4 py-3 text-sm ${c.id === selected ? 'border-primary text-primary' : ''}`}>{names[c.product]} · {c.week}</button>)}</div>
    <article aria-live="polite" className="ui-panel rounded-xl p-5 space-y-4">
      <h3 className="font-headline-md text-xl">{names[item.product]} hacia EE. UU.</h3>
      <p className="text-xs text-on-surface-variant">Semana {item.week} frente a la observación anterior disponible: {item.previous_week}. Cobertura parcial.</p>
      <dl className="grid sm:grid-cols-3 gap-4">{[['Valor unitario FOB', 'unit_fob', 'USD/kg'], ['Volumen registrado', 'volume_kg', 'kg'], ['Valor FOB registrado', 'fob_usd', 'USD']].map(([label, key, unit]) => <div key={key}><dt className="text-xs text-on-surface-variant">{label}</dt><dd className="font-mono text-primary mt-2">{num(item.observed[key])} {unit}</dd><dd className="text-xs text-on-surface-variant mt-2">Anterior: {num(item.previous[key])} {unit}{item.change_pct[key] != null && ` · ${num(item.change_pct[key])}%`}</dd></div>)}</dl>
      <RevisionComparison key={item.id} item={item} data={data} />
      <div className="ui-card rounded-lg p-4"><h4 className="font-semibold">Conclusión cuantitativa</h4><p className="text-sm mt-2">El valor FOB registrado {fobDelta < 0 ? 'disminuyó' : fobDelta > 0 ? 'aumentó' : 'se mantuvo'} {num(Math.abs(fobDelta))} % entre ambas observaciones. {item.change_pct.unit_fob > 0 && fobDelta < 0 ? 'El aumento del valor unitario no compensó la reducción del volumen registrado.' : item.change_pct.unit_fob === 0 ? 'Con el valor unitario constante, el cambio del valor total acompaña al volumen registrado.' : 'La variación del valor total combina los cambios de volumen y valor unitario.'}</p></div>
      <p className="text-sm leading-relaxed">{item.interpretation}</p><p className="text-sm text-tertiary">Siguiente paso: {item.next_action}</p>
      <div className="flex flex-wrap gap-4 text-sm"><Link className="text-primary underline" to={`/dashboard?view=series&product=${item.product}&destination=US&start=${item.previous_week}&end=${item.week}`}>Ver estas observaciones en la serie</Link><Link className="text-primary underline" to={`/dashboard?view=pronosticos&product=${item.product}&destination=US&forecastMode=history&forecastStart=${item.previous_week}&forecastEnd=${item.week}`}>Contrastar modelos piloto</Link><Link className="text-primary underline" to="/dashboard?view=proceso">Revisar trazabilidad</Link></div>
    </article>
    <ResearchNews item={item} />
    <div className="ui-panel rounded-lg p-4 text-xs text-on-surface-variant space-y-2"><p><strong>Fuente del gráfico:</strong> registros SUNAT/ADUANET del corte {revision.snapshot_date}, conciliados y agregados por producto, destino y semana ISO. Valor unitario = suma FOB / suma peso neto.</p><p><strong>Precios locales:</strong> SISAP es contexto mayorista; sus unidades y presentaciones deben comprobarse antes de compararlo con FOB en USD/kg. No se dibuja una equivalencia sin esa comprobación.</p><p><strong>Noticias:</strong> catálogo GDELT; cada artículo conserva el enlace a su medio original. Las observaciones, las hipótesis y las noticias tienen procedencias distintas.</p></div>
    <details className="text-xs text-on-surface-variant"><summary className="cursor-pointer text-primary">Procedencia y alcance de la revisión</summary><div className="mt-3 space-y-2 break-words"><p>{revision.authorship}</p><p>{revision.scope} Revisión humana pendiente.</p><p className="font-mono break-all">SHA256 del corte: {revision.source_sha256}</p></div></details>
  </section>
}
