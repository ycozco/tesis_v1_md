"""Start the Docker-only local research app and initialize persistent state."""
import os
from pathlib import Path
import secrets
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'sistema-web-agro/backend'))
sys.path.insert(1, str(ROOT))
state = ROOT / 'data'
state.mkdir(exist_ok=True)
os.chdir(state)
key = state / 'session-signing-key'
if not key.exists():
    key.write_text(secrets.token_urlsafe(48), encoding='utf-8')
    key.chmod(0o600)
os.environ['SECRET_KEY'] = key.read_text(encoding='utf-8').strip()

from sqlalchemy import text
from models import engine, init_tables, SessionLocal, Usuario
from app_fastapi.core.security import get_password_hash, verify_password
if engine.dialect.name == 'postgresql':
    with engine.begin() as connection:
        connection.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
init_tables()
with SessionLocal() as db:
    username = os.environ['LOCAL_USERNAME']
    password = os.environ['LOCAL_PASSWORD']
    user = db.query(Usuario).filter(Usuario.username == username).first()
    if user is None:
        user = Usuario(username=username, email=f'{username}@example.invalid',
                       nombre='Revisión local', rol='ADMIN', password_hash=get_password_hash(password))
        db.add(user)
    elif not verify_password(password, user.password_hash):
        user.password_hash = get_password_hash(password)
    db.commit()

from app_fastapi.main import app
import uvicorn
uvicorn.run(app, host='0.0.0.0', port=8000, log_level='info')
