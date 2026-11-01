"""Rebuild expanded retrospective features; no calendar change or model fitting."""
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    import pandas as pd
    from pipeline.research.protocol import weekly_panel, feature_table

    source = ROOT/'datasets/fuentes/2026-11-01-expansion/conciliacion/vista-conciliada.csv'
    calendar = ROOT/'datasets/tratamiento/2026-11-01/calendario-provisional.csv'
    out = ROOT/'datasets/tratamiento/2026-11-01-expansion'
    out.mkdir(parents=True, exist_ok=True)
    rows = pd.read_csv(source, dtype=str)
    panel = weekly_panel(rows)
    panel['coverage_certified'] = False
    panel['published_at'] = pd.NaT
    panel['eligible_historical_asof'] = False
    panel.to_parquet(out/'panel-conservadora.parquet', index=False)
    outputs = ['panel-conservadora.parquet']
    for embargo in (0, 4, 8):
        features = feature_table(panel, embargo)
        features['target_published_at'] = pd.NaT
        features['eligible_for_final_experiment'] = False
        name = f'features-conservadora-L{embargo}.parquet'
        features.to_parquet(out/name, index=False)
        outputs.append(name)
    shutil.copyfile(calendar, out/'calendario-provisional.csv')
    outputs.append('calendario-provisional.csv')
    manifest = {'status': 'expanded_retrospective_preprocessing_only_not_model_ready',
                'views': {'conservadora': {'input_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                    'rows': len(rows), 'series': len(panel.groupby(['producto','destino'])),
                    'observed_cells': int(panel.unit_fob.notna().sum()), 'grid_cells': len(panel),
                    'unknown_cells': int(panel.unit_fob.isna().sum())}},
                'publication_policy': 'unknown_not_imputed',
                'eligible_final_rows': 0, 'model_fitting_executed': False, 'final_test_executed': False,
                'calendar': {'copied_from': str(calendar.relative_to(ROOT)).replace('\\','/'),
                    'sha256': hashlib.sha256(calendar.read_bytes()).hexdigest(),
                    'requires_pretest_protocol_freeze': True, 'calendar_changed': False},
                'feature_rules': 'Legacy pilot lag features; final baseline rules and availability filtering must be integrated in final runner.',
                'sensitivity': 'Not mixed with the previous release; expanded heuristic sensitivity has not been reconstructed.',
                'outputs_sha256': {name: hashlib.sha256((out/name).read_bytes()).hexdigest() for name in outputs}}
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(json.dumps(manifest, ensure_ascii=True))


if __name__ == '__main__':
    main()
