import React, { useEffect, useState } from 'react'
import { useAuth } from '../App.jsx'
import { researchApi } from '../lib/researchApi.js'
const productNames = { palta: 'Palta', uva: 'Uva fresca', arandano: 'Arándano' }
const factNames = { unit_fob: 'Valor unitario FOB', volume_kg: 'Volumen neto', fob_usd: 'Valor FOB' }

export default function ResearchAI() {
  const { token, user } = useAuth()
  const [providers, setProviders] = useState([])
  const [cases, setCases] = useState([])
  const [provider, setProvider] = useState('codex_archive')
  const [pilots, setPilots] = useState([])
  const [pilot, setPilot] = useState(null)
  const [caseId, setCaseId] = useState('')
  const [consent, setConsent] = useState(false)
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)
  async function refresh() {
    setLoading(true); setError('')
    try {
      const [p, c, archived] = await Promise.all([researchApi('providers', token), researchApi('cases', token), researchApi('codex-pilots', token)])
      setPilots(archived.pilots)
      setProviders(p.providers); setCases(c.cases); setCaseId(current => current || c.cases[0]?.case_id || '')
    } catch (e) { setError(e.message) } finally { setLoading(false) }
  }
  useEffect(() => { refresh() }, [token])
  const selectedProvider = providers.find(p => p.id === provider)
  const selectedCase = cases.find(c => c.case_id === caseId)
  async function openPilot(id) {
    setBusy(true); setError(''); setPilot(null)
    try { setPilot(await researchApi(`codex-pilots/${id}`, token)) }
    catch (e) { setError(e.message) } finally { setBusy(false) }
  }
  async function downloadPilot() {
    try {
      const response = await fetch(`/api/research/codex-pilots/${pilot.id}/file`, { headers: { Authorization: `Bearer ${token}` } })
      if (!response.ok) throw new Error('No se pudo comprobar el archivo del piloto.')
      const bytes = await response.arrayBuffer()
      const sha = [...new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))].map(v => v.toString(16).padStart(2, '0')).join('')
      if (sha !== pilot.download_sha256 || sha !== response.headers.get('X-Report-SHA256')) throw new Error('La huella del piloto no coincide.')
      const url = URL.createObjectURL(new Blob([bytes], { type: 'application/json' })), link = document.createElement('a')
      link.href = url; link.download = `piloto-${pilot.id}.json`; link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000)
    } catch (e) { setError(e.message) }
  }
  async function generate() {
    setBusy(true); setError(''); setResult(null)
    try { setResult(await researchApi('reports', token, { method: 'POST', body: JSON.stringify({ case_id: caseId, provider, paid_consent: consent }) })) }
    catch (e) { setError(e.message) } finally { setBusy(false) }
  }
  async function download() {
    try {
      const response = await fetch(`/api/research/reports/${result.id}/file`, { headers: { Authorization: `Bearer ${token}` } })
      if (!response.ok) throw new Error('No se pudo verificar el archivo del informe.')
      const bytes = await response.arrayBuffer()
      const sha = [...new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))].map(v => v.toString(16).padStart(2, '0')).join('')
      if (sha !== result.report_sha256 || sha !== response.headers.get('X-Report-SHA256')) throw new Error('La descarga no coincide con la huella del informe.')
      const url = URL.createObjectURL(new Blob([bytes], { type: 'application/json' })), link = document.createElement('a')
      link.href = url; link.download = `borrador-${result.id}.json`; link.click(); URL.revokeObjectURL(url)
    } catch (e) { setError(e.message) }
  }
  return <div className="space-y-6 research-enter">
    <div className="flex flex-wrap justify-between gap-4"><p className="text-sm text-on-surface-variant max-w-2xl">Consulte respuestas de Codex archivadas o solicite un borrador a un proveedor configurado. Abrir un piloto no genera otra respuesta. Ninguno reemplaza los modelos de pronóstico.</p><button onClick={refresh} disabled={loading || busy} className="glass-input rounded-lg px-4 py-2 text-sm">Actualizar conexión</button></div>
    {loading && <p role="status" className="text-primary">Consultando proveedores y evidencia…</p>}
    {error && <p role="alert" className="glass-panel rounded-xl border border-error/30 text-error p-4 text-sm">{error}</p>}
    <section className="grid md:grid-cols-2 xl:grid-cols-4 gap-4" aria-label="Proveedores de generación">{providers.map(p => <button disabled={busy} key={p.id} aria-pressed={provider === p.id} onClick={() => { setProvider(p.id); setConsent(false); setResult(null); setPilot(null) }} className={`glass-card rounded-xl p-5 text-left research-stage ${provider === p.id ? 'border-primary/60' : ''}`}>
      <span className="block font-semibold">{p.label}</span><span className={`block text-xs mt-2 ${p.ready ? 'text-primary' : 'text-on-surface-variant'}`}>{p.archive_only ? `${p.count} respuestas para consultar` : p.ready ? 'Disponible para solicitar' : 'Configuración pendiente'}</span>
      <span className="block font-mono text-xs mt-3 break-all text-on-surface-variant">{p.model || 'Modelo local no configurado'}</span>
      <span className="block text-xs text-on-surface-variant mt-3 leading-relaxed">{p.reason}</span></button>)}</section>
    {provider === 'codex_archive' && pilots.length > 0 && <section className="glass-card rounded-xl p-5 space-y-4" aria-label="Piloto Codex declarado">
      <div><h2 className="font-headline-md text-xl">{selectedProvider?.model}</h2><p className="text-sm text-tertiary mt-2">Identificador declarado por el usuario · sin verificación técnica del modelo</p></div>
      <p className="text-sm text-on-surface-variant">Respuestas redactadas por Codex en este chat sobre casos artificiales. Piloto con exposición previa a las claves; no es una comparación ciega ni parte de las 180 generaciones finales de H4.</p>
      <p className="text-xs text-on-surface-variant">{pilots.length} respuestas originales archivadas · 0 llamadas a DeepSeek · abrir o descargar no añade repeticiones. La aplicación no envía conversaciones al abrir el archivo.</p>
      <div className="grid md:grid-cols-3 gap-3">{pilots.map(p => <button key={p.id} disabled={busy} onClick={() => openPilot(p.id)} className={`glass-input rounded-lg p-4 text-left ${pilot?.id === p.id ? 'border-primary/60' : ''}`}><span className="block font-semibold text-sm">{p.title}</span><span className="block text-primary text-xs mt-2">Abrir respuesta archivada</span></button>)}</div>
      {busy && <p role="status" className="text-primary text-sm">Abriendo archivo y comprobando evidencia…</p>}
      {pilot && <article aria-live="polite" className="glass-panel rounded-xl p-5 space-y-4">
        <div className="flex flex-wrap justify-between gap-3"><h3 className="font-semibold">{pilot.title}</h3><button onClick={downloadPilot} className="text-primary underline text-sm">Descargar piloto con procedencia</button></div>
        <p className="text-sm leading-relaxed whitespace-pre-wrap">{pilot.summary}</p>
        <p className="text-sm text-primary">Afirmaciones numéricas estructuradas: {pilot.numeric_validation.status === 'passed' ? 'coinciden con la referencia' : pilot.numeric_validation.status === 'not_applicable' ? 'no aplicables: abstención prevista' : 'requieren corrección'}.</p>
        <p className="text-xs text-on-surface-variant">Texto y afirmaciones factuales: pendientes de revisión humana. La comprobación numérica no valida todo el texto ni acredita resultados históricos.</p>
        <div className="flex flex-wrap gap-2 text-xs"><span className="glass-input rounded-lg px-3 py-2">Codex · respuesta de este chat</span><span className="glass-input rounded-lg px-3 py-2">Modelo declarado, no verificado</span><span className="glass-input rounded-lg px-3 py-2">Piloto expuesto · H4 final: no</span></div>
        <details className="text-sm"><summary className="cursor-pointer text-primary">Entradas artificiales y trazabilidad</summary><pre className="mt-3 text-xs whitespace-pre-wrap break-words font-mono">{JSON.stringify({ input: pilot.input, provenance: pilot.provenance, delivery: pilot.delivery, sha256: pilot.download_sha256 }, null, 2)}</pre></details>
      </article>}
    </section>}
    {provider !== 'codex_archive' && cases.length > 0 && <section className="glass-card rounded-xl p-5 space-y-4"><label className="block text-sm">Caso y evidencia<select disabled={busy} value={caseId} onChange={e => { setCaseId(e.target.value); setResult(null) }} className="glass-input rounded-lg p-3 w-full mt-2">{cases.map(c => <option key={c.case_id} value={c.case_id}>{productNames[c.producto]} · {c.destino} · {c.week} · {c.case_id}</option>)}</select></label>
      {selectedCase && <dl className="grid sm:grid-cols-3 gap-3">{Object.entries(selectedCase.evidence).map(([id, fact]) => <div key={id} className="glass-panel rounded-lg p-3"><dt className="text-xs text-on-surface-variant break-all">{factNames[id.split('.').pop()]}</dt><dd className="font-mono mt-2 text-primary">{Number(fact.value).toLocaleString('es-PE', { maximumFractionDigits: 2 })} {fact.unit}</dd><dd className="text-xs text-on-surface-variant mt-2 break-all">Fuente: {fact.source_id}</dd></div>)}</dl>}
      {selectedProvider?.paid && <label className="flex gap-3 items-start text-sm text-on-surface-variant"><input type="checkbox" checked={consent} onChange={e => setConsent(e.target.checked)} className="mt-1" />Acepto enviar únicamente estos hechos agregados a DeepSeek y el consumo de su API. No se envían RUC, nombres de exportadores ni archivos originales.</label>}
      {selectedProvider?.paid && user?.rol !== 'ADMIN' && <p className="text-sm text-on-surface-variant">El consumo de API de pago requiere una cuenta administradora.</p>}
      <button onClick={generate} disabled={busy || loading || !selectedProvider?.ready || !caseId || (selectedProvider?.paid && (!consent || user?.rol !== 'ADMIN'))} className="research-button bg-primary-container text-on-primary-container rounded-lg px-5 py-3 disabled:opacity-40 disabled:cursor-not-allowed">{busy ? 'Generando y comprobando…' : provider === 'template' ? 'Crear borrador sin IA' : 'Solicitar borrador con IA'}</button>
      <p className="text-xs text-on-surface-variant">Hasta 800 tokens de salida para proveedores IA. La tarifa corresponde al proveedor. Las claves se configuran en el servidor y no se muestran aquí.</p>
    </section>}
    {result && <section className="glass-card rounded-xl p-6 research-enter space-y-4" aria-live="polite"><div className="flex flex-wrap justify-between gap-3"><h2 className="font-headline-md text-xl">Borrador para revisión</h2><button className="text-primary underline text-sm" onClick={download}>Descargar resultado y evidencia</button></div>
      <p className="text-sm whitespace-pre-wrap">{result.summary}</p>
      <div className="glass-panel rounded-lg p-4 text-sm"><p className={result.validation.numeric_status === 'passed' ? 'text-primary' : 'text-error'}>Comprobación numérica: {result.validation.numeric_status === 'passed' ? 'coincide con los hechos' : 'requiere corrección'}</p><p className="text-on-surface-variant mt-2">Sustento del texto: requiere revisión humana. No es un reporte H4 evaluado ni acredita fraude, causalidad o cumplimiento legal.</p></div>
      <ul className="space-y-2 text-sm">{result.validation.claims.map((item, i) => <li key={i} className="flex flex-wrap gap-2"><span className={item.valid ? 'text-primary' : 'text-error'}>{item.valid ? '✓' : '×'}</span><span className="font-mono break-all">{item.claim.fact_id}: {item.claim.value} {item.claim.unit}</span><span className="text-on-surface-variant">{item.valid ? 'Verificado numéricamente' : item.reason}</span></li>)}</ul>
      <div className="text-xs font-mono text-on-surface-variant break-all space-y-2"><p>ID: {result.id}</p><p>Proveedor / modelo: {result.provider} / {result.model}</p><p>SHA256 evidencia: {result.evidence_sha256}</p><p>SHA256 payload archivado: {result.report_sha256}</p></div>
    </section>}
    <div className="glass-panel rounded-xl p-4 text-xs text-on-surface-variant leading-relaxed">Codex es un archivo de respuestas de este chat, no un servicio remoto conectado. Ollama y DeepSeek conservan su configuración independiente. La caché de prefijos del proveedor no reutiliza respuestas como nuevas repeticiones; el registro local tampoco añade generaciones. RAG completo y H4 final siguen pendientes.</div>
  </div>
}
