import { useEffect, useId, useState } from 'react'
import { rangeError, rangePreset } from '../lib/temporalFilters.js'

// Draft inputs keep partial keyboard/calendar edits out of the shared URL and charts.
export default function DateRangeControl({ start, end, onApply, dates = [], label = 'Rango de fechas', presets = true }) {
  const id = useId()
  const [draft, setDraft] = useState({ start, end })
  const [submitted, setSubmitted] = useState(false)
  useEffect(() => { setDraft({ start, end }); setSubmitted(false) }, [start, end])
  const error = rangeError(draft.start, draft.end)
  const changed = draft.start !== start || draft.end !== end
  function apply(event) { event.preventDefault(); setSubmitted(true); if (!error) onApply(draft) }
  return <form onSubmit={apply} noValidate className="research-date-range space-y-3" aria-label={label}>
    <div className="flex flex-wrap items-end gap-3">
      <label className="text-sm flex-1 min-w-[150px]" htmlFor={id + '-start'}>Desde<input id={id + '-start'} type="date" className="ui-input rounded-lg p-3 mt-2 w-full" value={draft.start} aria-describedby={id + '-help'} onInput={e => { const value = e.currentTarget.value; setDraft(d => ({ ...d, start: value })); setSubmitted(false) }} onChange={e => { const value = e.target.value; setDraft(d => ({ ...d, start: value })); setSubmitted(false) }} /></label>
      <label className="text-sm flex-1 min-w-[150px]" htmlFor={id + '-end'}>Hasta<input id={id + '-end'} type="date" className="ui-input rounded-lg p-3 mt-2 w-full" value={draft.end} aria-describedby={id + '-help'} onInput={e => { const value = e.currentTarget.value; setDraft(d => ({ ...d, end: value })); setSubmitted(false) }} onChange={e => { const value = e.target.value; setDraft(d => ({ ...d, end: value })); setSubmitted(false) }} /></label>
      <button type="submit" className="research-action rounded-lg px-4 py-3 text-sm">Aplicar fechas</button>
      {changed && <button type="button" className="ui-input rounded-lg px-4 py-3 text-sm" onClick={() => { setDraft({ start, end }); setSubmitted(false) }}>Cancelar cambios</button>}
    </div>
    <p id={id + '-help'} className="text-xs text-on-surface-variant">{changed ? 'Fechas editadas sin aplicar. Pulse Aplicar fechas o Enter.' : `Rango aplicado: ${start || 'sin inicio'} — ${end || 'sin fin'}.`} Se incluyen las semanas ISO que contienen estas fechas.</p>
    {submitted && error && <p role="alert" className="text-error text-sm">{error}</p>}
    {presets && dates.length > 0 && <div className="flex flex-wrap gap-2" aria-label="Periodos rápidos">{[[4, '4 semanas'], [12, '12 semanas'], [26, '6 meses aprox.'], [52, '12 meses aprox.'], [0, 'Todo el histórico']].map(([weeks, name]) => <button type="button" key={weeks} className="ui-input rounded-lg px-3 py-2 text-sm text-primary" onClick={() => onApply(rangePreset(dates, weeks))}>{name}</button>)}</div>}
    {dates.length > 0 && <p className="text-xs text-on-surface-variant">Semanas con valores para esta selección: {dates[0]} — {dates.at(-1)}. Los accesos rápidos terminan en la última semana disponible; no en la fecha de hoy.</p>}
  </form>
}
