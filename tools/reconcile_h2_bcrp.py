"""Compare local BCRP backup with documentary candidates, without certifying vintages.

Table facts transcribed from indexed official documents; original PDF downloads
were HTML responses. Indexed transcription is NOT an authenticated PDF vintage.
"""
import argparse
import calendar
import csv
from datetime import date, datetime, timezone
from decimal import Decimal
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'datasets/contexto/h2-bcrp-2026-11-01'
# Interbank average, third column after bid and ask, table 36. May-to-date
# values are excluded. Only the unambiguous Jan 2025–April 2026 block is used;
# older rows and intervening annual summaries are not inferred from flattened text.
MONTHLY_AVERAGES = ['3.747','3.697','3.652','3.700','3.660','3.602',
                    '3.557','3.542','3.502','3.413','3.373','3.367','3.356','3.357',
                    '3.448','3.443']


def completed_before(month, document_date):
    year, number = map(int, month.split('-'))
    return date(year, number, calendar.monthrange(year, number)[1]) < date.fromisoformat(document_date)


def compare_rounded(local, printed):
    return abs(Decimal(local)-Decimal(printed)) <= Decimal('0.0005')+Decimal('1e-9')


def eligible_context(candidates, origin):
    """Only reviewed originals with explicit availability can enter a join.

    Month end alone never implies publication. Date-only document dates are
    insufficient to assign a timestamp; candidate rows therefore remain excluded.
    """
    origin = datetime.fromisoformat(origin.replace('Z','+00:00'))
    if origin.tzinfo is None:
        raise ValueError('Timezone required')
    valid = []
    for row in candidates:
        published = row.get('verified_available_at')
        if row.get('evidence_status') != 'original_verified' or not published:
            continue
        available = datetime.fromisoformat(published.replace('Z','+00:00'))
        if available.tzinfo is None:
            raise ValueError('Verified availability needs timezone')
        if available <= origin and completed_before(row['month'], available.date().isoformat()):
            valid.append(row)
    return sorted(valid,key=lambda row:(row['month'],row['verified_available_at']))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--retrieve',action='store_true',help='Record normal official downloads; never bypass access controls')
    args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    source = ROOT/'datasets/tratamiento/2026-11-01/bcrp-mensual-conciliado.csv'
    with source.open(encoding='utf-8',newline='') as handle:
        local = {row['month']:row for row in csv.DictReader(handle)}
    documents = [
        {'id':'bcrp-ns18-2026-table36','url':'https://www.bcrp.gob.pe/docs/Publicaciones/Nota-Semanal/2026/ns-18-2026.pdf','document_date':'2026-05-14'},
        {'id':'bcrp-ns19-2026-table36','url':'https://www.bcrp.gob.pe/docs/Publicaciones/Nota-Semanal/2026/ns-19-2026.pdf','document_date':'2026-05-21'}]
    if args.retrieve:
        import requests
        storage=ROOT/'data/h2-bcrp-retrieval'
        storage.mkdir(parents=True,exist_ok=True)
        manifest_path=OUT/'retrieval-manifest.json'
        retrieval=json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else []
        for document in documents:
            try:
                response=requests.get(document['url'],timeout=25)
                is_pdf=response.status_code==200 and response.content.startswith(b'%PDF-')
                path=storage/(document['id']+('.pdf' if is_pdf else '.html'))
                path.write_bytes(response.content)
                retrieval.append({'name':document['id'],'url':document['url'],
                    'retrieved_at_utc':datetime.now(timezone.utc).isoformat(),
                    'http_status':response.status_code,'content_type':response.headers.get('Content-Type'),
                    'bytes':len(response.content),'sha256':hashlib.sha256(response.content).hexdigest(),
                    'file':str(path.relative_to(ROOT)).replace('\\','/'),
                    'kind':'pdf' if is_pdf else 'not_pdf','original_verified':False})
            except requests.RequestException as error:
                retrieval.append({'name':document['id'],'url':document['url'],'error_type':type(error).__name__})
        manifest_path.write_text(json.dumps(retrieval,indent=2)+'\n',encoding='utf-8')
    candidates, comparisons = [], []
    for document in documents:
        for index, value in enumerate(MONTHLY_AVERAGES):
            year, month = divmod(2025*12+index,12)
            period = f'{year}-{month+1:02}'
            assert completed_before(period,document['document_date'])
            candidate = {'document_id':document['id'],'month':period,'value':value,
                'unit':'PEN/USD','concept':'interbank_period_average',
                'document_date':document['document_date'],'verified_available_at':None,
                'evidence_status':'indexed_transcription_original_not_verified',
                'original_series_code_mapping':'PN01207PM_candidate_conceptual_mapping_pending_original_check',
                'eligible_asof':False}
            candidates.append(candidate)
            previous = local.get(period,{}).get('pen_per_usd')
            comparisons.append({'document_id':document['id'],'month':period,'local_value':previous,
                'printed_value':value,'absolute_difference':str(abs(Decimal(previous)-Decimal(value))) if previous else None,
                'status':'matches_printed_precision' if previous and compare_rounded(previous,value)
                         else 'conflict' if previous else 'missing_local'})
    documents = [{**document,'table':36,'column':'Interbancario / Promedio',
        'extraction_method':'manual_transcription_of_official_search_index_table_not_original_pdf',
        'printed_decimal_places':3,'original_pdf_verified':False,
        'partial_current_month_excluded':True} for document in documents]
    for name, content in [('documentary-candidates.json',{'documents':documents,'observations':candidates}),
                          ('reconciliation.json',comparisons)]:
        (OUT/name).write_text(json.dumps(content,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    summary = {'date_local':'2026-11-01','local_series_months':len(local),
        'local_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'documentary_candidate_rows':len(candidates),'distinct_months_compared':len({r['month'] for r in comparisons}),
        'matches_printed_precision':sum(r['status']=='matches_printed_precision' for r in comparisons),
        'conflicts':sum(r['status']=='conflict' for r in comparisons),
        'candidate_eligible_asof_rows':len(eligible_context(candidates,'2026-11-01T00:00:00Z')),
        'source_backup_modified':False,'h2_ablation_executed':False,
        'decision':'H2 remains not evaluable; documentary reconciliation advanced but originals and availability not verified',
        'pending':['Obtain valid original dated PDFs and verify table/column identity',
                   'Recover dated vintages before and throughout development, not only May 2026',
                   'Set conservative evidenced availability timestamps and review conceptual mapping',
                   'Verify target coverage, freeze common calendar and execute paired ablation']}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(summary))


if __name__=='__main__':
    main()
