from pydantic import Field
from typing import List
from schemas.errors.base_error_schema import BaseErrorSchema, BaseErrorResponse


class RetiroErrorSchema(BaseErrorSchema):
    """Schema for retiro validation error details."""

    pass


class RetiroErrorResponse(BaseErrorResponse):
    """Schema for retiro validation error response."""

    detail: List[RetiroErrorSchema] = Field(
        ..., description="Lista de errores de validación"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": [
                    {
                        "type": "greater_than_equal",
                        "loc": ["body", "monto"],
                        "msg": "Input should be greater than or equal to 10000",
                        "input": 100,
                        "ctx": {"ge": 10000},
                    },
                    {
                        "type": "decimal_places",
                        "loc": ["body", "monto"],
                        "msg": "Input should have at most 2 decimal places",
                        "input": "100.123",
                        "ctx": {"decimal_places": 2},
                    },
                    {
                        "type": "foreign_key_violation",
                        "loc": ["body", "corresponsal_id"],
                        "msg": "Foreign key constraint failed",
                        "input": 99999,
                        "ctx": {},
                    },
                ]
            }
        }
    }
