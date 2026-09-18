from app.main import app


def test_health():
    client = app.test_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_add():
    client = app.test_client()
    resp = client.get("/add?a=2&b=3")
    assert resp.status_code == 200
    assert resp.get_json() == {"result": 5.0}


def test_add_invalid_input():
    client = app.test_client()
    resp = client.get("/add?a=foo&b=3")
    assert resp.status_code == 400
