from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from fastapi import HTTPException, status
from models import UsuarioModel, RetiroModel, CorresponsalModel
from schemas.responses.retiro_schema import RetiroCreateSchema, RetiroInDBSchema
from globals.retiro_vars import (
    RETIRO_RANGO_DESDE,
    RETIRO_RANGO_HASTA,
)
from functions.retiro_validate import (
    manejar_intento_fallido,
    raise_validar_hora_retiro_v1,
    raise_validar_monto_retiro,
)
from sqlalchemy import func


class RetiroService:
    def __init__(self, db: Session):
        self.db = db

    def crear_retiro(
        self, retiro: RetiroCreateSchema, current_user: UsuarioModel
    ) -> RetiroInDBSchema:
        # Esta validacion la uso para evitar que aparezcan los intentos y
        # el baneo temporal si esta fuera del horario de retiro
        try:
            # Validar el horario del retiro desde el servidor fastapi
            # hora_actual = datetime.now()
            # temporal: fecha personalizada para pruebas
            # hora_actual = datetime(2100, 4, 21, 19, 0, 0)
            raise_validar_hora_retiro_v1(retiro.fecha_hora)

        except HTTPException as http_ex:
            raise http_ex

        # Verificar si el usuario está bloqueado
        if not current_user.puede_intentar_retiro():
            tiempo_restante = current_user.get_tiempo_bloqueo_restante()
            minutos, segundos = tiempo_restante
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail=f"Usuario bloqueado temporalmente. Intente en {minutos} minutos y {segundos} segundos.",
            )

        try:
            # Validar el monto del retiro
            raise_validar_monto_retiro(retiro.monto)

            # Obtener el corresponsal
            corresponsal = (
                self.db.query(CorresponsalModel)
                .filter(CorresponsalModel.id == retiro.corresponsal_id)
                .first()
            )

            if not corresponsal:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Corresponsal no encontrado",
                )

            # Validaciones de operaciones diarias y tope
            fecha_actual = datetime.now().date()
            fecha_hora_inicio = datetime.combine(fecha_actual, RETIRO_RANGO_DESDE)
            fecha_hora_fin = datetime.combine(fecha_actual, RETIRO_RANGO_HASTA)

            # Contar operaciones y validar límite
            numero_operaciones = (
                self.db.query(func.count(RetiroModel.id))
                .filter(
                    RetiroModel.corresponsal_id == retiro.corresponsal_id,
                    RetiroModel.fecha_hora >= fecha_hora_inicio,
                    RetiroModel.fecha_hora <= fecha_hora_fin,
                )
                .scalar()
                or 0
            )

            if numero_operaciones >= 100:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Jornada finalizada: no se puede hacer más retiros. Se ha alcanzado el límite de 100 operaciones diarias.",
                )

            # Validar tope diario
            suma_retiros = (
                self.db.query(func.sum(RetiroModel.monto))
                .filter(
                    RetiroModel.corresponsal_id == retiro.corresponsal_id,
                    RetiroModel.fecha_hora >= fecha_hora_inicio,
                    RetiroModel.fecha_hora <= fecha_hora_fin,
                )
                .scalar()
                or 0
            )

            if suma_retiros + retiro.monto > corresponsal.tope_diario:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El monto excede el tope diario del corresponsal. Tope restante: {corresponsal.tope_diario - suma_retiros}",
                )

            # Crear el nuevo retiro
            db_retiro = RetiroModel(
                corresponsal_id=retiro.corresponsal_id,
                usuario_id=current_user.id,
                monto=retiro.monto,
                fecha_hora=datetime.now(),
                canal_atencion=retiro.canal_atencion,
            )

            self.db.add(db_retiro)
            self.db.commit()
            self.db.refresh(db_retiro)

            # Si llegamos aquí, el retiro fue exitoso
            # Refrescar el objeto usuario desde la base de datos
            user_to_update = (
                self.db.query(UsuarioModel)
                .filter(UsuarioModel.id == current_user.id)
                .first()
            )
            # Reiniciar intentos al tener éxito
            user_to_update.reiniciar_intentos_fallidos()
            self.db.commit()
            return db_retiro

        except HTTPException as http_ex:
            self.db.rollback()
            raise manejar_intento_fallido(self.db, current_user.id, http_ex.detail)

        except Exception as e:
            self.db.rollback()
            raise manejar_intento_fallido(
                self.db, current_user.id, "Error interno del servidor"
            )

    def listar_retiros(
        self, current_user: UsuarioModel, skip: int = 0, limit: int = 10
    ) -> List[RetiroInDBSchema]:
        retiros = (
            self.db.query(RetiroModel)
            .filter(RetiroModel.usuario_id == current_user.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return retiros

    def obtener_retiro(
        self, retiro_id: int, current_user: UsuarioModel
    ) -> RetiroInDBSchema:
        retiro = (
            self.db.query(RetiroModel)
            .filter(
                RetiroModel.id == retiro_id, RetiroModel.usuario_id == current_user.id
            )
            .first()
        )

        if retiro is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Retiro no encontrado"
            )

        return retiro
