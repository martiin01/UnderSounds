from fastapi import APIRouter, Body, HTTPException, Security
from model.dto.auth_login_post200_response import AuthLoginPost200Response
from model.dto.user_profile import UserProfile
from model.dto.user_register_input import UserRegisterInput
from model.dto.user_login_input import UserLoginInput
from model.extra.extra_models import TokenModel
from controller.auth_api_base import BaseAuthApi
from security.security_api import get_token_BearerAuth

router = APIRouter()

@router.post(
    "/auth/login",
    responses={
        200: {"model": AuthLoginPost200Response, "description": "Inicio de sesión exitoso"},
        401: {"description": "Credenciales inválidas"},
    },
    tags=["Auth"],
    summary="Iniciar sesión",
    response_model_by_alias=True,
)
async def auth_login_post(
    user_login_input: UserLoginInput = Body(..., description="Datos para iniciar sesión")
) -> AuthLoginPost200Response:
    """Inicia sesión validando las credenciales del usuario."""
    if not BaseAuthApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAuthApi.subclasses[0]().auth_login_post(user_login_input)


@router.post(
    "/auth/register",
    responses={
        201: {"model": UserProfile, "description": "Usuario registrado correctamente."},
        400: {"description": "Error de validación o usuario ya existente."},
    },
    tags=["Auth"],
    summary="Registrar un nuevo usuario (sea normal o artista)",
    response_model_by_alias=True,
)
async def auth_register_post(
    user_register_input: UserRegisterInput = Body(..., description="Datos para registrar un usuario")
) -> UserProfile:
    """Crea un nuevo usuario en la base de datos (Firebase + la BD local)."""
    if not BaseAuthApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAuthApi.subclasses[0]().auth_register_post(user_register_input)