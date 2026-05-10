from fastapi.testclient import TestClient
from goit_hw_12.main import app

client = TestClient(app)


def test_signup():
    response = client.post(
        "/auth/signup",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "12345678"
        }
    )

    assert response.status_code in [201, 409]


def test_login_wrong_password():
    response = client.post(
        "/auth/login",
        data={
            "username": "testuser@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401