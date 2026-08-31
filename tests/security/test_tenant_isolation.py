import pytest
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
