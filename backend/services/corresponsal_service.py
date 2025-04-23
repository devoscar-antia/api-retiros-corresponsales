from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import CorresponsalModel, RetiroModel
from sqlalchemy import func
from datetime import datetime
from globals.retiro_vars import RETIRO_RANGO_DESDE, RETIRO_RANGO_HASTA


class CorresponsalService:
    def __init__(self, db: Session):
        self.db = db
        
    def obtener_total_dia_corresponsal(self, corresponsal_id: int) -> dict:
            # Verificar que el corresponsal existe
            corresponsal = self.db.query(CorresponsalModel).filter(
                CorresponsalModel.id == corresponsal_id
            ).first()
            
            if not corresponsal:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Corresponsal no encontrado"
                )

            fecha_actual = datetime.now().date()
            fecha_hora_inicio = datetime.combine(fecha_actual, RETIRO_RANGO_DESDE)
            fecha_hora_fin = datetime.combine(fecha_actual, RETIRO_RANGO_HASTA)
            
            # Calcular la suma de retiros del día para este corresponsal
            suma_retiros = self.db.query(func.sum(RetiroModel.monto))\
                .filter(
                    RetiroModel.corresponsal_id == corresponsal_id,
                    RetiroModel.fecha_hora >= fecha_hora_inicio,
                    RetiroModel.fecha_hora <= fecha_hora_fin
                ).scalar() or 0
            
            # Calcular el número total de retiros
            total_retiros = self.db.query(func.count(RetiroModel.id))\
                .filter(
                    RetiroModel.corresponsal_id == corresponsal_id,
                    RetiroModel.fecha_hora >= fecha_hora_inicio,
                    RetiroModel.fecha_hora <= fecha_hora_fin
                ).scalar() or 0
            
            return {
                "corresponsal_id": corresponsal_id,
                "fecha": fecha_actual.isoformat(),
                "monto_total": suma_retiros,
                "tope_diario": corresponsal.tope_diario,
                "monto_disponible": corresponsal.tope_diario - suma_retiros,
                "total_retiros": total_retiros
            }
            
    def listar_corresponsales(self) -> List[CorresponsalModel]:
        """
        Lista todos los corresponsales
        """
        return self.db.query(CorresponsalModel).all()