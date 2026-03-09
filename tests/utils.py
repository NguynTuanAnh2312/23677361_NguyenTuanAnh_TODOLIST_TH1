def register_user(client, email="a@test.com", password="123456"):
    return client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password},
    )


def login_user(client, email="a@test.com", password="123456"):
    # OAuth2PasswordRequestForm uses form fields: username + password
    return client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )


def auth_header(token: str):
    return {"Authorization": f"Bearer {token}"}