from pydantic import BaseModel, EmailStr, Field


class LoginForm(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico válido")
    password: str = Field(..., min_length=6, description="Contraseña")
