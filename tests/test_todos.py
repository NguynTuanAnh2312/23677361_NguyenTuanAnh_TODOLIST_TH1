from tests.utils import auth_header, login_user, register_user


def _get_token(client, email="a@test.com"):
    register_user(client, email=email, password="123456")
    r = login_user(client, email=email, password="123456")
    return r.json()["access_token"]


def test_todo_auth_fail(client):
    r = client.post("/api/v1/todos", json={"title": "Hello", "description": None})
    assert r.status_code == 401


def test_create_todo_success(client):
    token = _get_token(client, email="todo@test.com")

    r = client.post(
        "/api/v1/todos",
        json={"title": "My Todo", "description": "test"},
        headers=auth_header(token),
    )
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "My Todo"


def test_create_todo_validation_fail(client):
    token = _get_token(client, email="val@test.com")

    # title too short (<3)
    r = client.post(
        "/api/v1/todos",
        json={"title": "Hi"},
        headers=auth_header(token),
    )
    assert r.status_code == 422


def test_get_todo_404(client):
    token = _get_token(client, email="nf@test.com")

    r = client.get("/api/v1/todos/999999", headers=auth_header(token))
    assert r.status_code == 404