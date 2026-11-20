import assert from 'node:assert/strict'
import fs from 'node:fs'
import crypto from 'node:crypto'
import { samePeriodContext, experimentalNarrative } from '../sistema-web-agro/frontend/src/lib/codexInterpretation.js'
const context=JSON.parse(fs.readFileSync('sistema-web-agro/frontend/public/research/interpretation-context.json'))
for(const source of context.sources) assert.equal(crypto.createHash('sha256').update(fs.readFileSync(source.file)).digest('hex'),source.sha256)
const april=samePeriodContext(context,'2026-04-20','2026-04-20','uva')
assert.equal(april.exchange.length,1);assert.equal(april.exchange[0].month,'2026-04')
assert.equal(april.climate.T2M_MAX.days,7)
assert.ok(april.local.length>0)
const october=samePeriodContext(context,'2026-10-19','2026-10-19','arandano')
assert.equal(october.exchange.length,0)
assert.equal(october.climate.T2M_MAX.complete,false)
assert.equal(october.climate.T2M_MAX.days,4)
assert.equal(october.local.length,0)
const future=samePeriodContext(context,'2026-11-02','2026-11-02','uva')
assert.equal(future.climate.records,0);assert.equal(future.exchange.length,0)
const job={config:{target:'unit_fob'},validation_weeks:['2026-04-20'],versions:{statsforecast:'2.0.3'},results:{statsforecast:{status:'completed',weeks:['2026-04-20'],actual:[100],models:[{model:'Naive',mae:5,values:[105]},{model:'AutoETS',mae:40,values:[140]}]}}}
const n=experimentalNarrative(job)
assert.ok(n.paragraphs[0].includes('Naive'));assert.ok(n.paragraphs[1].includes('2 de 2'))
assert.equal(n.models[0].version,'2.0.3')
console.log('Interpretación: procedencia, semanas exactas, clima parcial, dólar mensual, ausencia de datos y modelos verificados.')
