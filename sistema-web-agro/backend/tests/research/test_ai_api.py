"""Isolated integration tests: real JWT/SQLite; provider transport mocked, no cloud spend."""
import hashlib
import json
import os
from pathlib import Path
import sys
from types import SimpleNamespace
import pytest

ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'data/runtime-api'))
sys.path.insert(1,str(ROOT/'sistema-web-agro/backend'))
os.environ['DATABASE_URL']='sqlite+pysqlite:///:memory:'
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
import models
from app_fastapi.main import app
from app_fastapi.api.deps import get_db
from app_fastapi.core.security import get_password_hash
from services import research_ai as service


@pytest.fixture
def client(tmp_path, monkeypatch):
    engine=create_engine('sqlite://',connect_args={'check_same_thread':False},poolclass=StaticPool)
    models.Base.metadata.create_all(engine)
    factory=sessionmaker(bind=engine)
    monkeypatch.setattr(models,'engine',engine)
    monkeypatch.setattr(service,'REPORTS',tmp_path)
    monkeypatch.delenv('RESEARCH_ALLOW_PAID_AI',raising=False)
    monkeypatch.delenv('RESEARCH_ALLOW_LOCAL_AI',raising=False)
    monkeypatch.delenv('RESEARCH_DEEPSEEK_API_KEY',raising=False)
    # Avoid depending on an actual Ollama daemon in isolated tests.
    monkeypatch.setattr(service,'local_models',lambda: [])
    with factory() as db:
        for name,role in [('qa-admin','ADMIN'),('qa-reader','AUDITOR')]:
            db.add(models.Usuario(username=name,email=name+'@example.invalid',nombre=name,
                                  password_hash=get_password_hash('isolated-test-password'),rol=role))
        db.commit()
    def db_session():
        with factory() as db: yield db
    app.dependency_overrides[get_db]=db_session
    with TestClient(app) as session:
        yield session
    app.dependency_overrides.clear()
    engine.dispose()


def auth(client,name='qa-admin'):
    response=client.post('/api/auth/login',json={'identifier':name,'password':'isolated-test-password'})
    assert response.status_code==200
    return {'Authorization':'Bearer '+response.json()['token']}


def test_endpoints_require_auth_and_validate_requests(client):
    for path in ['audit','providers','cases']:
        assert client.get('/api/research/'+path).status_code==401
    headers=auth(client)
    assert client.post('/api/research/reports',headers=headers,json={'case_id':'palta-01','url':'https://untrusted.invalid'}).status_code==422
    assert client.post('/api/research/reports',headers=headers,json={'case_id':'missing'}).status_code==404


def test_source_integrity_and_cases(client):
    headers=auth(client)
    result=client.get('/api/research/audit',headers=headers).json()
    assert result['integrity_ok'] and result['verified_files']==result['total_files']==44
    cases=client.get('/api/research/cases',headers=headers).json()['cases']
    assert len(cases)==30
    assert all(len(case['evidence'])==3 for case in cases)


def test_template_archival_hash_and_owner_access(client):
    headers=auth(client,'qa-reader')
    result=client.post('/api/research/reports',headers=headers,json={'case_id':'palta-01'}).json()
    assert result['provider']=='template' and result['validation']['numeric_status']=='passed'
    assert result['validation']['factual_status']=='requires_human_review'
    assert result['h4_experiment_output'] is False and result['is_rag'] is False
    download=client.get('/api/research/reports/'+result['id']+'/file',headers=headers)
    assert download.status_code==200
    assert hashlib.sha256(download.content).hexdigest()==result['report_sha256']==download.headers['X-Report-SHA256']
    assert client.get('/api/research/reports/not-a-uuid/file',headers=headers).status_code==422


def test_provider_disabled_and_paid_role_gate(client):
    admin=auth(client)
    providers=client.get('/api/research/providers',headers=admin).json()['providers']
    assert {p['id']:p['ready'] for p in providers}=={'template':True,'ollama':False,'deepseek':False}
    response=client.post('/api/research/reports',headers=admin,json={'case_id':'palta-01','provider':'deepseek','paid_consent':True})
    assert response.status_code==503
    reader=auth(client,'qa-reader')
    assert client.post('/api/research/reports',headers=reader,json={'case_id':'palta-01','provider':'deepseek','paid_consent':True}).status_code==403


def test_deepseek_adapter_mocked_no_actual_cloud_call(client,monkeypatch):
    monkeypatch.setenv('RESEARCH_ALLOW_PAID_AI','true')
    monkeypatch.setenv('RESEARCH_DEEPSEEK_API_KEY','FAKE-TEST-KEY-NOT-A-CREDENTIAL')
    sent=[]
    def post(url,**kwargs):
        sent.append((url,kwargs))
        case=service.cases()[0]
        claims=[{'fact_id':k,'value':v['value'],'source_id':v['source_id'],'unit':v['unit']} for k,v in case['evidence'].items()]
        body={'choices':[{'message':{'content':json.dumps({'summary':'Borrador simulado para pruebas.','claims':claims})}}],
              'model':'mocked-deepseek','usage':{'total_tokens':20}}
        return SimpleNamespace(status_code=200,json=lambda:body)
    monkeypatch.setattr(service.requests,'post',post)
    headers=auth(client)
    case_id=service.cases()[0]['case_id']
    assert client.post('/api/research/reports',headers=headers,json={'case_id':case_id,'provider':'deepseek'}).status_code==409
    assert sent==[]
    response=client.post('/api/research/reports',headers=headers,json={'case_id':case_id,'provider':'deepseek','paid_consent':True})
    assert response.status_code==200 and response.json()['validation']['numeric_status']=='passed'
    assert sent[0][0]=='https://api.deepseek.com/chat/completions'
    payload=sent[0][1]['json']
    assert payload['max_tokens']==800 and payload['thinking']['type']=='disabled'
    assert 'FAKE-TEST-KEY' not in response.text


