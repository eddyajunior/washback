
from fastapi.testclient import TestClient
from app.main import app

import uuid
import pytest 

@pytest.fixture
def auth_headers_company(
    client
    ):

    email = f"empresa2_{uuid.uuid64().hex[:8]}@teste.com"

    client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "123456"
        }
    )

    login = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "123456"
        }
    )

    token = login.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture
def wash_created(
    client,
    auth_headers,
    customer_created
):
    payload = {
        "customer_id": customer_created["id"],
        "wash_type": "Simples",
        "price": 50
    }

    response = client.post(
        "/washes/",
        json=payload,
        headers=auth_headers
    )

    assert response.status_code == 201

    return response.json()["data"]


@pytest.fixture
def auth_headers_company2(client):
    password = "123456"
    email = f"empresa2_{uuid.uuid4().hex[:8]}@example.com"

    register = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password
        }
    )

    assert register.status_code in [200, 201], register.json()

    login = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    assert login.status_code == 200, login.json()

    token = login.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }

@pytest.fixture
def customer_created(
    client,
    auth_headers
):
    payload = {
        "name": "Cliente Fixture",
        "phone": "11999999999",
        "car_plate": f"TST{uuid.uuid4().hex[:4].upper()}",
        "car_model": "Gol"
    }

    response = client.post(
        "/customers/",
        json=payload,
        headers=auth_headers
    )

    assert response.status_code == 201

    return response.json()["data"]

# @pytest.fixture
# def client():
#     return TestClient(app)

# @pytest.fixture
# def auth_headers(client):


#     login_response = client.post(
#         "/auth/login",
#         json={
#         	"email": "edson@empresa1.com",
#     	"password": "1234"
#         }
#     )

#     token = login_response.json().get("access_token")

#     return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def unique_email():
    return f"teste_{uuid.uuid4().hex[:8]}@example.com"


@pytest.fixture
def auth_headers(client, unique_email):
    password = "123456"

    register_response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "password": password
        }
    )

    assert register_response.status_code in [200, 201]

    login_response = client.post(
        "/auth/login",
        json={
            "email": unique_email,
            "password": password
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }