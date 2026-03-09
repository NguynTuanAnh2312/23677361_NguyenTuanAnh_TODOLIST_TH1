from tests.utils import auth_header, login_user, register_user

def _get_token(client, email="a@test.com"):
    register_user(client, email=email, password="123456")
    r = login_user(client, email=email, password="123456")
    return r.json()["access_token"]

def test_soft_delete_todo(client):
    token = _get_token(client, email="del@test.com")

    # create
    r = client.post(
        "/api/v1/todos",
        json={"title": "Delete me", "description": None},
        headers=auth_header(token),
    )
    assert r.status_code == 201
    todo_id = r.json()["id"]

    # delete (soft)
    r = client.delete(f"/api/v1/todos/{todo_id}", headers=auth_header(token))
    assert r.status_code == 204

    # must be 404 after delete
    r = client.get(f"/api/v1/todos/{todo_id}", headers=auth_header(token))
    assert r.status_code == 404