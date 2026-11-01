"""Build audited panels, aligned features and a PROVISIONAL common calendar.

Run from repository: python -B tools/build_research_data.py
Does not invoke the legacy pipeline or update thesis results.
"""
import hashlib
import importlib.metadata as metadata
import json
from pathlib import Path
import platform
import shutil
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pipeline.research.protocol import weekly_panel, feature_table


def main():
    out = ROOT / 'datasets/tratamiento/2026-11-01'
    out.mkdir(parents=True, exist_ok=True)
    base = ROOT / 'datasets/fuentes/2026-10-31/conciliacion'
    inputs = {'conservadora': base / 'vista-conciliada.csv',
              'sensibilidad': base / 'resolucion-analitica/vista-resuelta-analitica.csv'}
    manifest = {'date': '2026-11-01', 'status': 'retrospective_provisional_not_final_experiment',
                'shipment_date': 'FEMB; Monday ISO week; incomplete collection', 'views': {}}
    for name, source in inputs.items():
        rows = pd.read_csv(source, dtype=str)
        panel = weekly_panel(rows)
        panel.to_parquet(out / f'panel-{name}.parquet', index=False)
        flags = rows.copy()
        unit = pd.to_numeric(flags.valor_fob_usd) / pd.to_numeric(flags.peso_neto_kg)
        flags = flags[(unit < .01) | (unit > 100)]
        flags.to_csv(out / f'revision-precios-{name}.csv', index=False)
        coverage = panel.groupby(['producto', 'destino']).agg(
            weeks_grid=('week', 'size'), weeks_observed=('unit_fob', 'count'),
            start=('week', 'min'), end=('week', 'max')).reset_index()
        coverage['coverage_certified'] = False
        coverage.to_csv(out / f'cobertura-{name}.csv', index=False)
        for embargo in (0, 4, 8):
            features = feature_table(panel, embargo)
            features.to_parquet(out / f'features-{name}-L{embargo}.parquet', index=False)
        manifest['views'][name] = {'input_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'rows': len(rows), 'observed_cells': int(panel.unit_fob.notna().sum()),
            'grid_cells': len(panel), 'unknown_cells': int(panel.unit_fob.isna().sum()),
            'price_review_rows': len(flags), 'series': len(coverage)}
    # Calendar uses dates alone, no model error/test outcomes. It is a planning proposal.
    last = panel.week.max()
    test_start = last - pd.Timedelta(weeks=25)
    dev_start = test_start - pd.Timedelta(weeks=26)
    calendar = pd.DataFrame({'target_week': pd.date_range(dev_start, last, freq='W-MON')})
    calendar['split'] = calendar.target_week.map(lambda d: 'reserved_test_NOT_RUN' if d >= test_start else 'development_pilot')
    calendar['emission'] = calendar.target_week  # origin is start of target week
    calendar['approved_final_protocol'] = False
    calendar.to_csv(out / 'calendario-provisional.csv', index=False)
    manifest['calendar'] = {'development_start': str(dev_start.date()), 'test_start': str(test_start.date()),
        'last_target': str(last.date()), 'test_executed': False, 'requires_pretest_protocol_freeze': True,
        'warning': 'Packet end dates are NOT publication dates. No certified as-of reconstruction.'}
    installed = {d.metadata['Name']: d.version for d in metadata.distributions() if d.metadata['Name']}
    (out / 'environment-observed.json').write_text(json.dumps({'python': platform.python_version(),
        'packages': dict(sorted(installed.items())), 'lock_status': 'observed_not_clean_install_verified'}, indent=2), encoding='utf-8')
    # Preserve the exact old source before parsing; its values are not eligible as-of features yet.
    cache = Path('D:/tesis_yoset/data/bcrp/exchange_rates_cache.json')
    if cache.exists():
        shutil.copyfile(cache, out / 'bcrp-cache-recuperada.json')
        raw = json.loads(cache.read_text(encoding='utf-8-sig'))
        months = {'Ene':1, 'Feb':2, 'Mar':3, 'Abr':4, 'May':5, 'Jun':6,
                  'Jul':7, 'Ago':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dic':12}
        records = []
        for period in raw['periods']:
            month, year = period['name'].split('.')
            records.append({'month': f'{year}-{months[month]:02}', 'pen_per_usd': float(period['values'][0]),
                            'published_at': None, 'eligible_asof': False, 'source': 'local_BCRP_cache'})
        pd.DataFrame(records).to_csv(out / 'bcrp-mensual-recuperado.csv', index=False)
        manifest['bcrp'] = {'months': len(records), 'source_sha256': hashlib.sha256(cache.read_bytes()).hexdigest(),
            'description': raw['config'], 'publication_dates': 'unknown_not_imputed',
            'note': 'Not joined to weekly features; cache lacks certified publication/vintage history.'}
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(manifest, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    main()
