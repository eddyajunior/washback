def test_health_check(client):

    response = client.get("/health/")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "healthy"
    assert body["app"] == "WashBack"
    assert body["database"] == "connected"