import uuid


def test_list_washes_empty_page(
        client,
        auth_headers
):
    
    response = client.get(
        "/washes?page=999&limit=10",
        headers=auth_headers
    )

    assert response.status_code == 200

def test_create_wash_without_token(
        client,
        customer_created
):
    
    response = client.post(
        "/washes/",
        json={
            "customer_id": customer_created["id"],
            "wash_type": "Simples",
            "price": 50
        }
    )

    assert response.status_code == 401

def test_create_wash_customer_not_found(
        client,
        auth_headers
):
    
    response = client.post(
        "/washes/",
        headers=auth_headers,
        json={
            "customer_id": 999999,
            "wash_type": "Simples",
            "price": 50
        }
    )

    assert response.status_code == 404

def test_create_wash_validation_error(
        client, 
        auth_headers
):
    
    response = client.post(
        "/washes",
        headers=auth_headers,
        json={}
    )

    assert response.status_code == 422

    body = response.json()

    assert body["success"] is False

def test_get_list_washes(
        client,
        auth_headers
):
    
    response = client.get(
        "/washes/?page=1&limit=10",
        headers = auth_headers
    )

    assert response.status_code == 200

def test_get_wash_by_id_not_found(
        client,
        auth_headers,
        wash_created
):
    
    wash_id = wash_created["id"] + 10000

    response = client.get(
        f"/washes/{wash_id}",
        headers = auth_headers
    )

    assert response.status_code == 404

def test_company_cannot_access_other_company_wash(
        client,
        wash_created
):
    email = f"empresa2_{uuid.uuid4().hex[:8]}@teste.com"
    password = "1234"

    register_response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password
        }
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    assert login_response.status_code == 200

    company_2_headers = {
        "Authorization": f"Bearer {login_response.json()['access_token']}"
    }

    response = client.get(
        f"/washes/{wash_created['id']}",
        headers=company_2_headers
    )

    assert response.status_code == 404

def test_get_wash_by_id_success(
        client,
        auth_headers,
        wash_created
):
    
    response = client.get(
        f"/washes/{wash_created["id"]}",
        headers = auth_headers
    )

    assert response.status_code == 200

def test_create_wash_success(
        client,
        auth_headers,
        customer_created
):
    
    response = client.post(
        "/washes/",
        headers = auth_headers,
        json = {   
            "customer_id": customer_created["id"],   
            "wash_type": "Simples",   
            "price": 50,   
            "notes": "" 
        }
    )

    assert response.status_code == 201

    body = response.json()

    assert body["success"] is True
