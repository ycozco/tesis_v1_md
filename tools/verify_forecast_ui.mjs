import assert from 'node:assert/strict'
import fs from 'node:fs'
import crypto from 'node:crypto'
import { forecastSelection } from '../sistema-web-agro/frontend/src/lib/forecastView.js'
const payload=JSON.parse(fs.readFileSync('sistema-web-agro/frontend/public/research/forecasts.json'))
const data=JSON.parse(fs.readFileSync('sistema-web-agro/frontend/public/research/snapshot.json'))
for(const [file,sha] of Object.entries(payload.source_sha256)) assert.equal(crypto.createHash('sha256').update(fs.readFileSync('datasets/tratamiento/2026-11-01/'+file)).digest('hex'),sha)
const opts={product:'uva',destination:'US',target:'unit_fob',mode:'emission',emission:'2026-04-20',start:'2026-03-02',end:'2026-04-20',methods:['xgb','lgb','naive']}
const r=forecastSelection(payload,data,opts)
assert.equal(r.selected.length,3)
assert.equal(payload.emission_kind, 'simulated_week_boundary_date')
for (const row of r.selected) {
  assert.deepEqual(row.slice(4,6), ['2026-04-20','2026-04-20'])
  assert.deepEqual(row.slice(8,10), ['2026-04-13','2026-04-13'])
}
assert.equal(r.graph.at(-1).week,'2026-04-20')
assert.equal(r.graph.at(-1).xgb,r.selected.find(x=>x[3]==='xgb')[7])
assert.ok(Math.abs(r.graph.at(-1).actual-r.selected[0][6])<1e-8)
assert.equal(r.graph.slice(0,-2).filter(p=>p.xgb!=null).length,0)
assert.equal(r.metrics.find(m=>m.method==='xgb').count,1)
assert.equal(forecastSelection(payload,data,{...opts,emission:'2026-11-02'}).selected.length,0)
assert.equal(forecastSelection(payload,data,{...opts,emission:''}).graph.length,0)
const h=forecastSelection(payload,data,{...opts,mode:'history'})
assert.ok(h.selected.length>3)
assert.equal(h.metrics.find(m=>m.method==='xgb').pairedCount,h.metrics.find(m=>m.method==='xgb').count)
assert.equal(forecastSelection(payload,data,{...opts,methods:[]}).selected.length,0)
console.log(`Pronósticos: ${payload.rows.length} filas, huellas verificadas, calendario, correspondencia con observados, filtros y métricas emparejadas correctos.`)
