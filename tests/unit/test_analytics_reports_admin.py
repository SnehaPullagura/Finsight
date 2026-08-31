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
