"""Recover actual public context data, keeping eligibility separate from availability."""
import concurrent.futures
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'datasets/tratamiento/2026-11-01/contexto'


def retrieve(name, url, params=None, data=None):
    item = {'name': name, 'url': url, 'params': params, 'post_data': data,
            'retrieved_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'eligible_asof': False}
    try:
        r = requests.post(url, data=data, timeout=40) if data else requests.get(url, params=params, timeout=40)
        item.update(http_status=r.status_code, content_type=r.headers.get('Content-Type'), bytes=len(r.content))
        r.raise_for_status()
        text = r.text
        if re.search('Pardon Our Interruption|captcha|Access Denied', text, re.I):
            item['status'] = 'access_control_not_bypassed'
            return item
        suffix = '.html'
        try:
            value = r.json()
            suffix = '.json'
            item['status'] = 'json_received_needs_semantic_validation'
            if name.startswith('nasa'):
                parameters = value['properties']['parameter']
                item['observations_per_parameter'] = {k: sum(v != -999 for v in values.values()) for k, values in parameters.items()}
                item['status'] = 'context_point_recovered_NOT_production_origin'
            elif name == 'bcrp-online':
                item['periods'] = len(value['periods'])
                item['status'] = 'monthly_series_recovered_publication_dates_unknown'
        except (ValueError, KeyError):
            item['status'] = 'html_received_not_confirmed_data'
            if name.startswith('sisap'):
                item['status'] = 'table_received_needs_cell_validation' if '<table' in text.lower() and re.search(r'\d+[.,]\d{2}', text) else 'no_confirmed_table'
        file = OUT / (name + suffix)
        file.write_bytes(r.content)
        item['file'], item['sha256'] = file.name, hashlib.sha256(r.content).hexdigest()
    except Exception as e:
        item['status'], item['error'] = 'failed', str(e)
    return item


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [('bcrp-online', 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01207PM/json/2018-1/2026-10/esp', None, None)]
    # One documented point, deliberately NOT assigned to any export or product.
    jobs.append(('nasa-arequipa-contexto-2018-2026', 'https://power.larc.nasa.gov/api/temporal/daily/point',
        {'parameters':'T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M', 'community':'AG', 'longitude':-71.54,
         'latitude':-16.4, 'start':'20180101', 'end':'20261022', 'format':'JSON'}, None))
    for product, code in [('palta', '0626'), ('uva', '0637')]:
        jobs.append(('sisap-' + product + '-2018-2026',
            'http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/filtrar', None,
            {'__ajax_carga_final':'consulta', 'periodicidad':'mensual', 'mercado':'15011502',
             'anios[]':[str(y) for y in range(2018, 2027)], 'meses[]':[f'{m:02}' for m in range(1,13)],
             'productos[]':code, 'variables[]':'precio_prom'}))
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(lambda args: retrieve(*args), jobs))
    (OUT / 'manifest-recuperacion.json').write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(results, indent=2, ensure_ascii=True))


if __name__ == '__main__':
    main()
