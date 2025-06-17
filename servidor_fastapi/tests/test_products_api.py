# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictStr, field_validator  # noqa: F401
from typing import Any, List, Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from model.dto.comment import Comment  # noqa: F401
from model.dto.comment_input import CommentInput  # noqa: F401
from model.dto.product import Product  # noqa: F401
from model.dto.product_input import ProductInput  # noqa: F401


def test_products_get(client: TestClient):
    """Test case for products_get

    Listar productos
    """
    params = [("search", 'search_example'),     ("category", 'category_example')]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/products",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_products_post(client: TestClient):
    """Test case for products_post

    Subir un nuevo producto (solo artista)
    """
    product_input = {"price":0.8008282,"image_url":"imageUrl","name":"name","description":"description","category":"vinilos"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/products",
    #    headers=headers,
    #    json=product_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_products_product_id_comments_post(client: TestClient):
    """Test case for products_product_id_comments_post

    Agregar un comentario al producto
    """
    comment_input = {"text":"text"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/products/{productId}/comments".format(productId='product_id_example'),
    #    headers=headers,
    #    json=comment_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_products_product_id_delete(client: TestClient):
    """Test case for products_product_id_delete

    Eliminar producto (solo artista)
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/products/{productId}".format(productId='product_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_products_product_id_get(client: TestClient):
    """Test case for products_product_id_get

    Obtener detalle de un producto
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/products/{productId}".format(productId='product_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_products_product_id_put(client: TestClient):
    """Test case for products_product_id_put

    Actualizar un producto (solo artista)
    """
    product_input = {"price":0.8008282,"image_url":"imageUrl","name":"name","description":"description","category":"vinilos"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/products/{productId}".format(productId='product_id_example'),
    #    headers=headers,
    #    json=product_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

