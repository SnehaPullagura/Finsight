import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    response = await async_client.get('/api/v1/health')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'healthy'
    assert 'version' in data
    assert 'environment' in data

@pytest.mark.asyncio
async def test_root_endpoint(async_client: AsyncClient):
    response = await async_client.get('/')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'online'
    assert data['docs'] == '/docs'

@pytest.mark.asyncio
async def test_readiness_check(async_client: AsyncClient):
    response = await async_client.get('/api/v1/health/ready')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'ready'
    assert data['database'] == 'ok'
