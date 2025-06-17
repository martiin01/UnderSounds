# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import StrictStr  # noqa: F401
from typing import Any, List  # noqa: F401
from model.dto.comment import Comment  # noqa: F401
from model.dto.product import Product  # noqa: F401


def test_forum_artista_artist_id_albums_get(client: TestClient):
    """Test case for forum_artista_artist_id_albums_get

    Obtener la lista de álbumes de un artista
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/forum/artista/{artistId}/albums".format(artistId='artist_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_forum_artista_artist_id_opiniones_get(client: TestClient):
    """Test case for forum_artista_artist_id_opiniones_get

    Obtener lista de opiniones sobre un artista
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/forum/artista/{artistId}/opiniones".format(artistId='artist_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