def test_missing_duplicate_and_wrong_unit_claims_are_not_passed():
    evidence={'f':{'value':1000,'unit':'kg','source_id':'s'}}
    claim={'fact_id':'f','value':'1000.006','unit':'kg','source_id':'s','decimals':0}
    assert service._validate({'claims':[claim]},evidence)['numeric_status']=='failed'
    claim['value']='1000.00'
    assert service._validate({'claims':[claim,claim]},evidence)['numeric_status']=='failed'
    claim['unit']='USD'
    assert service._validate({'claims':[claim]},evidence)['numeric_status']=='failed'
    assert service._validate({'claims':[]},evidence)['numeric_status']=='failed'
    with pytest.raises(service.ResearchError):
        service._validate({'claims':[{'fact_id':{}}]},evidence)


def test_tampered_report_cannot_be_downloaded(client):
    headers=auth(client)
    result=client.post('/api/research/reports',headers=headers,json={'case_id':'palta-01'}).json()
    path=service.REPORTS/(result['id']+'.json')
    body=json.loads(path.read_bytes());body['summary']='Changed after archival'
    path.write_text(json.dumps(body),encoding='utf8')
    response=client.get('/api/research/reports/'+result['id']+'/file',headers=headers)
    assert response.status_code==409


def test_valid_token_logout_and_invalid_login(client):
    assert client.post('/api/auth/login',json={'identifier':'qa-reader','password':'wrong'}).status_code==401
    assert client.post('/api/auth/logout').status_code==401
    assert client.post('/api/auth/logout',headers=auth(client)).status_code==200
    assert client.get('/health').status_code==200
    assert client.get('/api/migration/status').status_code==200


def test_legacy_dashboard_requires_auth_and_has_no_fabricated_trends(client):
    assert client.get('/api/dashboard/stats').status_code==401
    response=client.get('/api/dashboard/stats',headers=auth(client))
    assert response.status_code==200
    assert len(response.json()['trends_14_days'])==14
    assert all(row['cantidad']==0 for row in response.json()['trends_14_days'])


def test_ollama_adapter_uses_only_configured_local_model(client,monkeypatch):
    monkeypatch.setenv('RESEARCH_ALLOW_LOCAL_AI','true')
    monkeypatch.setenv('RESEARCH_OLLAMA_MODEL','qa-local-model')
    monkeypatch.setattr(service,'local_models',lambda:['qa-local-model'])
    sent=[]
    def post(url,**kwargs):
        sent.append((url,kwargs))
        case=service.cases()[0]
        claims=[{'fact_id':k,'value':v['value'],'source_id':v['source_id'],'unit':v['unit']} for k,v in case['evidence'].items()]
        return SimpleNamespace(status_code=200,json=lambda:{'choices':[{'message':{'content':json.dumps({'summary':'Prueba local simulada','claims':claims})}}]})
    monkeypatch.setattr(service.requests,'post',post)
    response=client.post('/api/research/reports',headers=auth(client),json={'case_id':service.cases()[0]['case_id'],'provider':'ollama'})
    assert response.status_code==200
    assert sent[0][0]=='http://127.0.0.1:11434/v1/chat/completions'
    assert 'Authorization' not in sent[0][1]['headers']


def test_provider_failure_is_redacted_and_never_silently_falls_back(client,monkeypatch):
    monkeypatch.setenv('RESEARCH_ALLOW_PAID_AI','true')
    monkeypatch.setenv('RESEARCH_DEEPSEEK_API_KEY','FAKE-TEST-KEY-NOT-A-CREDENTIAL')
    def post(*args,**kwargs):raise service.requests.Timeout('FAKE-TEST-KEY-NOT-A-CREDENTIAL')
    monkeypatch.setattr(service.requests,'post',post)
    response=client.post('/api/research/reports',headers=auth(client),json={'case_id':'palta-01','provider':'deepseek','paid_consent':True})
    assert response.status_code==502
    assert 'FAKE-TEST-KEY' not in response.text
    events=[json.loads(line) for line in (service.REPORTS/'events.jsonl').read_text().splitlines()]
    assert events[-1]['status']=='failed'
    assert not list(service.REPORTS.glob('*.json'))
    monkeypatch.setattr(service.requests,'post',lambda *args,**kwargs:SimpleNamespace(status_code=200,json=lambda:{'choices':[{'message':{'content':None}}]}))
    assert client.post('/api/research/reports',headers=auth(client),json={'case_id':'palta-01','provider':'deepseek','paid_consent':True}).status_code==502
