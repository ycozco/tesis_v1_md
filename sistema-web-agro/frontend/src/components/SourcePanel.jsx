import React, { useEffect, useState } from 'react'
import { useAuth } from '../App.jsx'
import ResearchIcon from './ResearchIcon.jsx'

const date = value => value ? new Date(value).toLocaleString('es-PE', { timeZone: 'America/Lima', dateStyle: 'short', timeStyle: 'short' }) : 'Sin consulta registrada'
const scopes = ['Registros de exportación', 'Precios mayoristas internos', 'Contexto cambiario', 'Documentación meteorológica']
export default function SourcePanel({ data }) {
  const { token } = useAuth()
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [attempt, setAttempt] = useState(0)
  useEffect(() => {
    const abort = new AbortController()
    async function load() {
      setLoading(true); setError('')
      try {
        const response = await fetch('/api/research/sources', { signal: abort.signal, headers: { Authorization: `Bearer ${token}` } })
        if (!response.ok) throw new Error(response.status === 401 ? 'Vuelva a iniciar sesión para consultar las fuentes.' : 'No se pudo verificar la conexión con las fuentes.')
        const body = await response.json()
        if (!abort.signal.aborted) setResult(body)
      } catch (e) { if (!abort.signal.aborted) setError(e.message) }
      finally { if (!abort.signal.aborted) setLoading(false) }
    }
    load()
    const timer = setInterval(load, 15 * 60 * 1000)
    return () => { abort.abort(); clearInterval(timer) }
  }, [token, attempt])
  const rows = result?.sources || data.sources.map((s, i) => ({ ...s, id: i, scope: scopes[i], status: 'unchecked' }))
  const lastWeek = data.weekly_rows.reduce((last, row) => row[6] === 'observed_partial' && row[2] > last ? row[2] : last, '')
  return <section className="glass-card rounded-xl p-5 space-y-4" aria-label="Fuentes y actualización">
    <div className="flex flex-wrap items-center justify-between gap-3"><div><h2 className="research-chart-title text-xl font-semibold"><ResearchIcon name="source" />Fuentes y actualización</h2><p className="text-xs text-on-surface-variant mt-2">Corte local: {data.generated_on} · Última semana con registros: {lastWeek}</p></div><button disabled={loading} className="glass-input research-button rounded-lg px-4 py-2 text-sm text-primary disabled:opacity-50" onClick={() => setAttempt(a => a + 1)}>{loading ? 'Consultando fuentes…' : 'Comprobar fuentes'}</button></div>
    <p className="text-sm text-on-surface-variant">Los gráficos conservan el corte de investigación. La consulta externa verifica enlaces y obtiene contexto del BCRP; se renueva cada 15 minutos.</p>
    {error && <p role="alert" className="research-warning text-sm">{error}</p>}
    <div className="research-source-grid">{rows.map(source => <article key={source.id} className="research-source-card">
      <div className="flex flex-wrap items-center justify-between gap-2"><a href={source.url} target="_blank" rel="noreferrer" className="text-primary font-semibold underline underline-offset-4">{source.name} ↗</a><span className={`research-status ${source.status === 'available' ? 'is-success' : 'is-pending'}`}>{source.status === 'available' ? (source.id === 'bcrp' ? 'Serie consultada' : 'Enlace accesible') : source.status === 'unchecked' ? 'Sin verificar' : 'Consulta no disponible'}</span></div>
      <p className="text-sm text-on-surface-variant mt-3">{source.scope}</p>
      <p className="text-xs text-on-surface-variant mt-3">Última consulta: {date(source.checked_at)} · Lima</p>
      {source.last_success_at && source.status !== 'available' && <p className="text-xs text-on-surface-variant mt-2">Última consulta exitosa: {date(source.last_success_at)}</p>}
      {source.live_observation && <div className="research-live-value"><strong>{source.live_observation.value.toLocaleString('es-PE', { maximumFractionDigits: 3 })} {source.live_observation.unit}</strong><span>{source.live_observation.period} · promedio mensual{source.status !== 'available' ? ' · última respuesta disponible' : ''}</span><a href={source.live_observation.url} target="_blank" rel="noreferrer" className="underline">Consultar serie PN01207PM ↗</a></div>}
      {source.reason && <p className="text-xs research-warning mt-2">{source.reason}</p>}
    </article>)}</div>
    <details className="research-info text-xs text-on-surface-variant"><summary className="cursor-pointer py-2">Fechas y alcance</summary><p className="leading-relaxed mt-2">La fecha del corte indica cuándo se generó el archivo local. La fecha de incorporación individual y la fecha de publicación histórica no están certificadas para todas las fuentes. Un enlace accesible no confirma que el conjunto esté completo. NASA POWER enlaza documentación; SISAP describe mercado interno y requiere revisar la unidad publicada.</p></details>
  </section>
}
