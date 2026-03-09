from tests.utils import login_user, register_user


def test_register_success(client):
    r = register_user(client, email="a@test.com", password="123456")
    assert r.status_code == 201
    data = r.json()
    assert data["email"] == "a@test.com"
    assert "id" in data


def test_register_validation_fail(client):
    r = register_user(client, email="b@test.com", password="12345")  # too short
    assert r.status_code == 422


def test_login_auth_fail(client):
    # user not exists
    r = login_user(client, email="notfound@test.com", password="123456")
    assert r.status_code in (401, 400)


def test_login_success(client):
    register_user(client, email="c@test.com", password="123456")
    r = login_user(client, email="c@test.com", password="123456")
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"