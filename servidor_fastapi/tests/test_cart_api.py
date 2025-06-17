# coding: utf-8

from fastapi.testclient import TestClient

from pydantic import StrictStr  # noqa: F401
from typing import Any, List  # noqa: F401
from model.dto.add_to_cart_input import AddToCartInput  # noqa: F401
from model.dto.cart_item import CartItem  # noqa: F401
from model.dto.cart_item_id_patch_request import CartItemIdPatchRequest  # noqa: F401


def test_cart_delete(client: TestClient):
    """Test case for cart_delete

    Vaciar el carrito
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/cart",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_cart_get(client: TestClient):
    """Test case for cart_get

    Obtener el contenido del carrito actual
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/cart",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_cart_item_id_delete(client: TestClient):
    """Test case for cart_item_id_delete

    Eliminar un producto del carrito
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/cart/{itemId}".format(itemId='item_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_cart_item_id_patch(client: TestClient):
    """Test case for cart_item_id_patch

    Actualizar la cantidad de un producto en el carrito
    """
    
    cart_item_id_patch_request = CartItemIdPatchRequest()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PATCH",
    #    "/cart/{itemId}".format(itemId='item_id_example'),
    #    headers=headers,
    #    json=cart_item_id_patch_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_cart_post(client: TestClient):
    """Test case for cart_post

    Añadir un producto al carrito
    """
    add_to_cart_input = {"quantity":1,"product_id":"productId"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/cart",
    #    headers=headers,
    #    json=add_to_cart_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

