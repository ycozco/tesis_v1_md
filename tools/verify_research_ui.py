"""Independently compare the public UI snapshot with its source artifacts."""
import hashlib
import json
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'datasets/tratamiento/2026-11-01'


def main():
    snapshot=ROOT/'sistema-web-agro/frontend/public/research/snapshot.json'
    data=json.loads(snapshot.read_text(encoding='utf8'))
    assert data['schema_version']==1 and data['test_executed'] is False
    for name,expected in data['artifact_hashes'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected
    ui=pd.DataFrame(data['weekly_rows'],columns=data['weekly_columns'])
    original=pd.read_parquet(BASE/'panel-conservadora.parquet')
    assert len(ui)==len(original)==14683
    assert int(ui.unit_fob.notna().sum())==3268
    assert int(ui.unit_fob.isna().sum())==11415
    left=ui.set_index(['product','destination','week']).sort_index()
    original['week']=original.week.dt.strftime('%Y-%m-%d')
    right=original.set_index(['producto','destino','week']).sort_index()
    for column in ('unit_fob','volume_kg','fob_usd'):
        pd.testing.assert_series_equal(left[column],right[column],check_names=False)
    metrics=pd.read_csv(BASE/'metricas-emparejadas-piloto.csv')
    metrics=metrics[(metrics.view=='conservadora')&(metrics.L==0)]
    assert len(data['paired_metrics'])==len(metrics)
    for record,reference in zip(data['paired_metrics'],metrics.to_dict('records')):
        for key in ['model','target','reference','n_paired']:assert record[key]==reference[key]
        for key in ['model_macro_mae','reference_macro_mae']:assert abs(record[key]-reference[key])<1e-7
    search=json.loads((ROOT/'datasets/busqueda/2026-11-01/manifest-busqueda.json').read_text())
    assert data['pending_search']['candidate_rows']==search['candidate_rows']==8579
    assert data['h4']['h4_outputs_generated']==0
    print(json.dumps({'status':'passed','weekly_rows':len(ui),'observed_cells':3268,'unknown_cells':11415,
                      'source_hashes_verified':len(data['artifact_hashes']),'new_candidates_not_in_panel':True,
                      'paired_metrics_verified':len(metrics)}))


if __name__=='__main__':main()
