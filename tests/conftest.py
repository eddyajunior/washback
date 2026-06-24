from urllib import response

from fastapi.testclient import TestClient
from app.main import app

import uuid
import pytest 
import random 
import string 

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
    auth_headers
):
    
    payload = {
        "customer_id": 1, #f"{uuid.uuid4().hex[:1]}",   
        "wash_type": "Simples",   
        "price": 50,   
        "notes": "Explaned note" 
    }
    
    response = client.post(
        "/washes",
        headers = auth_headers,
        json = payload
    )

    assert response.status_code == 200

    return response.json()["data"]


@pytest.fixture
def auth_headers_company2(client):

    login = client.post(
        "/auth/login",
        json={
            "email": "user4@example.com",
            "password": "1234"
        }
    )

    token = login.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }

@pytest.fixture
def customer_created(client, auth_headers):

    payload = {   
        "name": "Cliente Teste Pytest Fixture",   
        "phone": f"119{uuid.uuid4().hex[:8]}",   
        "car_plate": f"PYT{uuid.uuid4().hex[:4].upper()}",   
        "car_model": "Gol" 
    }

    response = client.post(
        "/customers/", 
        json=payload, 
        headers=auth_headers
        )
    
    assert response.status_code == 200

    return response.json()["data"]

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_headers(client):


    login_response = client.post(
        "/auth/login",
        json={
        	"email": "edson@empresa1.com",
    	"password": "1234"
        }
    )

    token = login_response.json().get("access_token")

    return {"Authorization": f"Bearer {token}"}