from pydantic import BaseModel, Field, ValidationError
from typing import List, Any, Optional, Dict, Type
from fastapi import HTTPException, status


class BaseErrorContext(BaseModel):
    """Base schema for validation error context."""

    ge: Optional[int] = Field(None, description="Valor mínimo permitido")
    decimal_places: Optional[int] = Field(
        None, description="Número de decimales permitidos"
    )
    max_length: Optional[int] = Field(None, description="Longitud máxima permitida")

    def get_error_message(self) -> str:
        """Retorna el mensaje de error en español basado en el contexto."""
        if self.ge is not None:
            return f"El valor debe ser mayor o igual a {self.ge}"
        return ""


class BaseErrorSchema(BaseModel):
    """Base schema for validation error details."""

    type: str = Field(..., description="Tipo de error")
    loc: List[str] = Field(..., description="Ubicación del error")
    msg: str = Field(..., description="Mensaje de error")
    input: Any = Field(..., description="Valor de entrada que causó el error")
    ctx: BaseErrorContext = Field(
        default_factory=BaseErrorContext, description="Contexto del error"
    )

    def get_localized_message(self) -> str:
        """Retorna el mensaje de error localizado en español."""
        if self.ctx.get_error_message():
            return self.ctx.get_error_message()
        return self.msg


class BaseErrorResponse(BaseModel):
    """Base schema for validation error response."""

    detail: List[BaseErrorSchema] = Field(
        ..., description="Lista de errores de validación"
    )


def translate_validation_error(error: ValidationError) -> BaseErrorResponse:
    """Traduce los errores de validación al español."""
    error_messages = {
        "greater_than_equal": "El valor debe ser mayor o igual a {ge}",
        "less_than_equal": "El valor debe ser menor o igual a {le}",
        "decimal_places": "El número debe tener máximo {decimal_places} decimales",
        "max_length": "La longitud máxima permitida es {max_length}",
    }

    translated_errors = []
    for err in error.errors():
        error_type = err["type"]
        ctx = err.get("ctx", {})

        if error_type in error_messages:
            msg = error_messages[error_type].format(**ctx)
        else:
            msg = err["msg"]

        translated_errors.append(
            BaseErrorSchema(
                type=error_type,
                loc=err["loc"],
                msg=msg,
                input=err["input"],
                ctx=BaseErrorContext(**ctx),
            )
        )

    return BaseErrorResponse(detail=translated_errors)
