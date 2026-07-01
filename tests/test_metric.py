def test_metrics(client):

    response = client.get("/metrics/")

    assert response.status_code == 200

    body = response.json()

    assert "requests_total" in body
    assert "errors_total" in body
    assert "average_duration_ms" in body


def test_metrics_increment_requests(client):

    before = client.get("/metrics/").json()["requests_total"]

    client.get("/health/")

    after = client.get("/metrics/").json()["requests_total"]

    assert after > before