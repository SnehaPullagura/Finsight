import pytest
import datetime
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_transaction_crud_and_splitting(client: AsyncClient):
    # Register & login
    await client.post("/api/v1/auth/register", json={
        "email": "tx.tester@finsight.app",
        "password": "Password123!",
        "full_name": "Tx Tester"
    })
    login_res = await client.post("/api/v1/auth/login", json={
        "email": "tx.tester@finsight.app",
        "password": "Password123!"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create account
    acc_res = await client.post("/api/v1/accounts", json={
        "name": "Checking Account",
        "account_type": "bank",
        "current_balance": 50000.0
    }, headers=headers)
    acc_id = acc_res.json()["id"]

    # Categories
    cats = (await client.get("/api/v1/categories", headers=headers)).json()
    groceries_cat = next(c for c in cats if "Groceries" in c["name"])
    dining_cat = next(c for c in cats if "Dining" in c["name"])

    # Create Transaction with splits
    tx_payload = {
        "account_id": acc_id,
        "amount": 3000.0,
        "transaction_type": "expense",
        "transaction_date": str(datetime.date.today()),
        "description": "Supermarket and Cafe combo",
        "merchant_name": "SuperStore",
        "splits": [
            {"category_id": groceries_cat["id"], "amount": 2000.0, "notes": "Groceries part"},
            {"category_id": dining_cat["id"], "amount": 1000.0, "notes": "Coffee & snacks"}
        ]
    }
    tx_res = await client.post("/api/v1/transactions", json=tx_payload, headers=headers)
    assert tx_res.status_code == 201
    tx = tx_res.json()
    assert tx["amount"] == 3000.0
    assert len(tx["splits"]) == 2

    # Verify updated account balance
    acc_updated = (await client.get(f"/api/v1/accounts/{acc_id}", headers=headers)).json()
    assert acc_updated["current_balance"] == 47000.0

    # Search / list transactions
    list_res = await client.get(f"/api/v1/transactions?account_id={acc_id}", headers=headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1
