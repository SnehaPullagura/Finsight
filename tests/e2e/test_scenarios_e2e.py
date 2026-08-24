import pytest
import datetime
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_full_scenario_simulation_e2e(client: AsyncClient):
    # 1. Register & Login
    await client.post("/api/v1/auth/register", json={
        "email": "e2e.user@finsight.app",
        "password": "Password123!",
        "full_name": "Scenario Master"
    })
    token = (await client.post("/api/v1/auth/login", json={
        "email": "e2e.user@finsight.app",
        "password": "Password123!"
    })).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Add Checking & Savings Accounts
    await client.post("/api/v1/accounts", json={
        "name": "Salary Account",
        "account_type": "savings",
        "current_balance": 150000.0,
        "is_primary": True
    }, headers=headers)

    # 3. Run Scenario 1: Car Loan Simulation
    sc1 = await client.post("/api/v1/scenarios", json={
        "name": "EV Car Purchase",
        "monthly_income_delta": 0.0,
        "monthly_expense_delta": -2000.0, # fuel savings
        "one_time_lump_sum": 200000.0,
        "loan_amount": 600000.0,
        "loan_tenure_months": 36,
        "loan_interest_rate": 8.5
    }, headers=headers)
    assert sc1.status_code == 201
    d1 = sc1.json()
    assert d1["calculated_monthly_emi"] > 0
    assert d1["is_feasible"] == True

    # 4. Run Scenario 2: High Risk Infeasible Purchase
    sc2 = await client.post("/api/v1/scenarios", json={
        "name": "Luxury Yacht Purchase",
        "monthly_income_delta": 0.0,
        "monthly_expense_delta": 50000.0,
        "one_time_lump_sum": 500000.0,
        "loan_amount": 2000000.0,
        "loan_tenure_months": 24,
        "loan_interest_rate": 14.0
    }, headers=headers)
    assert sc2.status_code == 201
    d2 = sc2.json()
    assert d2["is_feasible"] == False
    assert d2["health_score_delta"] < 0

    # 5. Side-by-side comparison
    cmp_res = await client.get("/api/v1/scenarios/compare", headers=headers)
    assert cmp_res.status_code == 200
    assert len(cmp_res.json()["scenarios"]) == 2
