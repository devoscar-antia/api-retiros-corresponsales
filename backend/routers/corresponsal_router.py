from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from services.corresponsal_service import CorresponsalService
from models.usuario_model import UsuarioModel
from auth.auth import get_current_user
from schemas.responses.corresponsal_schema import (
    CorresponsalTotalDiaSchema,
    CorresponsalListResponse,
)
from schemas.errors.corresponsal_error_schema import CorresponsalErrorResponse

router = APIRouter(prefix="/corresponsales", tags=["corresponsales"])


@router.get(
    "/dia/{corresponsal_id}",
    response_model=CorresponsalTotalDiaSchema,
    description="Obtiene el total de retiros del día para un corresponsal específico",
    responses={
        422: {
            "model": CorresponsalErrorResponse,
            "description": "Error de validación",
        }
    },
)
async def obtener_total_dia_corresponsal(
    corresponsal_id: int = Path(
        ...,
        description="ID del corresponsal",
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
    # Nota: Si se quiere se puede validar para que este router sea solo accesible para el admin
    retiro_service = CorresponsalService(db)
    return retiro_service.obtener_total_dia_corresponsal(corresponsal_id)


@router.get(
    "/",
    response_model=CorresponsalListResponse,
    description="Obtiene la lista completa de corresponsales",
)
async def listar_corresponsales(
    db: Session = Depends(get_db),
    current_user: UsuarioModel = Depends(get_current_user),
):
    corresponsal_service = CorresponsalService(db)
    return corresponsal_service.listar_corresponsales()
