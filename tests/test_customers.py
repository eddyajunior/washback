import uuid

def test_access_with_corrupted_token(client):

    response = client.get(
        "/customers/1",
        headers={
            "Authorization": "Bearer abc.def.xyz"
        }
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 401
    
def test_access_with_malformed_authorization_header(client):

    response = client.get(
        "/customers/1",
        headers={
            "Authorization": "Token abc123"
        }
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 401

def test_access_with_empty_token(client):

    response = client.get(
        "/customers/1",
        headers={
            "Authorization": "Bearer "
        }
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 401

# def test_access_with_invalid_token(client):

#     response = client.get(
#         "/customers/1",
#         headers={
#             "Authorization": "Bearer token_invalido"
#         }
#     )

#     print(response.status_code)
#     print(response.json())

#     assert response.status_code == 401

def test_access_with_invalid_token(client):

    response = client.get(
        "/customers/1",
        headers={
            "Authorization": "Bearer token_invalido"
        }
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 401

def test_access_without_token(client):

    response = client.get(
        "customers/1"
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 401

def test_customer_fixture(customer_created):

    assert customer_created["id"] > 0
    assert customer_created["name"] == "Cliente Fixture"

def test_list_customers_only_from_current_company(
    client,
    auth_headers_company2
):

    response = client.get(
        "/customers?page=1&limit=100",
        headers=auth_headers_company2
    )

    assert response.status_code == 200

    body = response.json()

    print(body)

def test_customer_isolation_between_companies(
    client,
    auth_headers_company2
):

    response = client.get(
        "/customers/1",
        headers=auth_headers_company2
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code in [403, 404]

def test_list_customers_empty_page(client, auth_headers):

    response = client.get(
        "/customers/?page=9999&size=10", 
        headers=auth_headers
        )
    
    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Clientes listados com sucesso."
    assert body["data"]["pagination"]["total"] >= 0
    assert body["data"]["pagination"]["limit"] == 10
    assert len(body["data"]["items"]) == 0

def test_list_customers_paginated(client, auth_headers, customer_created):

    response = client.get(
        "/customers/?page=1&size=10", 
        headers=auth_headers
        )
    
    print(response.status_code)
    print(response.json())

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Clientes listados com sucesso."
    assert body["data"]["pagination"]["total"] > 0
    assert body["data"]["pagination"]["page"] == 1
    assert body["data"]["pagination"]["page"] > 0
    assert body["data"]["pagination"]["limit"] == 10
    assert len(body["data"]["items"]) > 0
    assert any(customer["id"] > 0 for customer in body["data"]["items"])


def test_delete_customer_not_found(client, auth_headers, customer_created):

    customer_created_id = customer_created["id"] + 1000

    response = client.delete(
        f"/customers/{customer_created_id}", 
        headers=auth_headers
        )

    assert response.status_code == 204


def test_delete_customer_success(client, auth_headers, customer_created):

    customer_created_id = customer_created["id"]

    response = client.delete(
        f"/customers/{customer_created_id}", 
        headers=auth_headers
        )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Cliente excluído com sucesso."

    response_get = client.get(
        f"/customers/{customer_created_id}", 
        headers=auth_headers
        )

    assert response_get.status_code == 404

def test_get_customer_success(client, auth_headers, customer_created):

    customer_created_id = customer_created["id"]

    response = client.get(
        f"/customers/{customer_created_id}", 
        headers=auth_headers
        )

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Cliente encontrado com sucesso"

def test_get_customer_not_found(client, auth_headers, customer_created):

    customer_created_id = customer_created["id"]

    response = client.get(
        f"/customers/{customer_created_id + 10000}", 
        headers=auth_headers
        )

    assert response.status_code == 404

    body = response.json()

    assert body["success"] is False
    assert body["message"] == "Cliente não encontrado."

def test_create_customer_success(client, auth_headers):
    payload = {   
        "name": "Cliente Teste Pytest",   
        "phone": "1199999999",   
        "car_plate": f"PY{uuid.uuid4().hex[:5].upper()}",   
        "car_model": "Gol" 
    }

    response = client.post(
        "/customers/", 
        json=payload, 
        headers=auth_headers
        )
    
    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Cliente criado com sucesso"

def test_create_car_plate_exists(client, auth_headers, customer_created):

    customer_created_car_plate = customer_created["car_plate"]

    payload = {   
        "name": "Cliente Teste Pytest",   
        "phone": "1199999999",   
        "car_plate": customer_created_car_plate,
        "car_model": "Gol" 
    }

    response = client.post(
        "/customers/", 
        json=payload, 
        headers=auth_headers
        )
    
    assert response.status_code == 422

    body = response.json()

    assert body["success"] is False
    assert body["message"] == "Já existe um cliente com essa placa."

def test_update_customer_success(client, auth_headers, customer_created):

    customer_id = customer_created["id"]

    payload = {   
        "id": customer_id,
        "name": f"{customer_created['name']} - Atualizado",   
        "phone": customer_created["phone"],
        "car_plate": customer_created["car_plate"],
        "car_model": customer_created["car_model"]
    }

    response = client.put(
        f"/customers/{customer_id}", 
        json=payload, 
        headers=auth_headers
    )

    assert response.status_code == 200

    body = response.json()  

    assert body["success"] is True
    assert body["message"] == "Cliente atualizado com sucesso."

    assert body["data"]["name"] == payload["name"]
    assert body["data"]["phone"] == payload["phone"]
    assert body["data"]["car_plate"] == payload["car_plate"]
    assert body["data"]["car_model"] == payload["car_model"]

def test_update_customer_not_found(client, auth_headers, customer_created):

    customer_id = customer_created["id"] + 10000

    payload = {   
        "id": customer_id,
        "name": "Cliente Teste Pytest - Atualizado",   
        "phone": "1199999999",
        "car_plate": "PYB755C",
        "car_model": "Gol"
    }

    response = client.put(
        f"/customers/{customer_id}", 
        json=payload, 
        headers=auth_headers
    )

    print(response.json())

    assert response.status_code == 404

    body = response.json()  

    assert body["success"] is False
    assert "não encontrado" in body["message"].lower()