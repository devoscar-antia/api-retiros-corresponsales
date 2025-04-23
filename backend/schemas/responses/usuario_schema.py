from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    bloqueado_hasta: datetime | None = None

class UsuarioCreate(UsuarioBase):
    clave: str

class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class UsuarioBaseSchema(BaseModel):
    """Base model for Usuario with basic fields."""
    nombre: str = Field(..., min_length=1, max_length=100)
    correo: EmailStr = Field(...)
    clave: str = Field(..., min_length=8)  # Se espera que venga ya encriptada

class UsuarioCreateSchema(UsuarioBaseSchema):
    """Model for creating a new Usuario."""
    pass

class UsuarioInDBSchema(UsuarioBaseSchema):
    """Model for Usuario as stored in the database."""
    id: int

    class Config:
        from_attributes = True

class UsuarioSchema(BaseModel):
    id: int
    nombre: str
    correo: str

    class Config:
        from_attributes = True 