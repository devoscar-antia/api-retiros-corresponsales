from pydantic import Field
from typing import List
from schemas.errors.base_error_schema import BaseErrorSchema, BaseErrorResponse


class CorresponsalErrorSchema(BaseErrorSchema):
    """Schema for corresponsal validation error details."""

    pass


class CorresponsalErrorResponse(BaseErrorResponse):
    """Schema for corresponsal validation error response."""

    detail: List[CorresponsalErrorSchema] = Field(
        ..., description="Lista de errores de validación"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": [
                    {
                        "type": "int_parsing",
                        "loc": ["path", "corresponsal_id"],
                        "msg": "Input should be a valid integer, unable to parse string as an integer",
                        "input": "1x",
                        "ctx": {},
                    },
                    {
                        "type": "string_too_long",
                        "loc": ["body", "nombre"],
                        "msg": "String should have at most 100 characters",
                        "input": "a" * 101,
                        "ctx": {"max_length": 100},
                    },
                    {
                        "type": "missing",
                        "loc": ["body", "nombre"],
                        "msg": "Field required",
                        "input": None,
                        "ctx": {},
                    },
                ]
            }
        }
    }
