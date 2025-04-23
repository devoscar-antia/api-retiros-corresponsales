from fastapi import HTTPException, status
from datetime import datetime, time, timezone, timedelta
from sqlalchemy.orm import Session
from models.usuario_model import UsuarioModel
from globals.retiro_vars import (
    ERROR_MESSAGE_7AMPM, ERROR_MESSAGE_MONTO, RETIRO_PERMITIDO_DESDE, RETIRO_PERMITIDO_HASTA, USUARIO_MINUTOS_BLOQUEO
)

def raise_validar_hora_retiro_v1(hora: datetime):
    if not (7 <= hora.hour < 19):
        if hora.hour == 19:
            # if hora.minute > 0 or hora.second > 0 or hora.microsecond > 0:
            if hora.minute > 0 or hora.second > 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ERROR_MESSAGE_7AMPM
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGE_7AMPM
            )


def raise_validar_hora_retiro_v2(hora: datetime):
    if not (RETIRO_PERMITIDO_DESDE <= hora.time() <= RETIRO_PERMITIDO_HASTA):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGE_7AMPM
        )
        

def raise_validar_monto_retiro(monto: float):
    if not (10_000 <= monto <= 1_000_000):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGE_MONTO
        )
        
        
def manejar_intento_fallido(db: Session, id_usuario: int, error_detail: str = "Error en la operación"):
    """
    Maneja la lógica de intentos fallidos y bloqueo de usuario
    """
    user_to_update = db.query(UsuarioModel).filter(UsuarioModel.id == id_usuario).first()
    intentos = user_to_update.incrementar_intentos_fallidos()
    
    if intentos >= 3:
        db.commit()
        error_response = {
            "message": f"Usuario bloqueado por exceder el número máximo de intentos. Vuelva en {USUARIO_MINUTOS_BLOQUEO} {'minutos' if USUARIO_MINUTOS_BLOQUEO > 1 else 'minuto'}.",
            "intentos": 3
        }
        return HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail=error_response
        )
    
    db.commit()
    error_response = {
        "message": error_detail,
        "intentos": user_to_update.intentos_fallidos
    }
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=error_response
    )

