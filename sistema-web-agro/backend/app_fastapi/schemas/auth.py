from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    identifier: str
    password: str

class UserResponse(BaseModel):
    id_usuario: int
    username: str
    email: str
    rol: str
    nombre: str

class LoginResponse(BaseModel):
    token: str
    user: UserResponse
    condicion: str
