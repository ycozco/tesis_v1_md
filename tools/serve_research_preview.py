"""Loopback-only real FastAPI preview with an isolated SQLite DB and QA account.

This does not point to the production database or enable external AI.
Run via the audited Python interpreter; credentials are temporary test fixtures.
"""
import os
from pathlib import Path
import sys
import secrets

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'data/runtime-api'))
sys.path.insert(1,str(ROOT/'sistema-web-agro/backend'))
folder=ROOT/'data/research_preview'
folder.mkdir(parents=True,exist_ok=True)
os.environ['DATABASE_URL']='sqlite+pysqlite:///'+str(folder/'preview.sqlite').replace('\\','/')
os.environ['SECRET_KEY']=secrets.token_urlsafe(48)
os.environ['RESEARCH_ALLOW_LOCAL_AI']='false'
os.environ['RESEARCH_ALLOW_PAID_AI']='false'
from models import init_tables,SessionLocal,Usuario
from app_fastapi.core.security import get_password_hash
from app_fastapi.main import app
import uvicorn

init_tables()
with SessionLocal() as db:
    user=db.query(Usuario).filter(Usuario.username=='revision-ui').first()
    if user is None:
        user=Usuario(username='revision-ui',email='revision-ui@example.invalid',nombre='Revisión local',rol='ADMIN',
                     password_hash=get_password_hash('SoloRevisionLocal2026!'))
        db.add(user)
    else:
        user.password_hash=get_password_hash('SoloRevisionLocal2026!')
    db.commit()
print('Isolated FastAPI preview on loopback:5002; QA-only account; paid/local AI disabled.',flush=True)
uvicorn.run(app,host='127.0.0.1',port=5002,log_level='warning')
