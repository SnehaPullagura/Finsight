import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock
from backend.app.main import app
from backend.app.core.database import get_db

@pytest.fixture
def mock_db_session():
    session = AsyncMock()
    session.execute = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.close = AsyncMock()
    return session

@pytest_asyncio.fixture
async def async_client(mock_db_session):
    async def override_get_db():
        yield mock_db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as client:
        yield client
    app.dependency_overrides.clear()
