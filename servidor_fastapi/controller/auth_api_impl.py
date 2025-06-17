from controller.auth_api_base import BaseAuthApi
from model.dao.implementations.user_dao import UserDAO
from model.dto.user_profile import UserProfile
from model.dto.user_register_input import UserRegisterInput
from model.dto.user_login_input import UserLoginInput
from model.dto.auth_login_post200_response import AuthLoginPost200Response
from firebase_admin import auth as firebase_auth
from fastapi import HTTPException, status
import jwt
import os

# Clave secreta para generar tokens JWT (puedes mover esto a variables de entorno)
SECRET_KEY = os.getenv("xxxx", "xxxxx") # Cambia esto por una clave secreta segura
ALGORITHM = "HS256"

class AuthApiImpl(BaseAuthApi):
    async def auth_register_post(self, user_register_input: UserRegisterInput) -> UserProfile:
        """
        Registra un nuevo usuario en Firebase Authentication y en la base de datos local.
        """
        try:
            # Registrar al usuario en Firebase Authentication
            firebase_user = firebase_auth.create_user(
                email=user_register_input.email,
                password=user_register_input.password,
                display_name=user_register_input.username
            )
            print(f"Usuario registrado en Firebase con UID: {firebase_user.uid}")

            # Guardar información adicional en la base de datos local
            dao = UserDAO()
            user = UserProfile(
                id=firebase_user.uid,  # Usamos el UID de Firebase como ID
                username=user_register_input.username,
                email=user_register_input.email,
                tipo_usuario=user_register_input.tipo_usuario,
                nombre_banda=user_register_input.nombre_banda
            )
            dao.create_user(user)
            return user

        except firebase_auth.EmailAlreadyExistsError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo electrónico ya está registrado."
            )
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al registrar el usuario."
            )

    async def auth_login_post(self, user_login_input: UserLoginInput) -> AuthLoginPost200Response:
        """
        Inicia sesión validando las credenciales del usuario con Firebase Authentication.
        """
        try:
            # Validar las credenciales con Firebase Authentication
            firebase_user = firebase_auth.get_user_by_email(user_login_input.email)
            print(f"Usuario encontrado en Firebase con UID: {firebase_user.uid}")

            # Obtener los datos completos del usuario desde la base de datos local
            dao = UserDAO()
            try:
                user = dao.get_user_by_id(firebase_user.uid)
            except Exception as e:
                print(f"Error al obtener el usuario desde la base de datos: {e}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado en la base de datos local."
                )

            # Generar un token JWT para la sesión
            token = jwt.encode(
                {"uid": firebase_user.uid, "email": firebase_user.email},
                SECRET_KEY,
                algorithm=ALGORITHM
            )

            # Construir la respuesta con el DTO AuthLoginPost200Response
            return AuthLoginPost200Response(
                token=token,
                user=user  # Aquí pasamos el objeto UserProfile obtenido de la base de datos
            )

        except firebase_auth.UserNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas."
            )
        except Exception as e:
            print(f"Error al iniciar sesión: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al iniciar sesión."
            )