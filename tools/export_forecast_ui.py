"""Publish existing pilot forecasts for display; no fitting or final-test execution."""
import hashlib
import json
from pathlib import Path
import pandas as pd

ROOT = Path('/workspace') if Path('/workspace').exists() else Path(__file__).resolve().parents[1]
BASE = ROOT / 'datasets/tratamiento/2026-11-01'
OUT = ROOT / 'sistema-web-agro/frontend/public/research/forecasts.json'

def main():
    hashes = json.loads((BASE/'hashes.json').read_text(encoding='utf-8'))
    sources = {}
    for name in ['predicciones-desarrollo-piloto.parquet', 'estado-intervalos-piloto.parquet']:
        sha = hashlib.sha256((BASE/name).read_bytes()).hexdigest()
        if hashes[name] != sha: raise ValueError('Source integrity failed: ' + name)
        sources[name] = sha
    frame = pd.read_parquet(BASE/'predicciones-desarrollo-piloto.parquet')
    frame = frame[(frame['view']=='conservadora') & (frame.L==0)].copy()
    for col in ['emission', 'target_week']:
        frame[col] = pd.to_datetime(frame[col]).dt.strftime('%Y-%m-%d')
    intervals = pd.read_parquet(BASE/'estado-intervalos-piloto.parquet')
    intervals = intervals[(intervals['view']=='conservadora') & (intervals.L==0)]
    assert not frame.duplicated(['target','method','producto','destino','emission','target_week']).any()
    assert (pd.to_datetime(frame.target_week) - pd.to_datetime(frame.emission)).dt.days.eq(0).all()
    origin = (pd.to_datetime(frame.target_week) - pd.Timedelta(weeks=1)).dt.strftime('%Y-%m-%d')
    frame['origin_week'] = origin
    # The pilot required lag0 to be present. At L=0 it is exactly the origin week.
    frame['last_observed_week'] = origin
    columns = ['producto','destino','target','method','emission','target_week','actual','prediction',
               'origin_week','last_observed_week']
    payload = {'schema_version':2, 'scope':'retrospective_development_pilot', 'view':'conservadora', 'L':0,
        'data_cut':'2026-11-01', 'test_executed':False, 'horizon_weeks':1,
        'emission_kind':'simulated_week_boundary_date', 'source_sha256':sources, 'columns':columns,
        'rows':json.loads(frame[columns].to_json(orient='values')),
        'interval_status':{str(k):int(v) for k,v in intervals.status.value_counts().items()},
        'limits':['Cobertura parcial; disponibilidad histórica no certificada.',
                  'Predicciones de desarrollo a una semana; no son nuevas generaciones ni pronósticos operativos de noviembre.',
                  'No se entrenó ni ejecutó el test final para publicar esta vista.']}
    OUT.write_text(json.dumps(payload,ensure_ascii=False,allow_nan=False,separators=(',',':')),encoding='utf-8')
    print(json.dumps({'rows':len(frame),'first':frame.target_week.min(),'last':frame.target_week.max(),'intervals':payload['interval_status'],'bytes':OUT.stat().st_size}))

if __name__ == '__main__': main()
