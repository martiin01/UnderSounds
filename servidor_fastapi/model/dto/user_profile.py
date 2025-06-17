from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserProfile(BaseModel):
    id: str = Field(..., description="Identificador único del usuario (Firebase UID)")
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    username: str = Field(..., description="Nombre de usuario")
    tipo_usuario: str = Field(..., description="Tipo de usuario (usuario | artista)")
    nombre_banda: Optional[str] = Field(None, description="Nombre de la banda (solo para artistas)")
    image_url: Optional[str] = Field(None, alias="imageUrl", description="URL de la imagen del perfil")