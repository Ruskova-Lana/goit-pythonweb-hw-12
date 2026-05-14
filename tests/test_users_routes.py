from fastapi.testclient import TestClient
from goit_hw_12.main import app

client = TestClient(app)


def test_docs():
    response = client.get("/docs")

    assert response.status_code == 200


def test_openapi():
    response = client.get("/openapi.json")

    assert response.status_code == 200


def test_me_without_token():
    response = client.get("/users/me")

    assert response.status_code == 401


