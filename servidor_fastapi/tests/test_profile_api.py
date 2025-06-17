# coding: utf-8

from fastapi.testclient import TestClient


from typing import Any, List  # noqa: F401
from model.dto.purchase import Purchase  # noqa: F401
from model.dto.user_profile import UserProfile  # noqa: F401
from model.dto.user_profile_update import UserProfileUpdate  # noqa: F401


def test_profile_get(client: TestClient):
    """Test case for profile_get

    Obtener los datos del perfil
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/profile",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_profile_purchases_get(client: TestClient):
    """Test case for profile_purchases_get

    Ver mis compras
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/profile/purchases",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_profile_put(client: TestClient):
    """Test case for profile_put

    Actualizar el perfil
    """
    user_profile_update = {"display_name":"displayName","image_url":"https://openapi-generator.tech"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/profile",
    #    headers=headers,
    #    json=user_profile_update,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

