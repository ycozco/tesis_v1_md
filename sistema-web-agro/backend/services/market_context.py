"""Public market context, persisted independently of the frozen research cut."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone, date
from html.parser import HTMLParser
from pathlib import Path
import copy
import json
import math
import logging
import re
import threading
import requests

LIMA = timezone(timedelta(hours=-5))
INTERVAL = 3600
SISAP_URL = 'http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/filtrar'
SISAP_PAGE = 'http://sistemas.midagri.gob.pe/sisap/portal2/mayorista/resumenes/consultar/'
BCRP_URL = 'https://estadisticas.bcrp.gob.pe/estadisticas/series/api/PD04638PD/json'
REGIONS = [('ica', 'Ica', -14.07, -75.73), ('trujillo', 'Trujillo', -8.11, -79.03), ('arequipa', 'Arequipa', -16.40, -71.54)]
_lock = threading.Lock()
_stop = threading.Event()
_thread = None
_state = None
_store = None

def now():
    return datetime.now(LIMA).isoformat()

def number(value):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError('Non-finite public observation')
    return result

class PriceTable(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows, self.cells, self.cell = [], [], None
    def handle_starttag(self, tag, attrs):
        if tag == 'tr': self.cells = []
        if tag in ('td', 'th'): self.cell = []
        if tag == 'br' and self.cell is not None: self.cell.append(' ')
    def handle_data(self, data):
        if self.cell is not None: self.cell.append(data)
    def handle_endtag(self, tag):
        if tag in ('td', 'th') and self.cell is not None:
            self.cells.append(' '.join(''.join(self.cell).split())); self.cell = None
        if tag == 'tr' and self.cells: self.rows.append(self.cells)

def parse_sisap(html, requested_date):
    match = re.search(r'Fecha:\s*(\d{2}/\d{2}/\d{4})', html)
    if not match or match.group(1) != requested_date.strftime('%d/%m/%Y'):
        raise ValueError('Unverified price date')
    parser = PriceTable(); parser.feed(html)
    if not parser.rows or not any('S/.' in x and 'Kg.' in x and 'Unid.' in x for x in parser.rows[0]):
        raise ValueError('Changed price unit header')
    product = None; rows = []
    for cells in parser.rows[1:]:
        if len(cells) == 3: product, variety, raw = cells
        elif len(cells) == 2: variety, raw = cells
        else: continue
        if product not in ('Palta', 'Uva'): continue
        try: value = number(raw.replace(',', '.'))
        except (ValueError, TypeError): continue
        if value <= 0: continue
        rows.append(dict(product=product, variety=variety, value=value))
    if not rows: raise ValueError('No verified prices')
    return rows

def get_json(url, **kwargs):
    r = requests.get(url, timeout=(4, 16), headers={'User-Agent':'AgroScope/1.0 public research dashboard'}, **kwargs)
    r.raise_for_status()
    return r.json()

def exchange():
    payload = get_json(BCRP_URL)
    months = {'Ene':1,'Feb':2,'Mar':3,'Abr':4,'May':5,'Jun':6,'Jul':7,'Ago':8,'Sep':9,'Set':9,'Oct':10,'Nov':11,'Dic':12}
    observations = []
    for row in payload.get('periods', []):
        try:
            day, month, year = row['name'].split('.')
            period = date(2000+int(year) if len(year)==2 else int(year), months[month], int(day))
            value = number(row['values'][0])
            if value > 0 and period <= datetime.now(LIMA).date(): observations.append((period, value))
        except (KeyError, ValueError, TypeError, IndexError): continue
    if not observations: raise ValueError('No dated exchange observation')
    observations.sort(); period,value = observations[-1]
    previous = observations[-2][1] if len(observations)>1 else None
    return [dict(id='usd',kind='exchange',label='Dólar interbancario',value=value,unit='S/ por USD',
        observed_at=period.isoformat(),source='BCRP',url=BCRP_URL,series='PD04638PD',
        detail='Tipo de cambio venta · última observación diaria publicada',change=value-previous if previous else None,
        status='available' if (datetime.now(LIMA).date()-period).days<=7 else 'delayed')]

def prices():
    today = datetime.now(LIMA).date()
    r = requests.post(SISAP_URL, data={'ajax':'true','__ajax_carga_final':'consulta','fecha':today.strftime('%d/%m/%Y'),
        'periodicidad':'dia','mercado':'15011502','productos[]':['0626','0637'],'producto':'NA','variables[]':'precio_prom'},
        timeout=(4,20),headers={'User-Agent':'AgroScope/1.0 public research dashboard'})
    r.raise_for_status()
    rows = parse_sisap(r.text,today)
    return [dict(id='price-'+str(i),kind='price',label=row['variety'],product=row['product'],value=row['value'],
        unit='S/ · unidad de fuente',observed_at=today.isoformat(),source='SISAP / MIDAGRI',url=SISAP_PAGE,
        detail='Mercado Mayorista N.º 2 de Frutas, Lima',unit_note='Encabezado publicado: S/ por kg, litro o unidad. Unidad específica no validada; sin conversión.',
        status='available') for i,row in enumerate(rows)]

def weather(region):
    identity,label,lat,lon = region
    payload = get_json('https://api.open-meteo.com/v1/forecast',params={'latitude':lat,'longitude':lon,
        'current':'temperature_2m,relative_humidity_2m,precipitation','daily':'temperature_2m_max,temperature_2m_min,precipitation_sum',
        'forecast_days':3,'timezone':'America/Lima'})
    c,d = payload['current'],payload['daily']; value=number(c['temperature_2m'])
    observed = datetime.fromisoformat(c['time']).replace(tzinfo=LIMA)
    age = datetime.now(LIMA)-observed
    if age.total_seconds() < -3600: raise ValueError('Future current weather')
    return [dict(id='weather-'+identity,kind='weather',label=label,value=value,unit='°C',observed_at=observed.isoformat(),
        source='Open-Meteo',url='https://open-meteo.com/en/docs',latitude=lat,longitude=lon,
        detail='Condiciones de modelo · punto de referencia regional',humidity=number(c['relative_humidity_2m']),
        precipitation=number(c['precipitation']),high=number(d['temperature_2m_max'][0]),low=number(d['temperature_2m_min'][0]),
        status='available' if age.total_seconds()<10800 else 'delayed')]

def collect_one(identity, action, previous):
    checked = now()
    try:
        return [dict(row,checked_at=checked,last_success_at=checked) for row in action()]
    except (requests.RequestException,ValueError,KeyError,TypeError,IndexError):
        old = [dict(row,status='stale',checked_at=checked,reason='No se pudo actualizar; se conserva el último dato recuperado.') for row in previous if row.get('group')==identity]
        return old or [dict(id=identity,kind='price' if identity=='sisap' else 'weather' if identity.startswith('weather-') else 'exchange',
            label='Precios mayoristas' if identity=='sisap' else identity,source='SISAP / MIDAGRI' if identity=='sisap' else 'Open-Meteo' if identity.startswith('weather-') else 'BCRP',
            value=None,unit='',observed_at=None,checked_at=checked,last_success_at=None,status='unavailable',
            url=SISAP_PAGE if identity=='sisap' else 'https://open-meteo.com/en/docs' if identity.startswith('weather-') else BCRP_URL,
            detail='La fuente no devolvió datos verificables. Se reintentará automáticamente.')]

def refresh():
    global _state
    with _lock: previous=copy.deepcopy((_state or {}).get('items',[]))
    jobs=[('bcrp',exchange),('sisap',prices)]+[('weather-'+r[0],lambda r=r:weather(r)) for r in REGIONS]
    def run(job):
        identity,action=job
        return [dict(row,group=identity) for row in collect_one(identity,action,previous)]
    with ThreadPoolExecutor(max_workers=5) as pool: items=[row for rows in pool.map(run,jobs) for row in rows]
    result=dict(items=items,checked_at=now(),refresh_seconds=INTERVAL,research_dataset_updated=False,
        scope='public_context_not_offers_or_price_forecasts')
    with _lock:
        _state=result
        if _store:
            try:
                tmp=_store.with_suffix('.tmp');tmp.write_text(json.dumps(result,ensure_ascii=False),encoding='utf-8');tmp.replace(_store)
            except OSError: pass
    return result

def snapshot():
    with _lock:
        result=copy.deepcopy(_state) if _state else dict(items=[],checked_at=None,refresh_seconds=INTERVAL,research_dataset_updated=False)
    # A stopped collector must not leave old values labelled current.
    for row in result['items']:
        try:
            if row.get('status')=='available' and (datetime.now(LIMA)-datetime.fromisoformat(row['checked_at'])).total_seconds()>INTERVAL*2:
                row['status']='stale'
        except (KeyError,ValueError,TypeError): row['status']='stale'
    return result

def start():
    global _state,_thread,_store
    if _thread and _thread.is_alive(): return
    _store=Path.cwd()/'market-context.json'
    try:
        loaded=json.loads(_store.read_text(encoding='utf-8'))
        if isinstance(loaded.get('items'),list): _state=loaded
    except (OSError,ValueError,AttributeError): pass
    _stop.clear()
    def loop():
        while not _stop.is_set():
            try: refresh()
            except Exception: logging.getLogger(__name__).exception("Public market collector failed")
            _stop.wait(INTERVAL)
    _thread=threading.Thread(target=loop,name='public-market-context',daemon=True);_thread.start()

def stop():
    _stop.set()
