from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from .base_model import Base

class CorresponsalModel(Base):
    __tablename__ = "corresponsales"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    tope_diario = Column(Numeric(11, 2), nullable=False)

    # Relaciones
    retiros = relationship("RetiroModel", back_populates="corresponsal")

    def __repr__(self):
        return f"<Corresponsal {self.nombre}>" 