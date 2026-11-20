import assert from 'node:assert/strict'
import fs from 'node:fs'
import { validDate, isoMonday, rangePreset, observedDates, comparisonSeries, rangeError } from '../sistema-web-agro/frontend/src/lib/temporalFilters.js'
import { forecastSelection } from '../sistema-web-agro/frontend/src/lib/forecastView.js'
const snapshot=JSON.parse(fs.readFileSync('sistema-web-agro/frontend/public/research/snapshot.json'))
const payload=JSON.parse(fs.readFileSync('sistema-web-agro/frontend/public/research/forecasts.json'))
assert.equal(validDate('2026-02-31'),false)
assert.equal(isoMonday('2026-10-18'),'2026-10-12')
assert.ok(rangeError('2026-11-01','2026-10-01'))
assert.ok(rangeError('0001-01-01','9999-12-31'))
const palta=observedDates(snapshot.weekly_rows,'palta','US')
assert.equal(palta.at(-1),'2026-10-12')
assert.equal(rangePreset(palta,4).end,'2026-10-12')
assert.equal(rangePreset(palta,0).start,palta[0])
const opts={product:'uva',destination:'US',compare:'NL',target:'unit_fob',start:'2026-10-13',end:'2026-10-25'}
const series=comparisonSeries(snapshot.weekly_rows,opts)
assert.deepEqual(series.map(r=>r.week),['2026-10-12','2026-10-19'])
for(const point of series)for(const [field,dest]of [['main','US'],['comparison','NL']])assert.equal(point[field],snapshot.weekly_rows.find(r=>r[0]==='uva'&&r[1]===dest&&r[2]===point.week)[3])
const f=forecastSelection(payload,snapshot,{...opts,mode:'history',methods:['xgb','lgb','naive']})
assert.equal(f.selected.length,0)
assert.equal(f.graph.length,2)
assert.ok(f.graph.every(r=>Number.isFinite(r.actual)&&r.xgb===null))
const inWeek=forecastSelection(payload,snapshot,{...opts,start:'2026-04-21',end:'2026-04-26',mode:'history',methods:['xgb','naive']})
assert.equal(inWeek.graph[0].week,'2026-04-20')
assert.ok(inWeek.selected.length>0)
console.log('Fechas: semanas inclusivas, ausencia de pronósticos recientes, rangos reales por producto y correspondencia gráfico/tabla verificados.')
