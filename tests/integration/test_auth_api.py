import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_auth_registration_and_login(client: AsyncClient):
    # Register
    reg_resp = await client.post("/api/v1/auth/register", json={
        "email": "sarah.connor@cyberdyne.internal",
        "password": "StrongPassword123!",
        "first_name": "Sarah",
        "last_name": "Connor",
        "organization_name": "Cyberdyne Systems"
      })
    assert reg_resp.status_code == 201
    reg_data = reg_resp.json()
    assert reg_data["email"] == "sarah.connor@cyberdyne.internal"
    assert reg_data["first_name"] == "Sarah"

    # Login
    login_resp = await client.post("/api/v1/auth/login", json={
        "email": "sarah.connor@cyberdyne.internal",
        "password": "StrongPassword123!"
    })
    assert login_resp.status_code == 200
    token_data = login_resp.json()
    assert "access_token" in token_data
    assert "refresh_token" in token_data

    # Refresh
    ref_resp = await client.post("/api/v1/auth/refresh", json={
        "refresh_token": token_data["refresh_token"]
    })
    assert ref_resp.status_code == 200
    assert "access_token" in ref_resp.json()
