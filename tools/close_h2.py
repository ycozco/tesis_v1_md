"""One-pass H2 closure for this exact source release; never manufactures metrics.

Audits source eligibility and every common-calendar origin/L/target/family cell.
The thesis explicitly permits a documented not-evaluable conclusion (H2/T02).
"""
import csv
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from pipeline.research.h2 import decide_h2


def main():
    import pandas as pd
    out=ROOT/'datasets/experimentos/h2-cierre-2026-11-01'
    out.mkdir(parents=True,exist_ok=True)
    hashes={}
    def path(relative):
        p=ROOT/relative
        hashes[relative]=hashlib.sha256(p.read_bytes()).hexdigest()
        return p
    def read(relative):
        return json.loads(path(relative).read_text(encoding='utf-8'))
    def rows(relative):
        with path(relative).open(encoding='utf-8',newline='') as handle:
            return list(csv.DictReader(handle))
    foundation=read('planificacion/2026-11-01/fundamento-tesis.json')
    h2_text=next(a['excerpt'] for a in foundation['anchors'] if a['id']=='T02')
    assert 'no pudo evaluarse' in h2_text
    bcrp=rows('datasets/tratamiento/2026-11-01/bcrp-mensual-conciliado.csv')
    assert hashes['datasets/tratamiento/2026-11-01/bcrp-mensual-conciliado.csv']=='bc020972a7adc97580b3d359934fe24f417cfa059e4f28a482952e818a1af39e'
    candidates=read('datasets/contexto/h2-bcrp-2026-11-01/documentary-candidates.json')
    bcrp_audit=read('datasets/contexto/h2-bcrp-2026-11-01/independent-audit.json')
    assert bcrp_audit['original_pdfs_verified']==0
    assert all(not row['published_at'] and row['eligible_asof'].lower()=='false' for row in bcrp)
    assert all(row['verified_available_at'] is None and not row['eligible_asof'] for row in candidates['observations'])
    sisap=rows('datasets/tratamiento/2026-11-01/contexto/sisap-mensual-normalizado.csv')
    assert all(not row['publicado_en'] and row['eligible_asof'].lower()=='false' for row in sisap)
    assert all(row['unidad_especifica_validada'].lower()=='false' for row in sisap)
    nasa=read('datasets/tratamiento/2026-11-01/contexto/nasa-arequipa-contexto-2018-2026.json')
    retrieval=read('datasets/tratamiento/2026-11-01/contexto/manifest-recuperacion.json')
    nasa_entry=next(r for r in retrieval if r['name']=='nasa-arequipa-contexto-2018-2026')
    assert nasa_entry['eligible_asof'] is False
    assert nasa_entry['sha256']==hashes['datasets/tratamiento/2026-11-01/contexto/nasa-arequipa-contexto-2018-2026.json']
    comtrade=read('datasets/fuentes/2026-10-31/muestras-contextuales/comtrade-muestra.json')
    assert len(comtrade['data'])==1
    inventory=[
        {'source':'BCRP','role':'monthly_macro_covariate_not_a_FOB_replacement','observations':len(bcrp),
         'documentary_candidates':len(candidates['observations']),'verified_eligible_rows':0,
         'reasons':['publication_vintages_not_verified','dated_index_transcriptions_not_original_PDFs'],
         'not_a_reason_for_exclusion':'Monthly frequency can be aligned as-of with evidenced release dates and age.'},
        {'source':'SISAP','role':'domestic_wholesale_proxy_requiring_explicit_interpretation',
         'observations':len(sisap),'numeric_observations':sum(bool(row['precio_promedio']) for row in sisap),
         'verified_eligible_rows':0,'reasons':['specific_price_units_unverified','historical_publication_dates_missing','proxy_interpretation_not_validated'],
         'not_a_reason_for_exclusion':'A domestic price need not equal FOB to be a contextual covariate.'},
        {'source':'NASA_POWER','role':'climate_context_requiring_origin_mapping_or_justified_proxy',
         'observations_per_parameter':{name:len(values) for name,values in nasa['properties']['parameter'].items()},
         'coordinates':nasa['geometry']['coordinates'],'verified_eligible_rows':0,
         'reasons':['production_origin_or_proxy_mapping_not_verified','historical_publication_vintages_missing']},
        {'source':'Comtrade','role':'international_trade_covariate_requiring_series_and_release_history',
         'observations':len(comtrade['data']),'verified_eligible_rows':0,
         'reasons':['single_sample_not_continuous_context_series','historical_publication_versions_missing']}]
    panel_path=path('datasets/tratamiento/2026-11-01-expansion/panel-conservadora.parquet')
    panel=pd.read_parquet(panel_path,columns=['producto','destino','week','coverage_certified','published_at','eligible_historical_asof'])
    assert not panel.coverage_certified.any() and panel.published_at.isna().all()
    assert not panel.eligible_historical_asof.any()
    calendar=rows('datasets/tratamiento/2026-11-01-expansion/calendario-provisional.csv')
    assert len(calendar)==52 and len({r['emission'] for r in calendar})==52
    matrix=[]
    # Origins are date labels here, not asserted UTC release timestamps. Since no
    # source has a verified publication clock, no value is joined or backfilled.
    for origin in calendar:
        for embargo in (0,4,8):
            for target in ('unit_fob','volume_kg'):
                for source in inventory:
                    matrix.append({'emission_date':origin['emission'],'target_week':origin['target_week'],
                        'split':origin['split'],'L':embargo,'target':target,'source':source['source'],
                        'verified_context_rows':0,'verified_target_rows':0,'eligible_paired_cases':0,
                        'status':'not_evaluable_missing_verified_availability_and_coverage'})
    with (out/'origin-eligibility.csv').open('w',encoding='utf-8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(matrix[0]));writer.writeheader();writer.writerows(matrix)
    decision=decide_h2(inventory,0,0)
    decision.update({'scope':'exact_source_release_identified_by_evidence_sha256',
        'thesis_source':foundation['source'],'thesis_anchor':'T02 / 1.4.3 H2',
        'closed_analysis_not_confirmed_hypothesis':True,'source_families_audited':4,
        'calendar_origins':52,'availability_sensitivities':[0,4,8],'targets':['unit_fob','volume_kg'],
        'origin_source_target_L_checks':len(matrix),'target_panel_cells_audited':len(panel),
        'evidence_sha256':hashes,'final_test_predictions_generated':0,
        'models_fitted':0,'reopen_only_if':'New source evidence or a reviewed protocol amendment changes eligibility; regenerate this audit before any outcome evaluation.'})
    assert len(matrix)==1248
    for name,content in [('source-inventory.json',inventory),('decision.json',decision)]:
        (out/name).write_text(json.dumps(content,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({key:decision[key] for key in ('status','eligible_context_families','calendar_origins','origin_source_target_L_checks','models_fitted','supports_h2','refutes_h2')}))


if __name__=='__main__':main()
