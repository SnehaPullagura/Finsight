import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_full_end_to_end_crm_lifecycle(client: AsyncClient, auth_headers):
    # 1. Create Organization
    org_resp = await client.post("/api/v1/organizations", json={
        "name": "Acme Global Dynamics",
        "plan_tier": "enterprise"
    }, headers=auth_headers)
    assert org_resp.status_code in [200, 201]

    # 2. Create Company
    comp_resp = await client.post("/api/v1/companies", json={
        "name": "Stark Industries",
        "domain": "starkindustries.internal",
        "industry": "technology",
        "annual_revenue": 5000000.0,
        "employee_count": 250
    }, headers=auth_headers)
    assert comp_resp.status_code == 201
    comp_id = comp_resp.json()["id"]

    # 3. Create Contact
    contact_resp = await client.post("/api/v1/contacts", json={
        "first_name": "Pepper",
        "last_name": "Potts",
        "email": "pepper.potts@starkindustries.internal",
        "company_id": comp_id,
        "title": "Chief Executive Officer"
    }, headers=auth_headers)
    assert contact_resp.status_code == 201
    contact_id = contact_resp.json()["id"]

    # 4. Create Lead
    lead_resp = await client.post("/api/v1/leads", json={
        "first_name": "Tony",
        "last_name": "Stark",
        "email": "tony.stark@starkindustries.internal",
        "company_name": "Stark Industries",
        "estimated_budget": 250000.0,
        "employee_count": 500,
        "industry": "technology",
        "intent_score": 95
    }, headers=auth_headers)
    assert lead_resp.status_code == 201
    lead_id = lead_resp.json()["id"]

    # 5. Qualify Lead
    qualify_resp = await client.post(f"/api/v1/leads/{lead_id}/qualify", headers=auth_headers)
    assert qualify_resp.status_code == 200
    assert qualify_resp.json()["status"] == "qualified"

    # 6. Convert Lead
    conv_resp = await client.post(f"/api/v1/leads/{lead_id}/convert", json={
        "create_deal": True,
        "deal_name": "Enterprise Arc Reactor Deal",
        "deal_value": 250000.0
    }, headers=auth_headers)
    assert conv_resp.status_code == 200
    deal_id = conv_resp.json()["deal_id"]

    # 7. Create Proposal
    prop_resp = await client.post("/api/v1/proposals", json={
        "title": "Enterprise Arc Reactor Expansion SOW",
        "deal_id": deal_id,
        "company_id": comp_id,
        "contact_id": contact_id,
        "line_items": [
            {
                "item_name": "Arc Reactor Core Architecture",
                "quantity": 1,
                "unit_price": 200000.0,
                "discount_pct": 0.0,
                "tax_rate_pct": 5.0
            }
        ]
    }, headers=auth_headers)
    assert prop_resp.status_code == 201
    prop_id = prop_resp.json()["id"]

    # 8. Accept Proposal
    accept_resp = await client.post(f"/api/v1/proposals/{prop_id}/accept", headers=auth_headers)
    assert accept_resp.status_code == 200
    assert accept_resp.json()["status"] == "accepted"

    # 9. Onboard Customer & Recalculate Health
    plan_resp = await client.post("/api/v1/customer-success/plans", json={
        "company_id": comp_id,
        "status": "onboarding"
    }, headers=auth_headers)
    assert plan_resp.status_code == 201
    plan_id = plan_resp.json()["id"]

    health_resp = await client.post(f"/api/v1/customer-success/plans/{plan_id}/recalculate-health", headers=auth_headers)
    assert health_resp.status_code == 200
    assert health_resp.json()["health_score"] >= 70
