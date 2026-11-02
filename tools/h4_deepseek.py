"""Configure/check offline; --calibrate is an explicit paid neutral probe.

Does not execute the 180 H4 slots. Human keys, retrieval and freeze remain gates.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from pipeline.research.deepseek_h4 import DEFAULTS,DeepSeekH4Transport,H4TransportError


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    action=parser.add_mutually_exclusive_group()
    action.add_argument('--init',action='store_true')
    action.add_argument('--check',action='store_true')
    action.add_argument('--calibrate',action='store_true',help='Paid neutral call within configured ledger; never executed by --check')
    args=parser.parse_args()
    private=ROOT/'data/h4-deepseek';private.mkdir(parents=True,exist_ok=True)
    path=private/'config.json'
    if args.init and not path.exists():
        path.write_text(json.dumps(DEFAULTS,indent=2)+'\n',encoding='utf-8')
    if not path.is_file():
        print(json.dumps({'status':'not_configured','next':'Run --init or tools/configure_h4_deepseek.ps1. No network call.'}));return 2
    settings=json.loads(path.read_text(encoding='utf-8-sig'))
    try:
        transport=DeepSeekH4Transport(settings,private/'budget-ledger.json')
        if args.calibrate:
            metadata=transport.calibrate()
            settings['expected_system_fingerprint']=metadata['system_fingerprint']
            settings['expected_returned_model']=metadata['model']
            path.write_text(json.dumps(settings,indent=2)+'\n',encoding='utf-8')
            (private/'calibration.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
            print(json.dumps({'status':'calibrated_paid_probe','metadata':metadata,'H4_slots_executed':0}))
        else:
            print(json.dumps({'status':'offline_check_only',**transport.status(),
                'H4_final_run_ready':False,'pending':['Human key review','Undefined-rate policy review','Verified retrieval and experimental freeze']}))
    except H4TransportError as error:
        print(json.dumps({'status':'not_ready','reason':str(error),'key_value_disclosed':False}));return 2
    return 0


if __name__=='__main__':raise SystemExit(main())
