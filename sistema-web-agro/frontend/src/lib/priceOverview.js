import { addWeek, weekGrid } from './revisionComparison.js'
export function pricePeriods(rows, start, end) {
  const aggregate = new Map()
  for (const r of rows) {
    if (!aggregate.has(r[2])) aggregate.set(r[2], { week:r[2], fob:0, volume:0, count:0 })
    if (r[6] === 'observed_partial' && Number.isFinite(r[4]) && r[4] > 0 && Number.isFinite(r[5])) {
      const a=aggregate.get(r[2]); a.fob+=r[5]; a.volume+=r[4]; a.count++
    }
  }
  const known=[...aggregate.keys()].sort()
  const grid=weekGrid(start || known[0] || '', end || known.at(-1) || '')
  const weeks=grid.map(week=>{const a=aggregate.get(week);return {week,price:a?.volume>0?a.fob/a.volume:null,volume:a?.count?a.volume:null,fob:a?.count?a.fob:null,count:a?.count||0}})
  const months=new Map()
  for(const w of weeks){const key=w.week.slice(0,7);if(!months.has(key))months.set(key,{month:key,fob:0,volume:0,weeks:0,observed:0});const m=months.get(key);m.weeks++;if(w.price!=null){m.fob+=w.fob;m.volume+=w.volume;m.observed++}}
  const monthly=[...months.values()].map(m=>({...m,price:m.volume>0?m.fob/m.volume:null}))
  const last=weeks.at(-1), previous=weeks.at(-2)
  const recent=weeks.slice(-4).filter(w=>w.price!=null)
  const fourVolume=recent.reduce((s,w)=>s+w.volume,0)
  const four=fourVolume>0?recent.reduce((s,w)=>s+w.fob,0)/fourVolume:null
  const change=last?.price!=null&&previous?.price>0?(last.price/previous.price-1)*100:null
  return {weeks,monthly,last,previous,four,fourCount:recent.length,change,lastObserved:weeks.filter(w=>w.price!=null).at(-1)}
}
export function overviewPreset(cut,weeks){return {start:addWeek(cut,1-weeks),end:cut}}
