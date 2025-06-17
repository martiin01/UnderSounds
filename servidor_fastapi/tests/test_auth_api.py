# coding: utf-8

from fastapi.testclient import TestClient


from typing import Any  # noqa: F401
from model.dto.auth_login_post200_response import AuthLoginPost200Response  # noqa: F401
from model.dto.user_login_input import UserLoginInput  # noqa: F401
from model.dto.user_profile import UserProfile  # noqa: F401
from model.dto.user_register_input import UserRegisterInput  # noqa: F401


def test_auth_login_post(client: TestClient):
    """Test case for auth_login_post

    Iniciar sesión
    """
    user_login_input = {"password":"password","email":"email"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/auth/login",
    #    headers=headers,
    #    json=user_login_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_auth_logout_post(client: TestClient):
    """Test case for auth_logout_post

    Cerrar sesión
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/auth/logout",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_auth_register_post(client: TestClient):
    """Test case for auth_register_post

    Registrar un nuevo usuario (sea normal o artista)
    """
    user_register_input = {"password":"password","role":"role","display_name":"displayName","email":"email"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/auth/register",
    #    headers=headers,
    #    json=user_register_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

