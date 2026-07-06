import random
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app_fastapi.api.deps import get_db, get_current_user
from app_fastapi.schemas.auth import LoginRequest, LoginResponse
from app_fastapi.core.security import verify_password, create_access_token
from models import Usuario, SecurityLog

router = APIRouter()

USER_CONDITIONS = {
    'auditor1': 'INTEGRADO',
    'auditor2': 'AISLADO'
}

@router.post("/login", response_model=LoginResponse)
def login(request_data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    identifier = request_data.identifier
    password = request_data.password
    ip_addr = request.client.host if request.client else '127.0.0.1'

    user = db.query(Usuario).filter(
        (Usuario.username == identifier) | (Usuario.email == identifier)
    ).first()

    if user and verify_password(password, user.password_hash):
        if user.rol == 'AUDITOR':
            if user.username not in USER_CONDITIONS:
                USER_CONDITIONS[user.username] = random.choice(['INTEGRADO', 'AISLADO'])
            condicion = USER_CONDITIONS[user.username]
        else:
            condicion = 'ADMIN'

        # Grabar log de seguridad
        sec_log = SecurityLog(usuario=user.username, evento='LOGIN_SUCCESS', ip_address=ip_addr)
        db.add(sec_log)
        db.commit()

        # Emitir JWT real
        access_token = create_access_token(subject=user.username)

        return {
            "token": access_token,
            "user": user.to_dict(),
            "condicion": condicion
        }
    else:
        # Login fallido
        sec_log = SecurityLog(usuario=identifier[:50], evento='LOGIN_FAILURE', ip_address=ip_addr)
        db.add(sec_log)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso denegado. Credenciales incorrectas."
        )

@router.post("/logout")
def logout(request: Request, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    ip_addr = request.client.host if request.client else '127.0.0.1'
    
    sec_log = SecurityLog(usuario=current_user.username, evento='LOGOUT', ip_address=ip_addr)
    db.add(sec_log)
    db.commit()
    
    return {"message": "Sesión cerrada."}
