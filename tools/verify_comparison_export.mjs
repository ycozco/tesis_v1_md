import fs from 'node:fs'
import assert from 'node:assert/strict'
import { comparisonCsv } from '../sistema-web-agro/frontend/src/lib/comparisonCsv.js'
const snapshot = JSON.parse(fs.readFileSync(new URL('../sistema-web-agro/frontend/public/research/snapshot.json', import.meta.url)))
const weeks = new Map()
for (let date = new Date('2025-10-20T00:00:00Z'); date <= new Date('2026-10-19T00:00:00Z'); date.setUTCDate(date.getUTCDate() + 7)) {
  const week = date.toISOString().slice(0, 10); weeks.set(week, { week, main: null, comparison: null })
}
for (const row of snapshot.weekly_rows) {
  if (row[0] !== 'palta' || !weeks.has(row[2])) continue
  if (row[1] === 'US') weeks.get(row[2]).main = row[3]
  if (row[1] === 'NL') weeks.get(row[2]).comparison = row[3]
}
const csv = comparisonCsv([...weeks.values()], 'palta', 'US', 'NL', 'USD/kg', snapshot.manifest.views.conservadora.input_sha256)
const lines = csv.slice(1).split('\r\n')
assert.equal(lines.length, 54)
assert.equal(lines.filter(line => line.includes('"unknown"')).length, 23)
const knownZero = comparisonCsv([{ week: '2026-01-05', main: 0, comparison: null }], 'palta', 'US', '', 'USD/kg', 'sha')
assert.ok(knownZero.includes('"0";"USD/kg";"";"";"observed_partial"'))
assert.ok(csv.includes('"2026-10-19";"palta";"US";"";"USD/kg"'))
console.log(JSON.stringify({ status: 'passed', export_rows: 53, unknown_values_preserved: 23, observed_zero_preserved: true, browser_file_materialization_not_claimed: true }))
