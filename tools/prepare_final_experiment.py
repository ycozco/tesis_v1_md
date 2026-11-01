"""One preparation command; never evaluates the reserved final block.

Exit 0: preparation passed, scientific prerequisites still require review.
Exit 1: preparation failure. Exit 2: preparation passed, preflight has blockers.
Run with the isolated scientific environment described in the delivery guide.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TESTS = ['tests/unit/test_temporal_ledger.py', 'tests/unit/test_final_preflight.py',
         'tests/unit/test_h3_rules.py', 'tests/unit/test_h4_design.py',
         'tests/unit/test_methodology.py', 'tests/unit/test_research_protocol.py',
         'tests/reporting/test_reports.py']


def main():
    if sys.prefix == sys.base_prefix:
        raise SystemExit('Use an isolated virtual environment; no package installation is performed here.')
    out = ROOT/'planificacion/2026-11-01/ejecucion'
    out.mkdir(parents=True, exist_ok=True)
    steps = [('clean_environment', ['tools/verify_clean_research_environment.py']),
             ('expanded_features', ['tools/build_expanded_research_data.py']),
             ('independent_data_check', ['tools/verify_expanded_research_data.py']),
             ('protocol_tests', ['-m', 'pytest', *TESTS, '-q']),
             ('scientific_preflight', ['tools/check_final_experiment.py'])]
    records = []
    for name, arguments in steps:
        result = subprocess.run([sys.executable, '-B', *arguments], cwd=ROOT,
                                capture_output=True, text=True, encoding='utf-8', errors='replace')
        allowed = result.returncode == 0 or (name == 'scientific_preflight' and result.returncode == 2)
        records.append({'step': name, 'arguments': arguments, 'exit_code': result.returncode,
                        'technical_execution_passed': allowed,
                        'stdout': result.stdout.strip(), 'stderr': result.stderr.strip()})
        print(json.dumps({'step': name, 'exit_code': result.returncode, 'technical_execution_passed': allowed}), flush=True)
        if not allowed:
            break
    paths = [ROOT/'tools/prepare_final_experiment.py']
    paths += [ROOT/arguments[0] for _, arguments in steps if arguments[0].endswith('.py')]
    paths += list((ROOT/'pipeline/research').glob('*.py')) + [ROOT/test for test in TESTS]
    report = {'status': 'preparation_passed_final_blocked' if len(records) == len(steps)
                 and all(r['technical_execution_passed'] for r in records) and records[-1]['exit_code'] == 2
                 else 'preparation_passed_requires_protocol_review' if len(records) == len(steps)
                 and all(r['technical_execution_passed'] for r in records) else 'preparation_failed',
              'final_test_executed': False, 'paid_ai_calls': 0,
              'code_hash_convention': 'SHA-256 of UTF-8 text with universal newlines normalized to LF',
              'executed_code_sha256': {str(p.relative_to(ROOT)).replace('\\','/'): hashlib.sha256(p.read_text(encoding='utf-8').encode('utf-8')).hexdigest() for p in paths},
              'steps': records}
    (out/'preparation-run.json').write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    return 1 if report['status'] == 'preparation_failed' else 2 if report['status'] == 'preparation_passed_final_blocked' else 0


if __name__ == '__main__':
    raise SystemExit(main())
