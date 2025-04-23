from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import Optional


class RetiroBaseSchema(BaseModel):
    """Base model for Retiro with basic fields."""

    corresponsal_id: int = Field(
        ..., description="ID del corresponsal", example=1, ge=1
    )

    monto: Decimal = Field(
        ...,
        ge=10000,
        decimal_places=2,
        description="Monto del retiro en pesos colombianos",
        example=Decimal("100000.00"),
    )
    canal_atencion: Optional[str] = Field(
        None,
        max_length=50,
        description="Canal de atención del retiro",
        example="ventanilla",
    )

    fecha_hora: datetime = Field(
        ..., description="Fecha y hora del retiro", example="2025-04-22T07:30:00"
    )


class RetiroCreateSchema(RetiroBaseSchema):
    """Model for creating a new Retiro."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "corresponsal_id": 1,
                "monto": "100000.00",
                "fecha_hora": "2025-04-22T07:30:00",
                "canal_atencion": "ventanilla",
            }
        }
    )


class RetiroInDBSchema(RetiroBaseSchema):
    """Model for Retiro as stored in the database."""

    usuario_id: int = Field(
        ..., description="ID del usuario que creó el retiro", example=1
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "corresponsal_id": 1,
                "monto": "100000.00",
                "fecha_hora": "2025-04-22T07:30:00",
                "canal_atencion": "ventanilla",
                "usuario_id": 1,
            }
        },
    )
