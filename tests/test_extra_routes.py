import uuid
from unittest.mock import patch

from fastapi.testclient import TestClient

from goit_hw_12.main import app

client = TestClient(app)


def test_openapi_schema_available():
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "openapi" in response.json()

    
def test_wrong_login(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "wrong@test.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401


@patch("goit_hw_12.auth.send_verification_email")
def test_duplicate_signup(mock_send_email, client):
    unique_id = uuid.uuid4().hex

    user_data = {
        "username": "DuplicateUser",
        "email": f"duplicate_{unique_id}@test.com",
        "password": "12345678",
    }

    client.post("/auth/signup", json=user_data)

    response = client.post("/auth/signup", json=user_data)

    assert response.status_code == 409