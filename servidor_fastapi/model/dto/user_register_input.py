from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserRegisterInput(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    password: str = Field(..., description="Contraseña del usuario")
    username: str = Field(..., description="Nombre de usuario")
    tipo_usuario: str = Field(..., description="Tipo de usuario (usuario | artista)")
    nombre_banda: Optional[str] = Field(None, description="Nombre de la banda (solo para artistas)")