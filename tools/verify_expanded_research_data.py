"""Independent Decimal aggregation checks against expanded Parquet artefacts."""
import csv
from collections import defaultdict
from datetime import datetime, timedelta
from decimal import Decimal
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    import pandas as pd
    out = ROOT/'datasets/tratamiento/2026-11-01-expansion'
    source = ROOT/'datasets/fuentes/2026-11-01-expansion/conciliacion/vista-conciliada.csv'
    manifest = json.loads((out/'manifest.json').read_text(encoding='utf-8'))
    assert hashlib.sha256(source.read_bytes()).hexdigest() == manifest['views']['conservadora']['input_sha256']
    totals = defaultdict(lambda: [Decimal(0), Decimal(0)])
    with source.open(encoding='utf-8', newline='') as handle:
        for row in csv.DictReader(handle):
            day = datetime.strptime(row['fecha_embarque_raw'], '%Y%m%d').date()
            week = day-timedelta(days=day.weekday())
            cell = totals[(row['producto'],row['destino'],week)]
            cell[0] += Decimal(row['valor_fob_usd'])
            cell[1] += Decimal(row['peso_neto_kg'])
    panel = pd.read_parquet(out/'panel-conservadora.parquet')
    assert not panel.duplicated(['producto','destino','week']).any()
    observed = panel[panel.coverage_state == 'observed_partial']
    assert len(observed) == len(totals)
    for row in observed.itertuples():
        fob, weight = totals[(row.producto,row.destino,row.week.date())]
        for actual, expected in ((row.fob_usd,fob),(row.volume_kg,weight),(row.unit_fob,fob/weight)):
            assert abs(actual-float(expected)) <= max(1.,abs(float(expected)))*1e-12
    unknown = panel[panel.coverage_state == 'unknown']
    assert unknown[['fob_usd','volume_kg','unit_fob']].isna().all().all()
    assert panel.published_at.isna().all() and not panel.eligible_historical_asof.any()
    assert not panel.coverage_certified.any()
    for embargo in (0,4,8):
        features = pd.read_parquet(out/f'features-conservadora-L{embargo}.parquet')
        assert len(features) == len(panel)
        assert features.target_published_at.isna().all()
        assert not features.eligible_for_final_experiment.any()
        assert (features.embargo_weeks == embargo).all()
    assert (out/'calendario-provisional.csv').read_bytes() == (ROOT/'datasets/tratamiento/2026-11-01/calendario-provisional.csv').read_bytes()
    for name, expected in manifest['outputs_sha256'].items():
        assert hashlib.sha256((out/name).read_bytes()).hexdigest() == expected
    result = {'status': 'passed', 'source_rows': manifest['views']['conservadora']['rows'],
              'observed_cells_checked_against_decimal_source_totals': len(observed),
              'unknown_cells_preserved': len(unknown), 'publication_dates_not_imputed': True,
              'eligible_final_rows': 0, 'all_output_hashes_verified': True,
              'calendar_identical': True, 'model_fitting_executed': False}
    path = ROOT/'planificacion/2026-11-01/ejecucion/expanded-data-verification.json'
    path.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
