import json
from unittest.mock import MagicMock, patch

import pytest
from jose import jwt

from fastapi import HTTPException
from fastapi.testclient import TestClient


from goit_hw_12.auth import (
    get_current_user,
    create_access_token,
    create_email_token,
    create_password_reset_token, 
    verify_password, 
    get_password_hash,
    admin_required
)
from goit_hw_12.main import app
from goit_hw_12.config import settings

client = TestClient(app)


@pytest.mark.asyncio
async def test_get_current_user_from_cache_without_db_call():
    token = jwt.encode(
        {"sub": "cached@test.com"},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    cached_user = {
        "id": 1,
        "username": "Cached User",
        "email": "cached@test.com",
        "avatar": None,
        "confirmed": True,
        "role": "user",
    }

    db = MagicMock()

    with patch(
        "goit_hw_12.auth.redis_client.get",
        return_value=json.dumps(cached_user),
    ):
        user = await get_current_user(token=token, db=db)

    assert user.email == "cached@test.com"
    assert user.role == "user"
    db.query.assert_not_called()


def test_create_email_token():
    token = create_email_token("test@test.com")

    assert token is not None
    assert isinstance(token, str)


def test_create_password_reset_token():
    token = create_password_reset_token("test@test.com")

    assert token is not None
    assert isinstance(token, str)


def test_verify_password_false():
    hashed_password = get_password_hash("correctpassword")

    result = verify_password("wrongpassword", hashed_password)

    assert result is False


def test_docs_route():
    response = client.get("/docs")

    assert response.status_code == 200


def test_openapi_route():
    response = client.get("/openapi.json")

    assert response.status_code == 200


def test_signup_existing_user():
    response = client.post(
        "/auth/signup",
        json={
            "username": "Ruslana",
            "email": "ruslana@test.com",
            "password": "12345678",
        },
    )

    assert response.status_code in [201, 409]


def test_login_invalid_user():
    response = client.post(
        "/auth/login",
        data={
            "username": "notexists@test.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401


def test_access_token_contains_string():
    token = create_access_token({"sub": "test@test.com"})

    assert "eyJ" in token


def test_admin_required_success():
    user = MagicMock()
    user.role = "admin"

    result = admin_required(current_user=user)

    assert result == user


def test_admin_required_forbidden():
    user = MagicMock()
    user.role = "user"

    with pytest.raises(HTTPException) as exc_info:
        admin_required(current_user=user)

    assert exc_info.value.status_code == 403