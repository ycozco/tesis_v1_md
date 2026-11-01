"""Export a read-only, provenance-bound UI snapshot from research artifacts."""
import hashlib
import json
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'datasets/tratamiento/2026-11-01'
OUT=ROOT/'sistema-web-agro/frontend/public/research'


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    panel=pd.read_parquet(BASE/'panel-conservadora.parquet')
    rows=[]
    for row in panel.itertuples():
        rows.append([row.producto,row.destino,str(row.week.date()),
            float(row.unit_fob) if pd.notna(row.unit_fob) else None,
            float(row.volume_kg) if pd.notna(row.volume_kg) else None,
            float(row.fob_usd) if pd.notna(row.fob_usd) else None,row.coverage_state])
    metrics=pd.read_csv(BASE/'metricas-emparejadas-piloto.csv')
    metrics=metrics[(metrics.view=='conservadora')&(metrics.L==0)]
    signals=pd.read_csv(BASE/'h3-scores-piloto.csv')
    signals=signals[signals.ensemble_rank_selected][['target','emission','producto','destino','z','common_candidates','K','ensemble_rank']]
    payload={'schema_version':1,'generated_on':'2026-11-01','status':'retrospective_development_pilot',
        'test_executed':False,'manifest':json.loads((BASE/'manifest.json').read_text()),
        'weekly_columns':['product','destination','week','unit_fob','volume_kg','fob_usd','coverage_state'],
        'weekly_rows':rows,'paired_metrics':json.loads(metrics.to_json(orient='records')),
        'signals':json.loads(signals.to_json(orient='records',date_format='iso')),
        'h4':json.loads((BASE/'h3-h4-resumen.json').read_text()),
        'bcrp':json.loads((BASE/'bcrp-conciliacion.json').read_text()),
        'sisap':{k:v for k,v in json.loads((BASE/'contexto/normalizacion-resumen.json').read_text()).items() if k!='sources'},
        'pending_search':json.loads((ROOT/'datasets/busqueda/2026-11-01/manifest-busqueda.json').read_text()),
        'sources':[{'name':'SUNAT / ADUANET','url':'http://www.aduanet.gob.pe/aduanas/informae/presentacion_bases_web.htm'},
                   {'name':'SISAP / MIDAGRI','url':'http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/consultar/'},
                   {'name':'BCRP','url':'https://estadisticas.bcrp.gob.pe/estadisticas/series/'},
                   {'name':'NASA POWER','url':'https://power.larc.nasa.gov/docs/services/api/temporal/'}],
        'artifact_hashes':{str(f.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(f.read_bytes()).hexdigest()
                           for f in [BASE/'manifest.json',BASE/'panel-conservadora.parquet',BASE/'metricas-emparejadas-piloto.csv',BASE/'h3-scores-piloto.csv']}}
    target=OUT/'snapshot.json'
    target.write_text(json.dumps(payload,ensure_ascii=False,allow_nan=False,separators=(',',':')),encoding='utf8')
    print(json.dumps({'file':str(target),'weekly_cells':len(rows),'signals':len(signals),'bytes':target.stat().st_size}))


if __name__=='__main__':main()
