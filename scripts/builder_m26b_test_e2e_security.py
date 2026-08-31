import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. tests/integration/test_auth_api.py
    write_file("tests/integration/test_auth_api.py", """import pytest
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
""")

    # 2. tests/security/test_tenant_isolation.py
    write_file("tests/security/test_tenant_isolation.py", """import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_strict_multi_tenant_isolation(client: AsyncClient, auth_headers, auth_headers_tenant_beta):
    # Tenant Alpha creates a contact
    c_resp = await client.post("/api/v1/contacts", json={
        "first_name": "Alpha",
        "last_name": "Stakeholder",
        "email": "alpha.confidential@target.internal",
        "lifecycle_stage": "customer"
    }, headers=auth_headers)
    assert c_resp.status_code == 201
    contact_id = c_resp.json()["id"]

    # Tenant Beta lists contacts -> must NOT see Tenant Alpha's contact
    beta_list = await client.get("/api/v1/contacts", headers=auth_headers_tenant_beta)
    assert beta_list.status_code == 200
    beta_contacts = beta_list.json()
    assert not any(c["id"] == contact_id for c in beta_contacts)

    # Tenant Beta attempts direct GET on Tenant Alpha's contact -> must return 404
    beta_get = await client.get(f"/api/v1/contacts/{contact_id}", headers=auth_headers_tenant_beta)
    assert beta_get.status_code == 404
""")

    # 3. tests/e2e/test_full_crm_lifecycle.py
    write_file("tests/e2e/test_full_crm_lifecycle.py", """import pytest
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
""")

    print("Test Suite generated successfully!")

if __name__ == '__main__':
    run()
