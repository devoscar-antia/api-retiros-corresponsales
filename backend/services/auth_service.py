from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from models import UsuarioModel
from schemas.responses.auth_schema import TokenSchema, LoginSchema
from auth.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
)


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def login(self, credentials: LoginSchema) -> TokenSchema:
        """
        Autentica al usuario y genera un token de acceso
        - credentials: Credenciales del usuario (correo y clave)
        """
        user = authenticate_user(self.db, credentials.correo, credentials.clave)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o clave incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.correo}, expires_delta=access_token_expires
        )

        return TokenSchema(access_token=access_token, token_type="bearer")
