from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from models import UsuarioModel
from auth.auth import get_current_user
from services.retiro_service import RetiroService
from schemas.responses import (
    RetiroCreateSchema,
    RetiroInDBSchema,
)
from schemas.errors.retiro_error_schema import RetiroErrorResponse

router = APIRouter(prefix="/retiros", tags=["retiros"])


@router.post(
    "/",
    response_model=RetiroInDBSchema,
    description="Crea un nuevo retiro",
    responses={
        422: {
            "model": RetiroErrorResponse,
            "description": "Error de validación",
        }
    },
)
async def crear_retiro(
    retiro: RetiroCreateSchema,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user),
):
    retiro_service = RetiroService(db)
    return retiro_service.crear_retiro(retiro, current_user)


@router.get("/", response_model=List[RetiroInDBSchema])
async def listar_retiros(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user),
):
    retiro_service = RetiroService(db)
    return retiro_service.listar_retiros(current_user, skip, limit)


@router.get(
    "/{retiro_id}",
    response_model=RetiroInDBSchema,
)
async def obtener_retiro(
    retiro_id: int = Path(
        ...,
        description="ID del retiro",
        example=1,
        ge=1,
        error_messages={
            "type_error": "El ID debe ser un número entero",
            "int_parsing": "El ID debe ser un número entero válido",
            "ge": "El ID debe ser mayor o igual a 1",
        },
    ),
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user),
):
    retiro_service = RetiroService(db)
    return retiro_service.obtener_retiro(retiro_id, current_user)
