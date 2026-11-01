"""Final technical verification, not final experimental evaluation.

No paid providers, historical model training or reserved test predictions.
Legacy artifacts are checked only when explicitly supplied via the CLI.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy-gold-dir')
    arguments = parser.parse_args()
    out = ROOT/'planificacion/2026-11-01/ejecucion/verificacion-final'
    runtime = ROOT/'data/final-verification'
    out.mkdir(parents=True, exist_ok=True)
    runtime.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONPATH=str(ROOT), PYTHONIOENCODING='utf-8',
               DATABASE_URL='sqlite+pysqlite:///:memory:',
               SECRET_KEY='ArtificialFinalVerificationSigningKey2026Only',
               RESEARCH_ALLOW_PAID_AI='false', RESEARCH_ALLOW_LOCAL_AI='false',
               RESEARCH_DEEPSEEK_API_KEY='')
    python = [sys.executable, '-B']
    records = []

    def run(name, command, cwd=ROOT, allowed=(0,), junit=None):
        result = subprocess.run(command, cwd=cwd, env=env, capture_output=True,
                                text=True, encoding='utf-8', errors='replace')
        record = {'name': name, 'exit_code': result.returncode,
                  'passed': result.returncode in allowed,
                  'stdout': result.stdout.strip(), 'stderr': result.stderr.strip()}
        if junit and junit.is_file():
            tree = ET.parse(junit)
            suites = list(tree.getroot().iter('testsuite'))
            record['tests'] = {key: sum(int(s.get(key, 0)) for s in suites)
                               for key in ('tests','failures','errors','skipped')}
            shutil.copyfile(junit, out/(name+'.xml'))
        records.append(record)
        print(json.dumps({'name':name,'passed':record['passed'],'exit_code':result.returncode,
                          'tests':record.get('tests')}),flush=True)

    core = runtime/'current.xml'
    run('current_protocol_and_components', [*python,'-m','pytest','tests/unit','tests/reporting',
         'tests/end_to_end/test_current_research.py','-q','--junitxml='+str(core)], junit=core)
    api = runtime/'api-final.xml'
    # Empty working directory prevents loading the user's .env. Real credentials
    # and databases are neither required nor used by these isolated tests.
    run('isolated_api', [*python,'-m','pytest',str(ROOT/'sistema-web-agro/backend/tests'),
         '-q','--junitxml='+str(api)], cwd=runtime, junit=api)
    run('scientific_compatibility', [*python,'tools/verify_clean_research_environment.py',
         '--output-dir',str(out.relative_to(ROOT))])
    run('expanded_data_integrity', [*python,'tools/verify_expanded_research_data.py'])
    run('ui_snapshot_integrity', [*python,'tools/verify_research_ui.py'])
    npm = shutil.which('npm.cmd') or shutil.which('npm')
    if npm:
        run('frontend_build',[npm,'run','build'],cwd=ROOT/'sistema-web-agro/frontend')
    else:
        records.append({'name':'frontend_build','passed':False,'exit_code':None,'reason':'npm unavailable'})
    if arguments.legacy_gold_dir:
        legacy = Path(arguments.legacy_gold_dir).resolve()
        xml = runtime/'legacy-final.xml'
        run('legacy_artifacts_read_only', [*python,'-m','pytest','tests/data_quality/test_quality.py',
            'tests/leakage/test_leakage.py','tests/end_to_end/test_e2e.py','--legacy-gold-dir',str(legacy),
            '-q','--junitxml='+str(xml)], junit=xml)
        files = [legacy/name for name in ('weekly_product_market.parquet','prediction_features.parquet','traceability_log.json')]
        (out/'legacy-source-fingerprints.json').write_text(json.dumps({str(p):{
            'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in files if p.is_file()},indent=2)+'\n',encoding='utf-8')
    preflight = out/'preflight-final.json'
    run('experimental_preflight', [*python,'tools/check_final_experiment.py',
         '--output',str(preflight.relative_to(ROOT))], allowed=(0,2))
    scientific = json.loads(preflight.read_text(encoding='utf-8')) if preflight.is_file() else None
    current_tests = [r for r in records if r['name'] in {'current_protocol_and_components','isolated_api'}]
    report = {'status':'technical_verification_passed_experiment_not_ready' if all(r['passed'] for r in records)
                 else 'technical_verification_failed',
              'python':sys.version.split()[0],
              'scope':'Current component/API checks, compatibility, build and data integrity. Not a browser usability study or final historical experiment.',
              'current_tests':{key:sum(r.get('tests',{}).get(key,0) for r in current_tests)
                               for key in ('tests','failures','errors','skipped')},
              'legacy_release_checked_separately':bool(arguments.legacy_gold_dir),
              'scientific_blockers':scientific['blockers'] if scientific else [{'code':'preflight_unavailable'}],
              'final_historical_test_executed':False,'h4_generated_outputs':0,'paid_provider_calls':0,
              'checks':records}
    (out/'results.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('status','current_tests','final_historical_test_executed')}))
    return 0 if all(r['passed'] for r in records) else 1


if __name__=='__main__':
    raise SystemExit(main())
