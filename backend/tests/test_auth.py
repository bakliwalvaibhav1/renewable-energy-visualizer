import pytest
import uuid

@pytest.mark.asyncio
async def test_register_user(async_client):
    """
    Test registering a new user with a unique email.
    """
    unique_email = f"user-{uuid.uuid4()}@example.com"
    payload = {
        "email": unique_email,
        "password": "securepassword123"
    }

    response = await async_client.post("/auth/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == unique_email
    assert "message" in data and "successfully" in data["message"].lower()


@pytest.mark.asyncio
async def test_login_success(async_client):
    """
    Test login with valid demo credentials.
    """
    payload = {
        "username": "demo@example.com",
        "password": "demopass"
    }

    response = await async_client.post("/auth/login", data=payload)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_failure(async_client):
    """
    Test login fails with invalid password.
    """
    payload = {
        "username": "demo@example.com",
        "password": "wrongpass"
    }

    response = await async_client.post("/auth/login", data=payload)

    assert response.status_code == 401
    data = response.json()
    assert "detail" in data
    assert "invalid credentials" in data["detail"].lower()
