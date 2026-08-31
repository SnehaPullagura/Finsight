import pytest
import datetime
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_goals_and_recurring_flow(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "email": "goal.user@finsight.app",
        "password": "Password123!",
        "full_name": "Goal Achiever"
    })
    token = (await client.post("/api/v1/auth/login", json={
        "email": "goal.user@finsight.app",
        "password": "Password123!"
    })).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create Goal
    goal_res = await client.post("/api/v1/goals", json={
        "name": "New Laptop Fund",
        "goal_type": "custom",
        "target_amount": 100000.0,
        "current_amount": 25000.0,
        "target_date": str(datetime.date.today() + datetime.timedelta(days=120)),
        "monthly_contribution": 20000.0
    }, headers=headers)
    assert goal_res.status_code == 201
    goal = goal_res.json()
    assert goal["target_amount"] == 100000.0
    assert goal["percentage_completed"] == 25.0
    goal_id = goal["id"]

    # Contribute to goal
    contrib_res = await client.post(f"/api/v1/goals/{goal_id}/contribute", json={
        "amount": 15000.0,
        "notes": "Bonus allocation"
    }, headers=headers)
    assert contrib_res.status_code == 200
    assert contrib_res.json()["current_amount"] == 40000.0

    # Create Recurring Payment
    acc_res = await client.post("/api/v1/accounts", json={
        "name": "Salary Account",
        "account_type": "savings",
        "current_balance": 80000.0
    }, headers=headers)
    acc_id = acc_res.json()["id"]

    rec_res = await client.post("/api/v1/recurring", json={
        "account_id": acc_id,
        "merchant_name": "Netflix Streaming",
        "amount": 649.0,
        "cadence": "monthly",
        "next_expected_date": str(datetime.date.today() + datetime.timedelta(days=15))
    }, headers=headers)
    assert rec_res.status_code == 201
    assert rec_res.json()["merchant_name"] == "Netflix Streaming"

    # Calendar
    cal_res = await client.get("/api/v1/recurring/calendar", headers=headers)
    assert cal_res.status_code == 200
    assert len(cal_res.json()) >= 1
