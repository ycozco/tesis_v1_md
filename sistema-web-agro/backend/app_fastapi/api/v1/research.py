from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, ConfigDict, Field
from app_fastapi.api.deps import get_current_user
from services import research_ai

router = APIRouter()


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
