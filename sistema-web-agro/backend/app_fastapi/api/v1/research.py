from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, ConfigDict, Field
from app_fastapi.api.deps import get_current_user
from services import research_ai, codex_pilot

router = APIRouter()


@router.get('/sources')
def source_catalogue(user=Depends(get_current_user)):
    from services.source_status import catalogue
    return catalogue()


class Generation(BaseModel):
    model_config = ConfigDict(extra='forbid')
    case_id: str = Field(min_length=1, max_length=60)
    provider: Literal['template', 'ollama', 'deepseek'] = 'template'
    paid_consent: bool = False


def execute(action):
    try: return action()
    except research_ai.ResearchError as error:
        raise HTTPException(error.status, detail={'code': error.code, 'message': error.message})
    except (OSError, ValueError):
        raise HTTPException(503, detail={'code': 'artifact_unavailable', 'message': 'No se pudo comprobar la evidencia local.'})


@router.get('/audit')
def audit(user=Depends(get_current_user)):
    return execute(research_ai.integrity)


@router.get('/providers')
def providers(user=Depends(get_current_user)):
    return execute(research_ai.providers)


@router.get('/cases')
def cases(user=Depends(get_current_user)):
    return execute(lambda: {'cases': research_ai.cases()})


@router.get('/codex-pilots')
def codex_catalogue(user=Depends(get_current_user)):
    return execute(codex_pilot.catalogue)


@router.get('/progress')
def current_progress(user=Depends(get_current_user)):
    return execute(codex_pilot.progress)


@router.get('/codex-pilots/{pilot_id}/file')
def codex_download(pilot_id:str,user=Depends(get_current_user)):
    content,sha=execute(lambda:codex_pilot.export(pilot_id))
    return Response(content,media_type='application/json',headers={
        'Content-Disposition':'attachment; filename="codex-exposed-pilot.json"','X-Report-SHA256':sha})


@router.get('/codex-pilots/{pilot_id}')
def codex_detail(pilot_id:str,user=Depends(get_current_user)):
    content,sha=execute(lambda:codex_pilot.export(pilot_id))
    import json
    return {**json.loads(content),'download_sha256':sha}


@router.post('/reports')
def generate(body: Generation, user=Depends(get_current_user)):
    if body.provider == 'deepseek' and user.rol != 'ADMIN':
        raise HTTPException(403, detail='Solo un administrador puede solicitar consumo de la API de pago.')
    return execute(lambda: research_ai.generate(body.case_id, body.provider, body.paid_consent, user.username))


@router.get('/reports/{report_id}/file')
def download_report(report_id: str, user=Depends(get_current_user)):
    content, sha = execute(lambda: research_ai.archived_report(report_id, user.username, user.rol == 'ADMIN'))
    return Response(content, media_type='application/json', headers={
        'Content-Disposition': 'attachment; filename="research-report.json"', 'X-Report-SHA256': sha})

class NewsQuery(BaseModel):
    model_config = ConfigDict(extra='forbid')
    product: Literal['palta', 'uva', 'arandano']
    week: str = Field(pattern=r'^\d{4}-\d{2}-\d{2}$')
    topic: Literal['trade', 'logistics', 'weather'] = 'trade'

@router.post('/news')
def related_news(body: NewsQuery, user=Depends(get_current_user)):
    from services.research_news import search
    return execute(lambda: search(body.product, body.week, body.topic))

class ExperimentalTraining(BaseModel):
    model_config = ConfigDict(extra='forbid')
    product: Literal['palta', 'uva', 'arandano'] = 'uva'
    destination: str = Field(default='US', pattern=r'^[A-Z0-9]{2}$')
    target: Literal['unit_fob', 'volume_kg'] = 'unit_fob'
    horizon: Literal[1, 2, 4] = 1
    parallel: bool = True
    time_limit: int = Field(default=60, ge=30, le=180)
    validation_end: str | None = Field(default=None, pattern=r'^\d{4}-\d{2}-\d{2}$')


def training_request(path, body=None):
    import requests
    try:
        response = requests.get('http://training:8010/'+path, timeout=(3, 8)) if body is None else requests.post('http://training:8010/'+path, json=body, timeout=(3, 10))
        payload = response.json()
    except (requests.RequestException, ValueError):
        raise HTTPException(503, detail='El entorno de entrenamiento no está disponible. Compruebe el servicio training.')
    if not response.ok:
        raise HTTPException(response.status_code, detail=payload.get('detail','No se pudo iniciar el entrenamiento.'))
    return payload

@router.get('/training')
def training_status(product: Literal['palta', 'uva', 'arandano'] = 'uva', destination: str = 'US', target: Literal['unit_fob', 'volume_kg'] = 'unit_fob', horizon: int = 1, validation_end: str | None = None, user=Depends(get_current_user)):
    from urllib.parse import urlencode
    query = {'product': product, 'destination': destination, 'target': target, 'horizon': horizon}
    if validation_end: query['validation_end'] = validation_end
    return training_request('status?' + urlencode(query))

@router.post('/training')
def start_training(body: ExperimentalTraining, user=Depends(get_current_user)):
    if user.rol != 'ADMIN':
        raise HTTPException(403, detail='Solo un administrador puede iniciar entrenamientos experimentales.')
    return training_request('start', body.model_dump())


@router.get('/market-context')
def market_context(user=Depends(get_current_user)):
    from services.market_context import snapshot
    return snapshot()


@router.get('/forecasts')
def archived_forecasts(user=Depends(get_current_user)):
    from pathlib import Path
    from fastapi.responses import FileResponse
    artifact = Path(__file__).resolve().parents[4] / 'frontend/public/research/forecasts.json'
    if not artifact.is_file():
        raise HTTPException(404, detail='El archivo de pronósticos del piloto no está disponible.')
    return FileResponse(artifact, media_type='application/json')
