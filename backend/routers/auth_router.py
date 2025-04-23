from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.responses.auth_schema import TokenSchema, LoginSchema
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/token",
    response_model=TokenSchema,
    summary="Iniciar sesión",
    description="Obtiene un token de acceso usando correo y clave",
    responses={
        200: {
            "description": "Token de acceso generado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer",
                    }
                }
            },
        },
        401: {
            "description": "Credenciales inválidas",
            "content": {
                "application/json": {
                    "example": {"detail": "Correo o clave incorrectos"}
                }
            },
        },
    },
)
async def login_for_access_token(
    credentials: LoginSchema, db: Session = Depends(get_db)
):
    """
    Endpoint para iniciar sesión y obtener un token de acceso
    """
    auth_service = AuthService(db)
    return auth_service.login(credentials)
