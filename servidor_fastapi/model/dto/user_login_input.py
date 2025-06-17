from pydantic import BaseModel, Field, EmailStr

class UserLoginInput(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    password: str = Field(..., description="Contraseña del usuario")