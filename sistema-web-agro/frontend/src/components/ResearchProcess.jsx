import React, { useEffect, useState } from 'react'
import { useAuth } from '../App.jsx'
import { researchApi } from '../lib/researchApi.js'

export default function ResearchProcess({ data }) {
  const { token } = useAuth()
  const [active, setActive] = useState(0)
  const [audit, setAudit] = useState(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [steps, setSteps] = useState([])
  const [note, setNote] = useState('')
  useEffect(() => { verify() }, [token])
  const selected = steps[active]
  const proof = audit?.files.find(f => f.artifact === selected?.evidence)
  async function verify() {
    setBusy(true); setError(''); setAudit(null)
    try { const current = await researchApi('progress', token); setAudit(current); setSteps(current.stages); setNote(current.note) } catch (e) { setError(e.message) }
    finally { setBusy(false) }
  }
  return <div className="space-y-6 research-enter">
    <div className="flex flex-wrap items-center justify-between gap-4"><div><h2 className="font-headline-md text-xl">De la fuente al resultado</h2><p className="text-sm text-on-surface-variant mt-2">Seleccione una etapa para consultar evidencia y pendientes reales.</p></div>
      <button onClick={verify} disabled={busy} className="research-button glass-input rounded-lg px-4 py-3 text-sm text-primary disabled:opacity-50">{busy ? 'Comprobando archivos…' : 'Verificar integridad ahora'}</button></div>
    {note && <p className="glass-panel rounded-xl p-4 text-sm text-on-surface-variant">{note}</p>}
    {busy && <p role="status" className="text-primary text-sm">Comprobando el estado actual del proyecto...</p>}
    <ol className="grid sm:grid-cols-2 xl:grid-cols-5 gap-3" aria-label="Etapas del proceso">
      {steps.map((step, index) => <li key={step.name}><button aria-pressed={active === index} onClick={() => setActive(index)} className={`research-stage glass-card rounded-xl p-4 w-full h-full text-left ${active === index ? 'border-primary/60 bg-primary/10' : ''}`}>
        <div className="flex justify-between text-primary mb-4"><span className="material-symbols-outlined" aria-hidden="true">{step.icon}</span><span className="font-mono text-xs">0{index + 1}</span></div>
        <span className="block font-semibold mb-2">{step.name}</span><span className="text-xs text-on-surface-variant">{step.state}</span></button></li>)}
    </ol>
    {selected && <section key={active} className="glass-card rounded-xl p-6 research-enter" aria-live="polite"><div className="flex flex-wrap justify-between gap-3"><h3 className="font-headline-md text-xl">{selected.name}</h3><span className="text-primary text-sm">{selected.number}</span></div>
      <p className="text-sm text-on-surface-variant leading-relaxed mt-4">{selected.text}</p>
      <div className="glass-panel rounded-lg p-4 mt-5"><p className="text-xs uppercase tracking-wider text-on-surface-variant mb-2">Pendiente</p><p className="text-sm">{selected.pending}</p></div>
      <p className="text-xs text-on-surface-variant mt-5">Artefacto: <span className="font-mono">{selected.evidence}</span></p>
      {proof && <div className="mt-3 text-xs space-y-2"><p className={proof.matches ? 'text-primary' : 'text-error'}>{proof.matches ? 'Hash coincide con el manifiesto registrado' : 'Integridad no confirmada'}</p><p className="font-mono break-all text-on-surface-variant">SHA256: {proof.actual_sha256 || 'Archivo ausente'}</p></div>}
    </section>}
    {busy && <p role="status" className="text-sm text-primary">Se comparan bytes contra el manifiesto; no se ejecuta entrenamiento.</p>}
    {error && <p role="alert" className="glass-panel border border-error/30 rounded-xl p-4 text-sm text-error">{error}</p>}
    {audit && <div role="status" className={`glass-panel rounded-xl p-4 text-sm ${audit.integrity_ok ? 'text-primary' : 'text-error'}`}>
      {audit.verified_files} de {audit.total_files} archivos coinciden. Comprobación: {new Date(audit.checked_at).toLocaleString('es-PE')}.
      <p className="text-on-surface-variant text-xs mt-2">La integridad de bytes no acredita verdad económica, completitud de cobertura ni disponibilidad histórica.</p>
    </div>}
    {!audit && !busy && !error && <p className="text-xs text-on-surface-variant">Estados tomados del corte documentado. La comprobación actual del backend se ejecuta al pulsar el botón.</p>}
  </div>
}
