# coding: utf-8

#from typing import ClassVar, Dict, List, Tuple  # noqa: F401

#from typing import Any
#from openapi_server.models.auth_login_post200_response import AuthLoginPost200Response
#from openapi_server.models.user_login_input import UserLoginInput
#from openapi_server.models.user_profile import UserProfile
#from openapi_server.models.user_register_input import UserRegisterInput
#from openapi_server.security_api import get_token_BearerAuth
from typing import ClassVar, Tuple
#from openapi_server.models.auth_login_post200_response import AuthLoginPost200Response
from model.dto.auth_login_post200_response import AuthLoginPost200Response
from model.dto.user_profile import UserProfile
from model.extra.extra_models import TokenModel
from model.dto.user_register_input import UserRegisterInput
from model.dto.user_login_input import UserLoginInput


class BaseAuthApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseAuthApi.subclasses = BaseAuthApi.subclasses + (cls,)
    async def auth_login_post(
        self,
        user_login_input: UserLoginInput,
    ) -> AuthLoginPost200Response:
        """Devuelve un token JWT si las credenciales son correctas."""
        ...


    async def auth_logout_post(
        self,
    ) -> None:
        """Invalida el token o la sesión del usuario en Firebase (según tu implementación)."""
        ...


    async def auth_register_post(
        self,
        user_register_input: UserRegisterInput,
    ) -> UserRegisterInput:
        """Crea un nuevo usuario en la base de datos (Firebase + la BD local)."""
        ...
