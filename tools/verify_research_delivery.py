"""Independent artifact checks and real FastAPI read-only endpoint exercise.

API supplemental packages live in ignored data/runtime-api; no production DB used.
"""
import importlib.metadata as metadata
import json
import os
from pathlib import Path
import sys
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'datasets/tratamiento/2026-11-01'


def main():
    checks = {}
    for view in ['conservadora','sensibilidad']:
        source = ROOT/'datasets/fuentes/2026-10-31/conciliacion'
        source = source/'vista-conciliada.csv' if view=='conservadora' else source/'resolucion-analitica/vista-resuelta-analitica.csv'
        rows = pd.read_csv(source)
        dates = pd.to_datetime(rows.fecha_embarque_raw.astype(str),format='%Y%m%d')
        rows['week'] = dates - pd.to_timedelta(dates.dt.dayofweek,unit='D')
        expected = rows.groupby(['producto','destino','week'])[['valor_fob_usd','peso_neto_kg']].sum()
        panel = pd.read_parquet(OUT/f'panel-{view}.parquet')
        observed = panel.dropna(subset=['unit_fob']).set_index(['producto','destino','week']).sort_index()
        expected = expected.sort_index()
        assert np.allclose(observed.unit_fob, expected.valor_fob_usd/expected.peso_neto_kg)
        assert np.allclose(observed.volume_kg, expected.peso_neto_kg)
        assert panel.loc[panel.coverage_state=='unknown','volume_kg'].isna().all()
        assert not panel.duplicated(['producto','destino','week']).any()
        checks[view] = {'ratio_of_sums_verified':True,'unknown_not_zero':True,'unique_cells':True}
    pred = pd.read_parquet(OUT/'predicciones-desarrollo-piloto.parquet')
    calendar = pd.read_csv(OUT/'calendario-provisional.csv',parse_dates=['target_week'])
    reserved = set(calendar.loc[calendar.split=='reserved_test_NOT_RUN','target_week'])
    assert not set(pred.target_week)&reserved
    assert (pred.emission == pred.target_week).all()
    checks['reserved_test_not_predicted'] = True
    intervals = pd.read_parquet(OUT/'estado-intervalos-piloto.parquet')
    assert not ((intervals.past_errors<40)&intervals.lower.notna()).any()
    checks['no_intervals_under_40_errors'] = True
    cases = json.loads((OUT/'h4-casos-30.json').read_text())
    slots = json.loads((OUT/'h4-plan-180.json').read_text())
    assert len(cases)==30 and len(slots)==180
    assert len({(r['case_id'],r['configuration'],r['run']) for r in slots})==180
    assert all(r['output'] is None and r['status']=='not_executed' for r in slots)
    panel = pd.read_parquet(OUT/'panel-conservadora.parquet')
    for case in cases:
        reference = panel[(panel.producto==case['producto']) & (panel.destino==case['destino'])
                          & (panel.week==pd.Timestamp(case['week']))]
        assert len(reference)==1
        for name, fact in case['evidence'].items():
            field = name.split('.')[-1]
            assert abs(fact['value'] - float(reference.iloc[0][field])) < 1e-9
    checks['h4_30_cases_180_unique_unexecuted_slots'] = True
    runtime = ROOT/'data/runtime-api'
    checks['api'] = {'status':'not_installed'}
    if runtime.exists():
        try:
            sys.path.insert(0,str(runtime))
            sys.path.insert(1,str(ROOT/'sistema-web-agro/backend'))
            os.environ['DATABASE_URL']='sqlite+pysqlite:///:memory:'
            from fastapi.testclient import TestClient
            from app_fastapi.main import app
            with TestClient(app) as client:
                health = client.get('/health')
                migration = client.get('/api/migration/status')
                assert health.status_code==200 and health.json()['framework']=='FastAPI'
                assert migration.status_code==200
            installed = {d.metadata['Name']:d.version for d in metadata.distributions(path=[str(runtime)])}
            (OUT/'environment-api-observed.json').write_text(json.dumps(installed,indent=2),encoding='utf-8')
            checks['api']={'status':'passed','endpoints':['GET /health','GET /api/migration/status'],
                'database':'isolated SQLite in memory; NOT PostgreSQL or pgvector validation',
                'not_checked':['authentication','dashboard database data','Uvicorn network server']}
        except Exception as error:
            # Validation exceptions can include environment values; never publish those.
            checks['api']={'status':'failed','error_type':type(error).__name__,
                           'detail':'Endpoint verification failed; environment values omitted.'}
    (OUT/'verificacion-entrega.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
    print(json.dumps(checks))
    if checks['api']['status']=='failed': raise SystemExit(1)


if __name__=='__main__': main()
