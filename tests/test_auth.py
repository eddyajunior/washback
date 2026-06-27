import uuid

def test_register_validation_error(client):

    response = client.post(
        "auth/register",
        json={}
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 422

    body = response.json()

    assert body["success"] is False

def test_register_duplicate_email(client, unique_email):

    password = "123456"

    response = client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "password": password
            # ,"company_name": "Empresa Teste"
        }
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True

def test_register_success(client):

    email = f"teste_{uuid.uuid4().hex[:8]}@empresa.com"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "1234"
        }
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code in [200, 201]

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Usuário criado com sucesso"
    assert body["data"] is None

def test_register_success_and_login(client):

    email = f"teste_{uuid.uuid4().hex[:8]}@empresa.com"
    senha = "1234"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": senha
        }
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code in [200, 201]

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Usuário criado com sucesso"
    assert body["data"] is None

    print(email)

    response_login = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": senha
        }
    )

    print(response_login.json())

def test_login_invalid_password(client, unique_email):

    password = "123456"

    response = client.post(
        "/auth/login",
        json = {
            "email": unique_email,
            "password": password
        }        
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 422

    body = response.json()

    assert body["success"] is False


def test_login_user_not_found(client):

    response = client.post(
        "/auth/login",
        json = {
            "email": "naoexiste@email.com",
            "password": "123456"
        }        
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 401

    body = response.json()
    assert body["success"] is False


def test_login_invalid_credentials(client):

    response = client.post(
        "/auth/login",
        json = {
            "email": "usuario@inexistente.com",
            "password": "senha_errada"
        }
    )

    print(response.status_code)
    print(response.json())

    assert response.status_code == 401

    body = response.json()
    assert body["success"] is False

def test_login_validation_error(client):

    response = client.post(
        "/auth/login",
        json={}
    )

    assert response.status_code == 422

    body = response.json()

    assert body["success"] == False
    assert body["message"] == "Dados de entrada inválidos"

def test_login_invalid_credentials(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "edson@empresa1.com",
            "password": "12345"
        }
    )

    assert response.status_code == 422

def test_login_user_not_found(client):

    response = client.post(
        "/auth/login",
        json={
            "email": "nonexistent@empresa1.com",
            "password": "1234"
        }
    )

    assert response.status_code == 422

def test_login_success(client, unique_email):

    password = "123456"

    client.post(
        "/auth/register",
        json={
            "email": unique_email,
            "password": password
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": unique_email,
            "password": password
        }
    )

    assert response.status_code == 200
    
    body = response.json()

    assert "access_token" in body
    assert body["token_type"] == "bearer"