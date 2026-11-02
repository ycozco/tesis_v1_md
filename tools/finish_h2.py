"""Complete H2 source audit, independent contrast and regression in one command.

The current source release closes as NOT EVALUABLE under thesis H2/T02.
This does not claim H2 confirmation, refutation, or invented model metrics.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'datasets/experimentos/h2-cierre-2026-11-01'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--legacy-gold-dir',help='Optional separate read-only legacy release')
    args=parser.parse_args()
    final=['tools/run_final_verification.py']
    if args.legacy_gold_dir:final += ['--legacy-gold-dir',args.legacy_gold_dir]
    steps=[['tools/verify_h2_bcrp.py'],['tools/close_h2.py'],['tools/verify_h2_closure.py'],
        ['-m','pytest','tests/unit/test_final_preflight.py','tests/unit/test_h2_bcrp.py',
         'tests/unit/test_h2_closure.py','-q'],final]
    records=[]
    for command in steps:
        result=subprocess.run([sys.executable,'-B',*command],cwd=ROOT,capture_output=True,
            text=True,encoding='utf-8',errors='replace')
        records.append({'command':command,'exit_code':result.returncode,
            'stdout':result.stdout.strip(),'stderr':result.stderr.strip()})
        print(json.dumps({'step':command[0],'exit_code':result.returncode}),flush=True)
        if result.returncode:break
    success=len(records)==len(steps) and all(record['exit_code']==0 for record in records)
    report={'status':'closed_not_evaluable_current_release' if success else 'closure_verification_failed',
        'scope':'Exact audited release. Hypothesis neither supported nor refuted.',
        'final_reserved_predictions_generated':0,'paid_provider_calls':0,'steps':records,
        'code_hash_convention':'UTF-8 text with universal newlines normalized to LF',
        'code_sha256':{str(path.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(path.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
            for path in [ROOT/'tools/finish_h2.py',ROOT/'tools/close_h2.py',ROOT/'tools/verify_h2_closure.py',
                         ROOT/'tools/verify_h2_bcrp.py',ROOT/'pipeline/research/h2.py',ROOT/'tools/check_final_experiment.py']}}
    BASE.mkdir(parents=True,exist_ok=True)
    (BASE/'one-pass-run.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'status':report['status']}))
    return 0 if success else 1


if __name__=='__main__':raise SystemExit(main())
