import { useEffect, useRef, useState } from 'react'
import { researchApi } from '../lib/researchApi.js'
import { useAuth } from '../App.jsx'

const topics = { trade: 'Oferta, exportación y composición comercial', logistics: 'Logística y embarques', weather: 'Clima y producción' }
export default function ResearchNews({ item }) {
  const { token } = useAuth()
  const [topic, setTopic] = useState('trade')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const request = useRef(0)
  useEffect(() => { request.current++; setResult(null); setError(''); setBusy(false); setTopic('trade'); return () => { request.current++ } }, [item.id])
  async function search() {
    const id = ++request.current
    setBusy(true); setError(''); setResult(null)
    try {
      const data = await researchApi('news', token, { method: 'POST', body: JSON.stringify({ product: item.product, week: item.week, topic }) })
      if (id === request.current) setResult(data)
    } catch (e) { if (id === request.current) setError(e.message) }
    finally { if (id === request.current) setBusy(false) }
  }
  return <section className="ui-panel rounded-xl p-5 space-y-4" aria-label="Noticias experimentales">
    <div><span className="text-xs text-tertiary uppercase tracking-wider">Panel experimental</span><h3 className="font-headline-md text-xl mt-2">Noticias para contrastar la interpretación</h3></div>
    <p className="text-sm text-on-surface-variant">Sugerencia de esta revisión Codex: contrastar oferta y composición de embarques; explorar logística y clima como hipótesis alternativas. Una coincidencia en noticias no demuestra la causa de la variación.</p>
    <label className="block text-sm">Tema a investigar<select value={topic} disabled={busy} onChange={e => { setTopic(e.target.value); setResult(null); setError('') }} className="ui-input rounded-lg p-3 mt-2 w-full">{Object.entries(topics).map(([id, label]) => <option key={id} value={id}>{label}</option>)}</select></label>
    <p className="text-xs text-on-surface-variant">GDELT · producto + Perú + tema · semana {item.week} (7 días, limitada a hoy). La consulta envía solo estos filtros públicos. No envía cuentas, veredictos ni archivos.</p>
    <button disabled={busy} onClick={search} className="ui-input rounded-lg px-4 py-3 text-primary disabled:opacity-50">{busy ? 'Consultando noticias…' : 'Buscar noticias de esta semana'}</button>
    {error && <p role="alert" className="text-sm text-error">{error}</p>}
    {result && <div aria-live="polite" className="space-y-3"><p className="text-xs text-on-surface-variant">Consulta: {result.queried_at} · {result.start} a {result.end} · {result.cached ? 'Caché de hasta 15 min' : 'Consulta al proveedor'}</p><p className="text-xs font-mono break-words">{result.query}</p>{result.articles.length === 0 && <p className="text-sm">No se encontraron coincidencias. Esto no prueba ausencia de eventos.</p>}<ul className="space-y-3">{result.articles.map(a => <li key={a.url} className="ui-card rounded-lg p-4"><a className="text-primary underline text-sm" href={a.url} target="_blank" rel="noopener noreferrer">{a.title} ↗</a><p className="text-xs text-on-surface-variant mt-2">{a.domain} · Indexación GDELT: {a.indexed_at || 'Sin fecha'} · {a.language || 'Sin idioma'}</p></li>)}</ul></div>}
    <p className="text-xs text-on-surface-variant">La fecha de indexación no sustituye la fecha de publicación. Abra la fuente para verificarla. Noticias no auditadas; no modifican los datos ni los resultados del experimento. <a className="underline" href="https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/" target="_blank" rel="noreferrer">Documentación de GDELT</a>.</p>
  </section>
}
