from pydantic import BaseModel
from typing import Optional


class UsuarioLogin(BaseModel):
    email: str
    password: str


class UsuarioRegistro(BaseModel):
    nombre: str
    email: str
    password: str
    rol: str
    telefono: Optional[str] = None


class Usuario(BaseModel):
    id: int
    nombre: str
    email: str
    rol: str

    class Config:
        orm_mode = True
