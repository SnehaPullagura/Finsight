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
