import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    payload = {
        "name": "Sarah Connor",
        "email": "sarah@example.com",
        "password": "StrongPassword!2026",
        "age": 30,
        "gender": "female",
        "height_cm": 165.0,
        "weight_kg": 60.0,
        "activity_level": "active",
        "goal": "lose"
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "sarah@example.com"
    assert data["user"]["name"] == "Sarah Connor"
    assert data["user"]["daily_calorie_target"] > 0

@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    payload = {
        "name": "Sarah Connor",
        "email": "sarah_dup@example.com",
        "password": "StrongPassword!2026",
    }
    res1 = await client.post("/api/v1/auth/register", json=payload)
    assert res1.status_code == 201

    res2 = await client.post("/api/v1/auth/register", json=payload)
    assert res2.status_code == 400
    assert "already exists" in res2.json()["detail"].lower()

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    # Register first
    await client.post("/api/v1/auth/register", json={
        "name": "Login User",
        "email": "loginuser@example.com",
        "password": "CorrectPassword123"
    })

    # Now login
    response = await client.post("/api/v1/auth/login", json={
        "email": "loginuser@example.com",
        "password": "CorrectPassword123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "loginuser@example.com"

@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient):
    response = await client.post("/api/v1/auth/login", json={
        "email": "loginuser@example.com",
        "password": "WrongPasswordXYZ"
    })
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_current_user_me(client: AsyncClient, auth_headers: dict):
    response = await client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "alex.test@example.com"

@pytest.mark.asyncio
async def test_get_me_unauthorized(client: AsyncClient):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401
