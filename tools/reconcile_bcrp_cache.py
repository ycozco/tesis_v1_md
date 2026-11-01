"""Reconcile two physical BCRP backups, keeping publication eligibility false."""
import hashlib
import json
from pathlib import Path
import shutil
import pandas as pd

OUT = Path(__file__).resolve().parents[1]/'datasets/tratamiento/2026-11-01'


def main():
    source = Path('D:/tesis_yoset/data/downloads/bcrp_tipo_cambio.csv')
    recovered = pd.read_csv(OUT/'bcrp-mensual-recuperado.csv')
    old = pd.read_csv(source)
    months = dict(zip(['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'],range(1,13)))
    matches, added = [], []
    records = recovered.to_dict('records')
    existing = {r['month']:r for r in records}
    for row in old.itertuples():
        month, year = row.fecha_periodo.split('.')
        key = f'{year}-{months[month]:02}'
        if key in existing:
            if abs(existing[key]['pen_per_usd']-row.tipo_cambio_pen_usd)>1e-10:
                raise ValueError('Conflicting backups; no automatic merge')
            matches.append(key)
        else:
            records.append({'month':key,'pen_per_usd':row.tipo_cambio_pen_usd,'published_at':None,
                            'eligible_asof':False,'source':'local_BCRP_CSV_backup'})
            added.append(key)
    shutil.copyfile(source,OUT/'bcrp-csv-respaldo-original.csv')
    pd.DataFrame(records).sort_values('month').to_csv(OUT/'bcrp-mensual-conciliado.csv',index=False)
    report = {'shared_months_matching':matches,'added_from_csv':added,'total_months':len(records),
        'csv_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'status':'local_backup_reconciliation_not_fresh_remote_verification',
        'publication_dates':'unknown','eligible_asof':False}
    (OUT/'bcrp-conciliacion.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))


if __name__=='__main__':main()
