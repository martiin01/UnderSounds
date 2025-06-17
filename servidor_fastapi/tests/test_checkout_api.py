# coding: utf-8

from fastapi.testclient import TestClient


from typing import Any  # noqa: F401
from model.dto.checkout_input import CheckoutInput  # noqa: F401


def test_checkout_post(client: TestClient):
    """Test case for checkout_post

    Realizar la compra (pantalla de pago)
    """
    checkout_input = {"address":"address","payment_method":"paymentMethod"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/checkout",
    #    headers=headers,
    #    json=checkout_input,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

