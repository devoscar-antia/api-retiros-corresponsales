from pydantic import BaseModel
from typing import List, Optional


class ValidationErrorSchema(BaseModel):
    loc: List[str]
    msg: str
    type: str


class ValidationErrorResponse(BaseModel):
    detail: List[ValidationErrorSchema]
