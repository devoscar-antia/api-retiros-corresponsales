from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from models import UsuarioModel
from schemas.responses.usuario_schema import UsuarioResponse, UsuarioCreateSchema
from auth.auth import get_current_user
from services.usuario_service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/", response_model=List[UsuarioResponse])
async def get_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Obtiene la lista de usuarios.
    - skip: número de registros a saltar (paginación)
    - limit: número máximo de registros a retornar
    """
    usuario_service = UsuarioService(db)
    return usuario_service.get_usuarios(skip, limit)


@router.get("/me", response_model=UsuarioResponse)
async def read_users_me(
    current_user: UsuarioModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Endpoint protegido que obtiene los datos actualizados del usuario autenticado."""
    usuario_service = UsuarioService(db)
    return usuario_service.get_current_user_data(current_user)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def get_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user),
):
    """
    Obtiene un usuario por su ID
    """
    usuario_service = UsuarioService(db)
    return usuario_service.get_usuario_by_id(usuario_id)


@router.post("/", response_model=UsuarioResponse)
async def create_usuario(usuario: UsuarioCreateSchema, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario
    - nombre: nombre del usuario (2-100 caracteres)
    - correo: correo electrónico (debe ser único y válido)
    - clave: contraseña (8-72 caracteres, debe incluir mayúsculas, minúsculas y números)
    """
    usuario_service = UsuarioService(db)
    return usuario_service.create_usuario(usuario)
