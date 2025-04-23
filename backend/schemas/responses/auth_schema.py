from pydantic import BaseModel, EmailStr, Field

class LoginSchema(BaseModel):
    """Schema para las credenciales de inicio de sesión"""
    correo: EmailStr = Field(..., description="Correo electrónico del usuario", example="oscar@hotmail.com")
    clave: str = Field(..., min_length=8, description="Clave del usuario", example="Oscar123!")

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class TokenDataSchema(BaseModel):
    correo: str | None = None 