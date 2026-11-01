"""Build a non-executed H4 design without providers or historical personal data."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from pipeline.research.h4_design import build_design, digest


def main():
    out = ROOT / 'datasets/experimentos/h4-controlado-v1'
    out.mkdir(parents=True, exist_ok=True)
    design = build_design()
    for name, content in design.items():
        (out/(name+'.json')).write_text(json.dumps(content, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    manifest = {'status': 'prepared_not_executed_not_human_reviewed',
                'thesis_reference': '3.9.5.1; planificacion/2026-11-01/fundamento-tesis.json T07',
                'data_kind': 'artificial_controlled_cases_not_forecast_history',
                'cases': len(design['cases']), 'slots': len(design['schedule']),
                'outputs_generated': 0, 'design_sha256': digest(design),
                'generator_frozen': False, 'calls_to_local_or_paid_providers': 0,
                'pilot_catalogue_superseded_for_final_H4': 'datasets/tratamiento/2026-11-01/h4-casos-30.json',
                'pending': ['Human review of factual keys and abstention coverage policy',
                            'Freeze generator, prompt, corpus, retrieval and correction settings',
                            'Implement and verify paired runner and blind grading',
                            'Execute 180 paired outputs and aggregate repetitions within case first']}
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(json.dumps(manifest))


if __name__ == '__main__':
    main()
