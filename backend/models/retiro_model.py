from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from .base_model import Base

class RetiroModel(Base):
    __tablename__ = "retiros"

    id = Column(Integer, primary_key=True, index=True)
    corresponsal_id = Column(Integer, ForeignKey("corresponsales.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    monto = Column(Numeric(10, 2), nullable=False)
    fecha_hora = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    canal_atencion = Column(String(50), nullable=True)

    # Relaciones
    corresponsal = relationship("CorresponsalModel", back_populates="retiros")
    usuario = relationship("UsuarioModel", back_populates="retiros")

    def __repr__(self):
        return f"<Retiro {self.id}>" 