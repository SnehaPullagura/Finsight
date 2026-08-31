import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_and_root(client: AsyncClient):
    res = await client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["platform"] == "FinSight"

    root_res = await client.get("/")
    assert root_res.status_code == 200
    assert "FinSight" in root_res.json()["message"]

@pytest.mark.asyncio
async def test_auth_registration_and_login(client: AsyncClient):
    # Register
    reg_payload = {
        "email": "chaitanya.tech@finsight.app",
        "password": "SecurePassword123!",
        "full_name": "Chaitanya Kumar",
        "preferred_currency": "INR"
    }
    reg_res = await client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_res.status_code == 201
    user_data = reg_res.json()
    assert user_data["email"] == "chaitanya.tech@finsight.app"
    assert user_data["full_name"] == "Chaitanya Kumar"
    assert user_data["preferred_currency"] == "INR"

    # Login
    login_payload = {
        "email": "chaitanya.tech@finsight.app",
        "password": "SecurePassword123!",
        "device_info": "MacBook Pro M3"
    }
    login_res = await client.post("/api/v1/auth/login", json=login_payload)
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    assert "refresh_token" in token_data
    access_token = token_data["access_token"]
    refresh_token = token_data["refresh_token"]

    # Access /auth/me
    headers = {"Authorization": f"Bearer {access_token}"}
    me_res = await client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "chaitanya.tech@finsight.app"

    # Refresh token
    refresh_res = await client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_res.status_code == 200
    new_tokens = refresh_res.json()
    assert "access_token" in new_tokens

@pytest.mark.asyncio
async def test_accounts_and_categories_flow(client: AsyncClient):
    # Register & Login
    reg_payload = {
        "email": "sarah.investor@finsight.app",
        "password": "StrongPassword2025!",
        "full_name": "Sarah Jenkins",
        "preferred_currency": "USD"
    }
    await client.post("/api/v1/auth/register", json=reg_payload)
    login_res = await client.post("/api/v1/auth/login", json={
        "email": "sarah.investor@finsight.app",
        "password": "StrongPassword2025!"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Categories list
    cat_res = await client.get("/api/v1/categories", headers=headers)
    assert cat_res.status_code == 200
    categories = cat_res.json()
    assert len(categories) > 10

    # Create account
    acc_payload = {
        "name": "HDFC Primary Savings",
        "account_type": "savings",
        "account_number": "987654321098",
        "institution_name": "HDFC Bank",
        "currency": "INR",
        "current_balance": 150000.0,
        "is_primary": True
    }
    acc_res = await client.post("/api/v1/accounts", json=acc_payload, headers=headers)
    assert acc_res.status_code == 201
    account = acc_res.json()
    assert account["name"] == "HDFC Primary Savings"
    assert account["account_number_masked"] == "XXXX-XXXX-1098"
    assert account["current_balance"] == 150000.0
    acc_id = account["id"]

    # Reconcile account
    rec_res = await client.post(f"/api/v1/accounts/{acc_id}/reconcile", json={"actual_balance": 152500.0}, headers=headers)
    assert rec_res.status_code == 200
    assert rec_res.json()["current_balance"] == 152500.0

    # Check balance history
    hist_res = await client.get(f"/api/v1/accounts/{acc_id}/history", headers=headers)
    assert hist_res.status_code == 200
    assert len(hist_res.json()) >= 2
