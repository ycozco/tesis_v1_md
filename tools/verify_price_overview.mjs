import assert from 'node:assert/strict'
import { pricePeriods, overviewPreset } from '../sistema-web-agro/frontend/src/lib/priceOverview.js'
const rows=[['palta','US','2026-10-05',99,10,20,'observed_partial'],['palta','NL','2026-10-05',99,30,180,'observed_partial'],['palta','US','2026-10-12',null,null,null,'unknown'],['palta','US','2026-10-19',99,10,70,'observed_partial']]
const r=pricePeriods(rows,'2026-10-05','2026-10-19')
assert.equal(r.weeks[0].price,5)
assert.equal(r.previous.price,null)
assert.equal(r.change,null)
assert.equal(r.four,5.4)
assert.equal(r.monthly[0].price,5.4)
assert.equal(r.monthly[0].observed,2)
assert.equal(pricePeriods([], '2026-11-02','2026-11-09').last.price,null)
assert.deepEqual(overviewPreset('2026-10-19',4),{start:'2026-09-28',end:'2026-10-19'})
assert.equal(pricePeriods(rows,'2026-10-19','2026-10-05').weeks.length,0)
console.log('Résumé prix: pondération par poids, semaines manquantes, mois partiels et périodes vérifiés.')
