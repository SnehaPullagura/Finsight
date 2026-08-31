import os
from scripts.common import write_file

def build_comprehensive_tests():
    print("Building comprehensive test suites across all 19 modules...")

    write_file("tests/unit/test_transactions_budgets.py", """
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
""")

    write_file("tests/unit/test_goals_recurring.py", """
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
""")

    write_file("tests/unit/test_intelligence_health_scenarios.py", """
import pytest
import datetime
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_intelligence_and_health_scoring(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "email": "intel.user@finsight.app",
        "password": "Password123!",
        "full_name": "Intel Tester"
    })
    token = (await client.post("/api/v1/auth/login", json={
        "email": "intel.user@finsight.app",
        "password": "Password123!"
    })).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test NLP Categorization
    cat_req = {"description": "SWIGGY INSTAMART HYD", "amount": 850.0}
    cat_res = await client.post("/api/v1/intelligence/categorize", json=cat_req, headers=headers)
    assert cat_res.status_code == 200
    cat_data = cat_res.json()
    assert "Groceries" in cat_data["category_name"]
    assert cat_data["confidence_score"] >= 0.80

    # Test Health Score Calculation
    health_res = await client.get("/api/v1/health/score", headers=headers)
    assert health_res.status_code == 200
    health = health_res.json()
    assert 0 <= health["overall_score"] <= 100
    assert len(health["pillars"]) == 6

    # Test What-If Scenario Simulator
    scenario_res = await client.post("/api/v1/scenarios", json={
        "name": "Promotion + Apartment",
        "monthly_income_delta": 20000.0,
        "monthly_expense_delta": 8000.0,
        "loan_amount": 0.0
    }, headers=headers)
    assert scenario_res.status_code == 201
    sc = scenario_res.json()
    assert sc["is_feasible"] == True
    assert sc["health_score_delta"] > 0

    # Scenario Compare
    comp_res = await client.get("/api/v1/scenarios/compare", headers=headers)
    assert comp_res.status_code == 200
    assert "base_case" in comp_res.json()

    # AI Financial Assistant
    ai_res = await client.post("/api/v1/assistant/query", json={
        "query": "Can I afford a 40000 laptop?"
    }, headers=headers)
    assert ai_res.status_code == 200
    assert "Safe-to-Spend" in ai_res.json()["answer"]
""")

    write_file("tests/unit/test_analytics_reports_admin.py", """
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_analytics_reports_and_admin(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "email": "analytics.user@finsight.app",
        "password": "Password123!",
        "full_name": "Analytics Pro"
    })
    token = (await client.post("/api/v1/auth/login", json={
        "email": "analytics.user@finsight.app",
        "password": "Password123!"
    })).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Analytics Overview
    ana_res = await client.get("/api/v1/analytics/overview", headers=headers)
    assert ana_res.status_code == 200
    ana_data = ana_res.json()
    assert "mom" in ana_data
    assert "velocity" in ana_data
    assert "financial_stability_index" in ana_data

    # Forecasts
    fc_res = await client.get("/api/v1/forecasts/expenses?horizon_days=30", headers=headers)
    assert fc_res.status_code == 200
    assert len(fc_res.json()["daily_projections"]) == 30

    # Cashflow Summary
    cf_res = await client.get("/api/v1/cashflow/summary", headers=headers)
    assert cf_res.status_code == 200
    assert "daily_timeline" in cf_res.json()

    # Generate Report
    rep_res = await client.post("/api/v1/reports/generate", json={
        "report_type": "monthly_summary",
        "format": "csv"
    }, headers=headers)
    assert rep_res.status_code == 200
    assert "download_url" in rep_res.json()

    # Admin Metrics
    adm_res = await client.get("/api/v1/admin/metrics", headers=headers)
    assert adm_res.status_code == 200
    assert len(adm_res.json()["active_ml_models"]) >= 3
""")

    print("Test suites created successfully!")

if __name__ == "__main__":
    build_comprehensive_tests()
