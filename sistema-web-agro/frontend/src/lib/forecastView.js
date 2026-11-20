import { addWeek, paddedDomain, weekGrid } from './revisionComparison.js'
import { isoMonday, rangeError } from './temporalFilters.js'
export const METHODS = { xgb: { label: 'XGBoost', color: '#007bb5' }, lgb: { label: 'LightGBM', color: '#a35bc2' }, naive: { label: 'Último valor', color: '#ce7224' }, mean4: { label: 'Media de 4 semanas', color: '#00877d' }, seasonal52: { label: 'Estacional 52', color: '#7c6724' } }
export function forecastSelection(payload, snapshot, { product, destination, target, mode, emission, start, end, methods }) {
  if ((mode === 'emission' && !isoMonday(emission)) || (mode !== 'emission' && rangeError(start, end))) return { selected: [], graph: [], metrics: [], domain: [0, 1] }
  if (mode !== 'emission') { start = isoMonday(start); end = isoMonday(end) }
  const rows = payload.rows.filter(r => r[0] === product && r[1] === destination && r[2] === target)
  const candidates = rows.filter(r => mode === 'emission' ? r[4] === emission : r[5] >= start && r[5] <= end)
  const selected = candidates.filter(r => methods.includes(r[3]) && Number.isFinite(r[7]))
  const from = mode === 'emission' ? addWeek(emission, -8) : start
  const to = mode === 'emission' ? emission : end
  const observations = new Map(snapshot.weekly_rows.filter(r => r[0] === product && r[1] === destination).map(r => [r[2], r[target === 'unit_fob' ? 3 : 4]]))
  const graph = weekGrid(from, to).map(week => {
    const point = { week, actual: observations.get(week) ?? null }
    for (const method of methods) {
      const row = selected.find(r => r[3] === method && r[5] === week)
      point[method] = row?.[7] ?? null
      if (mode === 'emission' && selected.some(r => r[3] === method && r[9] === week)) point[method] = observations.get(week) ?? null
    }
    return point
  })
  const metrics = methods.map(method => {
    const valid = selected.filter(r => r[3] === method && Number.isFinite(r[6]))
    const paired = valid.map(r => ({ row: r, baseline: candidates.find(b => b[3] === 'naive' && b[4] === r[4] && b[5] === r[5] && Number.isFinite(b[7])) })).filter(p => p.baseline)
    return { method, count: valid.length, mae: valid.length ? valid.reduce((sum, r) => sum + Math.abs(r[7] - r[6]), 0) / valid.length : null,
      pairedCount: paired.length, pairedMae: paired.length ? paired.reduce((sum, p) => sum + Math.abs(p.row[7] - p.row[6]), 0) / paired.length : null,
      baselineMae: paired.length ? paired.reduce((sum, p) => sum + Math.abs(p.baseline[7] - p.row[6]), 0) / paired.length : null }
  })
  return { selected, graph, metrics, domain: paddedDomain(graph.flatMap(r => [r.actual, ...methods.map(m => r[m])])) }
}
