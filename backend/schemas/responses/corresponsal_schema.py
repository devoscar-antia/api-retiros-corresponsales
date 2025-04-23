from pydantic import BaseModel, Field, field_validator, RootModel, ConfigDict
from decimal import Decimal
from typing import List


class CorresponsalBaseSchema(BaseModel):
    """Base model for Corresponsal with basic fields."""

    nombre: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre del corresponsal",
        example="Corresponsal La Estrella - Medellín",
    )
    tope_diario: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
        description="Límite máximo de retiros permitido por día",
        example=Decimal("75000000.00"),
    )

    @field_validator("tope_diario")
    @classmethod
    def validate_tope_diario(cls, v):
        return round(v, 2)


class CorresponsalCreateSchema(CorresponsalBaseSchema):
    """Model for creating a new Corresponsal."""

    pass


class CorresponsalInDBSchema(CorresponsalBaseSchema):
    """Model for Corresponsal as stored in the database."""

    id: int = Field(..., description="ID único del corresponsal", example=1, ge=1)

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "nombre": "Corresponsal La Estrella - Medellín",
                "tope_diario": "75000000.00",
            },
            "list_example": [
                {
                    "id": 1,
                    "nombre": "Corresponsal La Estrella - Medellín",
                    "tope_diario": "75000000.00",
                },
                {
                    "id": 2,
                    "nombre": "Corresponsal El Poblado - Medellín",
                    "tope_diario": "50000000.00",
                },
                {
                    "id": 3,
                    "nombre": "Corresponsal Centro - Bogotá",
                    "tope_diario": "100000000.00",
                },
            ],
        },
    )


class CorresponsalListResponse(RootModel):
    """Model for list of Corresponsales response."""

    root: List[CorresponsalInDBSchema]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": [
                {
                    "id": 1,
                    "nombre": "Corresponsal La Estrella - Medellín",
                    "tope_diario": "75000000.00",
                },
                {
                    "id": 2,
                    "nombre": "Corresponsal El Poblado - Medellín",
                    "tope_diario": "50000000.00",
                },
                {
                    "id": 3,
                    "nombre": "Corresponsal Centro - Bogotá",
                    "tope_diario": "100000000.00",
                },
            ]
        },
    )


class CorresponsalTotalDiaSchema(BaseModel):
    """Model for Corresponsal's daily total information."""

    corresponsal_id: int = Field(
        ..., description="ID del corresponsal", example=1, ge=1
    )
    fecha: str = Field(
        ..., description="Fecha del reporte en formato YYYY-MM-DD", example="2025-04-22"
    )
    monto_total: float = Field(
        ..., description="Monto total de retiros del día", example=1520000.0
    )
    tope_diario: float = Field(
        ...,
        description="Límite máximo de retiros permitido por día",
        example=75000000.0,
    )
    monto_disponible: float = Field(
        ...,
        description="Monto disponible para retiros restante del día",
        example=73480000.0,
    )
    total_retiros: int = Field(
        ..., description="Cantidad total de retiros realizados en el día", example=100
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "corresponsal_id": 1,
                "fecha": "2025-04-22",
                "monto_total": 1520000.0,
                "tope_diario": 75000000.0,
                "monto_disponible": 73480000.0,
                "total_retiros": 100,
            },
            "error_responses": {
                422: {
                    "description": "Error de validación",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": [
                                    {
                                        "type": "int_parsing",
                                        "loc": ["path", "corresponsal_id"],
                                        "msg": "Input should be a valid integer, unable to parse string as an integer",
                                        "input": "1x",
                                    }
                                ]
                            }
                        }
                    },
                }
            },
        },
    )
