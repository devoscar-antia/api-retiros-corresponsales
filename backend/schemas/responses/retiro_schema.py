from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime
from typing import Optional


class RetiroBaseSchema(BaseModel):
    """Base model for Retiro with basic fields."""

    corresponsal_id: int = Field(
        ...,
        description="ID del corresponsal",
        example=1,
        ge=1,
        error_messages={
            "type_error": "El ID del corresponsal debe ser un número entero",
            "int_parsing": "El ID del corresponsal debe ser un número entero válido",
            "ge": "El ID del corresponsal debe ser mayor o igual a 1",
        },
    )

    monto: Decimal = Field(
        ...,
        ge=10000,
        decimal_places=2,
        description="Monto del retiro en pesos colombianos",
        example=Decimal("100000.00"),
        error_messages={
            "type_error": "El monto debe ser un número decimal",
            "decimal_parsing": "El monto debe ser un número decimal válido",
            "ge": "El monto debe ser mayor o igual a 10,000",
            "decimal_places": "El monto debe tener máximo 2 decimales",
        },
    )
    canal_atencion: Optional[str] = Field(
        None,
        max_length=50,
        description="Canal de atención del retiro",
        example="ventanilla",
        error_messages={
            "type_error": "El canal de atención debe ser una cadena de texto",
            "max_length": "El canal de atención no puede exceder los 50 caracteres",
        },
    )

    fecha_hora: datetime = Field(
        ...,
        description="Fecha y hora del retiro",
        example="2025-04-22T07:30:00",
        error_messages={
            "type_error": "La fecha y hora debe ser una fecha válida",
            "datetime_parsing": "La fecha y hora debe tener un formato válido (YYYY-MM-DDTHH:MM:SS)",
        },
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
