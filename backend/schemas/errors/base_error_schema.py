from pydantic import BaseModel, Field
from typing import List, Any, Optional


class BaseErrorContext(BaseModel):
    """Base schema for validation error context."""

    ge: Optional[int] = Field(None, description="Valor mínimo permitido")
    decimal_places: Optional[int] = Field(
        None, description="Número de decimales permitidos"
    )
    max_length: Optional[int] = Field(None, description="Longitud máxima permitida")


class BaseErrorSchema(BaseModel):
    """Base schema for validation error details."""

    type: str = Field(..., description="Tipo de error")
    loc: List[str] = Field(..., description="Ubicación del error")
    msg: str = Field(..., description="Mensaje de error")
    input: Any = Field(..., description="Valor de entrada que causó el error")
    ctx: BaseErrorContext = Field(
        default_factory=BaseErrorContext, description="Contexto del error"
    )


class BaseErrorResponse(BaseModel):
    """Base schema for validation error response."""

    detail: List[BaseErrorSchema] = Field(
        ..., description="Lista de errores de validación"
    )
