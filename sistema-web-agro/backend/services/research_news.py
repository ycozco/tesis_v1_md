"""Bounded news discovery. Headlines provide context, never causal evidence."""
from datetime import date, datetime, timedelta, timezone
from urllib.parse import urlparse
import threading
import time
import requests
from services.research_ai import ResearchError

PRODUCTS = {'palta': '(avocado OR palta)', 'uva': '(grape OR uva)', 'arandano': '(blueberry OR arandano)'}
TOPICS = {'trade': '(export OR exports OR exportacion)', 'logistics': '(port OR shipping OR logistics OR puerto)', 'weather': '(weather OR drought OR climate OR sequia)'}
_cache = {}
_lock = threading.Lock()

def search(product, week, topic):
    if product not in PRODUCTS or topic not in TOPICS:
        raise ResearchError('news_filter', 'Filtro de noticias no válido.', 422)
    start = date.fromisoformat(week)
    now = datetime.now(timezone.utc)
    end = min(start + timedelta(days=6), now.date())
    if start < now.date() - timedelta(days=89) or start > now.date():
        raise ResearchError('news_window', 'GDELT admite fechas recientes. Seleccione una semana de los últimos 89 días.', 422)
    key = (product, week, topic)
    query = f'{PRODUCTS[product]} (Peru OR Peruvian) {TOPICS[topic]}'
    with _lock:
        if key in _cache and time.monotonic() - _cache[key][0] < 900:
            return {**_cache[key][1], 'cached': True}
        if _cache.get('_last', 0) > time.monotonic() - 5:
            raise ResearchError('news_throttle', 'Espere cinco segundos entre consultas de noticias.', 429)
        _cache['_last'] = time.monotonic()
    params = {'query': query, 'mode': 'ArtList', 'format': 'json', 'sort': 'DateDesc', 'maxrecords': 12,
              'startdatetime': start.strftime('%Y%m%d000000'),
              'enddatetime': min(datetime.combine(end, datetime.max.time(), tzinfo=timezone.utc), now).strftime('%Y%m%d%H%M%S')}
    try:
        response = requests.get('https://api.gdeltproject.org/api/v2/doc/doc', params=params, timeout=(4, 18), allow_redirects=False)
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload.get('articles'), list):
            raise ValueError('invalid articles')
        articles = []
        seen = set()
        for a in payload['articles']:
            url = a.get('url', '')
            parsed = urlparse(url)
            if parsed.scheme not in ('https', 'http') or not parsed.hostname or parsed.username or parsed.password or url in seen:
                continue
            seen.add(url)
            articles.append({'title': str(a.get('title', 'Sin título'))[:500], 'url': url,
                             'domain': parsed.hostname, 'indexed_at': a.get('seendate'), 'language': a.get('language')})
    except (requests.RequestException, ValueError, TypeError, AttributeError):
        raise ResearchError('news_unavailable', 'GDELT no respondió con resultados válidos. Puede reintentar; no se han inventado noticias.', 503)
    result = {'provider': 'GDELT DOC 2.0', 'query': query, 'start': start.isoformat(), 'end': end.isoformat(),
              'queried_at': now.isoformat(), 'articles': articles, 'cached': False,
              'scope': 'context_not_causality', 'date_kind': 'GDELT indexing time; verify publication at source'}
    with _lock:
        if len(_cache) > 100: _cache.clear()
        _cache[key] = (time.monotonic(), result)
    return result
