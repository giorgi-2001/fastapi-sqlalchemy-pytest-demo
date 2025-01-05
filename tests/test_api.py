import pytest
from fastapi.testclient import TestClient
import json


BASE_URL = "http://localhost:8000/api/v1/products"


@pytest.mark.parametrize(
    "name, description, valid", [
        ("item", "description", True),
        ("item"*50, "description", False),
        ("item", None, False),
        (None, "description", False),
        (None, "", False),
        ("", "description", False),
    ]
)
def test_add_product(client: TestClient, product_data, name, description, valid):
    data = product_data(name, description)
    response = client.post(BASE_URL, json=data)
    message = response.json()

    assert message is not None

    if valid:
        assert response.status_code == 201
        assert message["detail"] == "Product 1 was added"
    else:
        assert response.status_code == 422


def test_add_product_dublicate_names(client, product_data):
    data = product_data("item", "description")
    response = client.post(BASE_URL, json=data)
    message = response.json()

    assert response.status_code == 409
    assert message["detail"] == "Product already exists"


def test_get_products(client):
    response = client.get(BASE_URL)
    products = response.json()

    assert response.status_code == 200
    assert products is not None


def test_get_product_by_id(client):
    response = client.get(BASE_URL + "/1")
    product = response.json()

    assert response.status_code == 200
    assert product["name"] == "item"
    assert product["description"] == "description"


def test_get_product_by_id_404(client):
    response = client.get(BASE_URL + "/5")
    message = response.json()

    assert response.status_code == 404
    assert message["detail"] == "Not Found"


@pytest.mark.parametrize(
    "id, name, description, match", [
        (1, "item2", "description", "success"),
        (1, "item", "description2", "success"),
        (1, "", "description", "invalid"),
        (1, None, "description", "invalid"),
        (1, "item2", None, "invalid"),
        (5, "item2", "description", "404"),
    ]
)
def test_update_product(client, product_data, id, name, description, match):
    data = product_data(name, description)
    response = client.put(BASE_URL + f"/{id}", json=data)
    message = response.json()
    match match:
        case "success":
            assert response.status_code == 200
            assert message["detail"] == f"Product {id} was updated"
        case "invalid":
            assert response.status_code == 422
            assert message is not None
        case "404":
            assert response.status_code == 404
            assert message["detail"] == "Not Found"


def test_update_product_with_dublicate(client, product_data):
    dublicate = product_data("dublicate", "dublicate")
    data = dublicate.copy()

    client.post(BASE_URL, json=dublicate)
    response = client.put(BASE_URL + "/1", json=dublicate)
    message = response.json()

    assert response.status_code == 409
    assert message["detail"] == "Product already exists"


def test_delete_product(client):
    response = client.delete(BASE_URL + "/1")
    message = response.json()

    assert response.status_code == 200
    assert message["detail"] == "Product 1 was removed"


def test_delete_product_404(client):
    response = client.delete(BASE_URL + "/5")
    message = response.json()

    assert response.status_code == 404
    assert message["detail"] == "Not Found"
