export const WEEK = 7 * 86400000
export const valueAt = { unit_fob: 3, volume_kg: 4, fob_usd: 5 }
export function addWeek(date, n = 1) { return new Date(Date.parse(date + 'T00:00:00Z') + n * WEEK).toISOString().slice(0, 10) }
export function weekGrid(start, end) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(start) || !/^\d{4}-\d{2}-\d{2}$/.test(end) || start > end) return []
  const date = new Date(start + 'T00:00:00Z')
  if (!Number.isFinite(+date)) return []
  date.setUTCDate(date.getUTCDate() + (8 - date.getUTCDay()) % 7)
  const dates = []
  for (let d = date.toISOString().slice(0, 10); d <= end && dates.length < 600; d = addWeek(d)) dates.push(d)
  return dates
}
export function paddedDomain(values, zero = false) {
  const valid = values.filter(v => typeof v === 'number' && Number.isFinite(v))
  if (!valid.length) return [0, 1]
  const lo = Math.min(...valid), hi = Math.max(...valid)
  const pad = (hi > lo ? (hi - lo) * .12 : Math.max(Math.abs(hi) * .002, .000001))
  return [zero ? 0 : Math.max(0, lo - pad), hi + pad]
}
export function seriesAnalysis(rows, product, destination, metric, start, end) {
  const column = valueAt[metric]
  const lookup = new Map(rows.filter(r => r[0] === product && r[1] === destination).map(r => [r[2], r[column]]))
  const grid = weekGrid(start, end)
  const observed = grid.filter(w => Number.isFinite(lookup.get(w))).map(week => ({ week, value: lookup.get(week) }))
  const first = observed[0], last = observed.at(-1)
  const delta = observed.length >= 2 && first.value !== 0 ? (last.value / first.value - 1) * 100 : null
  const anchor = grid.at(-1)
  const ready = !!anchor && [0, -1, -2, -3].every(n => Number.isFinite(lookup.get(addWeek(anchor, n))))
  return { grid, lookup, observed, first, last, delta, missing: grid.length - observed.length, ready, anchor, estimate: ready ? lookup.get(anchor) : null }
}
