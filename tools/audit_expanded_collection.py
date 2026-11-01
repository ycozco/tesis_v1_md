"""Portable stdlib-only coverage audit; never trains or consults test errors."""
import csv
from collections import defaultdict
from datetime import datetime, timedelta
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pipeline.research.methodology import candidate_grid


def main():
    base = ROOT / 'datasets/fuentes/2026-11-01-expansion'
    out = ROOT / 'planificacion/2026-11-01/ejecucion'
    out.mkdir(parents=True, exist_ok=True)
    cells = defaultdict(lambda: [Decimal(0), Decimal(0), 0])
    source = base / 'conciliacion/vista-conciliada.csv'
    with source.open(encoding='utf-8', newline='') as handle:
        for row in csv.DictReader(handle):
            day = datetime.strptime(row['fecha_embarque_raw'], '%Y%m%d').date()
            week = day - timedelta(days=day.weekday())
            cell = cells[(row['producto'], row['destino'], week)]
            cell[0] += Decimal(row['valor_fob_usd'])
            cell[1] += Decimal(row['peso_neto_kg'])
            cell[2] += 1
    series = defaultdict(list)
    for product, destination, week in cells:
        series[(product, destination)].append(week)
    with (out / 'cobertura-expansion.csv').open('w', encoding='utf-8', newline='') as handle:
        writer = csv.writer(handle)
        writer.writerow(['producto', 'destino', 'inicio', 'fin', 'semanas_observadas',
                         'semanas_rejilla', 'semanas_sin_evidencia', 'cobertura_certificada'])
        for (product, destination), weeks in sorted(series.items()):
            size = (max(weeks)-min(weeks)).days//7+1
            writer.writerow([product, destination, min(weeks), max(weeks), len(weeks),
                             size, size-len(weeks), False])
    summary = json.loads((base/'conciliacion/resumen.json').read_text(encoding='utf-8'))
    original = ROOT/'datasets/fuentes/2026-10-31/observaciones-sunat.csv'
    assert hashlib.sha256(original.read_bytes()).hexdigest() == '63b7fb27162d43b155648fa3af92c24fcfb073b597e7bd12eb80fa5b77b4ea3d'
    audit = {'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
             'source_rows': summary['filas_conciliadas'], 'previous_rows': 93225,
             'net_additional_rows': summary['filas_conciliadas']-93225,
             'quarantine_rows': summary['filas_cuarentena'],
             'series': len(series), 'observed_week_cells': len(cells),
             'complete_week_certificates': 0, 'publication_vintage_certificates': 0,
             'final_test_authorized': False, 'models_run': False,
             'coverage_states': {'observed_partial': 'operation recovered, completeness unknown',
               'certified_no_operations': 'requires explicit coverage certificate; none recovered',
               'missing_incomplete': 'NA; never inferred zero',
               'not_yet_observable': 'requires evidenced publication date; unknown is not eligible'},
             'prior_exposure': ['Actual targets have been plotted in UI',
                               'Pilot H4 examples include proposed reserved weeks'],
             'final_gate': ['Certify coverage or document a methodological reformulation',
                            'Establish availability policy and historical limitations',
                            'Freeze calendar, common universe, parameters and exposure declaration before test errors'],
             'context_features': {name: {'eligible_historical_asof': False, 'reason': reason}
                 for name, reason in {'BCRP': 'No certified publication vintages',
                   'SISAP': 'Commercial level and units not certified compatible',
                   'NASA_POWER': 'Single Arequipa point is not certified production origin',
                   'Comtrade': 'One sample is not a continuous contextual series'}.items()}}
    (out/'auditoria-expansion.json').write_text(json.dumps(audit, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    (out/'grid-candidatos.json').write_text(json.dumps(candidate_grid(), indent=2)+'\n', encoding='utf-8')
    print(json.dumps(audit, ensure_ascii=True))


if __name__ == '__main__':
    main()
