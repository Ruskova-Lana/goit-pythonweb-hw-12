import pytest
from fastapi.testclient import TestClient

from goit_hw_12.main import app


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def token(client):
    login_response = client.post(
        "/auth/login",
        data={
            "username": "ruslana@test.com",
            "password": "12345678"
        }
    )

    return login_response.json()["access_token"]