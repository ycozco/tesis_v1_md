"""Bounded public-source checks; never mutate the research dataset."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import math
import threading
import time
import requests

SOURCES = [
    ('sunat', 'SUNAT / ADUANET', 'http://www.aduanet.gob.pe/aduanas/informae/presentacion_bases_web.htm', 'Registros de exportación'),
    ('sisap', 'SISAP / MIDAGRI', 'http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/consultar/', 'Precios mayoristas internos; revisar unidad publicada'),
    ('bcrp', 'BCRPData', 'https://estadisticas.bcrp.gob.pe/estadisticas/series/PN01207PM/html', 'Tipo de cambio interbancario promedio mensual · S/ por USD'),
    ('nasa', 'NASA POWER', 'https://power.larc.nasa.gov/docs/services/api/temporal/', 'Documentación de variables meteorológicas'),
]
BCRP_API = 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PN01207PM/json'
_lock = threading.Lock()
_cached = None
_expires = 0
TTL = 900


def check_source(source):
    identity, name, url, scope = source
    result = dict(id=identity, name=name, url=url, scope=scope,
                  checked_at=datetime.now(timezone.utc).isoformat(),
                  status='unavailable', last_success_at=None, live_observation=None)
    try:
        endpoint = BCRP_API if identity == 'bcrp' else url
        with requests.get(endpoint, timeout=(3, 5), stream=True,
                          headers={'User-Agent': 'AgroScope-local/1.0'}) as response:
            result['http_status'] = response.status_code
            response.raise_for_status()
            if identity == 'bcrp':
                payload = response.json()
                for period in reversed(payload.get('periods', [])):
                    try:
                        value = float(period['values'][0])
                        if not math.isfinite(value):
                            continue
                    except (KeyError, IndexError, TypeError, ValueError):
                        continue
                    result['live_observation'] = dict(value=value, period=period['name'],
                        unit='S/ por USD', series='PN01207PM', url=BCRP_API)
                    break
                if result['live_observation'] is None:
                    raise ValueError('No numeric observation')
            result['status'] = 'available'
            result['last_success_at'] = datetime.now(timezone.utc).isoformat()
    except requests.RequestException:
        result['reason'] = 'No se pudo consultar la fuente; puede reintentar más tarde.'
    except (ValueError, KeyError, TypeError):
        result['reason'] = 'La fuente no devolvió una serie válida.'
    return result


def catalogue():
    global _cached, _expires
    with _lock:
        if _cached is not None and time.monotonic() < _expires:
            return {**_cached, 'cached': True}
        with ThreadPoolExecutor(max_workers=4) as pool:
            rows = list(pool.map(check_source, SOURCES))
        if _cached:
            previous = {row['id']: row for row in _cached['sources']}
            for row in rows:
                old = previous.get(row['id'], {})
                if row['status'] != 'available':
                    row['last_success_at'] = old.get('last_success_at')
                    row['live_observation'] = old.get('live_observation')
        _cached = dict(sources=rows, cache_seconds=TTL,
                       checked_at=datetime.now(timezone.utc).isoformat(),
                       research_dataset_updated=False)
        _expires = time.monotonic() + TTL
        return {**_cached, 'cached': False}
