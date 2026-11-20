import { addWeek, weekGrid } from './revisionComparison.js'

export function validDate(value) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value || '')) return false
  const date = new Date(value + 'T00:00:00Z')
  return Number.isFinite(+date) && date.toISOString().slice(0, 10) === value
}
export function isoMonday(value) {
  if (!validDate(value)) return ''
  const date = new Date(value + 'T00:00:00Z')
  date.setUTCDate(date.getUTCDate() - (date.getUTCDay() + 6) % 7)
  return date.toISOString().slice(0, 10)
}
export function observedDates(rows, product, destination = '', target = 'unit_fob') {
  const column = target === 'volume_kg' ? 4 : 3
  return [...new Set(rows.filter(r => r[0] === product && (!destination || r[1] === destination) && Number.isFinite(r[column])).map(r => r[2]))].sort()
}
export function rangePreset(dates, weeks = 12) {
  const end = dates.at(-1) || ''
  return { start: end ? weeks ? [dates[0], addWeek(end, 1 - weeks)].sort().at(-1) : dates[0] : '', end }
}
export function rangeError(start, end) {
  if (!validDate(start) || !validDate(end)) return 'Complete ambas fechas con un día válido.'
  if (start > end) return 'La fecha inicial debe ser anterior o igual a la final.'
  if (Date.parse(end) - Date.parse(start) > 20 * 366 * 86400000) return 'Seleccione un rango de hasta 20 años.'
  return ''
}
export function comparisonSeries(rows, { product, destination, compare, target, start, end }) {
  if (rangeError(start, end)) return []
  const lookup = new Map(rows.filter(r => r[0] === product && [destination, compare].includes(r[1])).map(r => [r[1] + r[2], r[target === 'volume_kg' ? 4 : 3]]))
  return weekGrid(isoMonday(start), isoMonday(end)).map(week => ({ week, main: lookup.get(destination + week) ?? null, comparison: compare ? lookup.get(compare + week) ?? null : null }))
}
