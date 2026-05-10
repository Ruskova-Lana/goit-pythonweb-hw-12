from fastapi.testclient import TestClient
from goit_hw_12.main import app

client = TestClient(app)


def test_get_contacts_unauthorized():
    response = client.get("/contacts/")

    assert response.status_code == 401