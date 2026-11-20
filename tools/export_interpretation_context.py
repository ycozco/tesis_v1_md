"""Export dated contextual observations for descriptive interpretation, not model features."""
import os
import csv
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
ROOT=Path(os.environ.get('RESEARCH_ROOT',Path(__file__).resolve().parents[1]))
BASE=ROOT/'datasets/tratamiento/2026-11-01'
nasa_path=BASE/'contexto/nasa-arequipa-contexto-2018-2026.json'
bcrp_path=BASE/'bcrp-mensual-conciliado.csv'
sisap_path=BASE/'contexto/sisap-mensual-normalizado.csv'
nasa=json.loads(nasa_path.read_text(encoding='utf-8-sig'))
parameters=nasa['properties']['parameter']
weeks={}
for key in sorted(set().union(*(p.keys() for p in parameters.values()))):
    day=datetime.strptime(key,'%Y%m%d').date();week=(day-timedelta(days=day.weekday())).isoformat()
    block=weeks.setdefault(week,{k:[] for k in parameters})
    for variable,values in parameters.items():
        value=values.get(key)
        if isinstance(value,(int,float)) and value!=-999 and value>-900:block[variable].append(value)
weekly=[]
for week,block in weeks.items():
    entry={'week':week,'days':{k:len(v) for k,v in block.items()}}
    for variable,values in block.items():
        entry[variable]=(sum(values) if variable=='PRECTOTCORR' else sum(values)/len(values)) if values else None
    weekly.append(entry)
with bcrp_path.open(encoding='utf-8-sig') as file:
    exchange=[{'month':r['month'],'pen_per_usd':float(r['pen_per_usd']),'published_at':r['published_at'] or None,'eligible_asof':False} for r in csv.DictReader(file)]
with sisap_path.open(encoding='utf-8-sig') as file:
    prices=[r for r in csv.DictReader(file) if r['precio_promedio']]
output={'schema_version':1,'scope':'retrospective_context_not_causal_not_model_features','weather':{'location':'Punto Arequipa; no acredita zona productora de los embarques','coordinates':nasa['geometry']['coordinates'],'weekly':weekly,'units':{'T2M_MAX':'°C: media de máximas diarias','T2M_MIN':'°C: media de mínimas diarias','PRECTOTCORR':'mm acumulados en días disponibles','RH2M':'% humedad media'}},'exchange':exchange,'local_prices':prices,'sources':[{'id':'nasa','name':'NASA POWER','url':'https://power.larc.nasa.gov/docs/services/api/temporal/','file':str(nasa_path.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(nasa_path.read_bytes()).hexdigest()},{'id':'bcrp','name':'BCRP PN01207PM','url':'https://estadisticas.bcrp.gob.pe/estadisticas/series/PN01207PM/html','file':str(bcrp_path.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(bcrp_path.read_bytes()).hexdigest()},{'id':'sisap','name':'SISAP / MIDAGRI','url':'http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/consultar/','file':str(sisap_path.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(sisap_path.read_bytes()).hexdigest()}]}
target=Path(os.environ.get('RESEARCH_CONTEXT_OUTPUT',ROOT/'sistema-web-agro/frontend/public/research/interpretation-context.json'))
target.write_text(json.dumps(output,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print(json.dumps({'weather_weeks':len(weekly),'exchange_months':len(exchange),'local_prices':len(prices)}))
