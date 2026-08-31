import sys
import os
sys.path.insert(0, os.path.abspath("."))
import pytest
import asyncio
import os
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# Set test environment
os.environ["APP_ENV"] = "test"
os.environ["APP_SECRET_KEY"] = "test_secret_key_64_characters_long_for_security_testing_purposes"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from backend.app.main import app
from backend.app.models.base import Base
from backend.app.core.database import get_db
from backend.app.core.security import create_access_token

# Import all models to ensure metadata registration
import backend.app.models.auth
import backend.app.models.organization
import backend.app.models.contact
import backend.app.models.company
import backend.app.models.lead
import backend.app.models.pipeline
import backend.app.models.deal
import backend.app.models.activity
import backend.app.models.task
import backend.app.models.calendar
import backend.app.models.communication
import backend.app.models.document
import backend.app.models.product
import backend.app.models.proposal
import backend.app.models.quote
import backend.app.models.invoice
import backend.app.models.support
import backend.app.models.customer_success
import backend.app.models.campaign
import backend.app.models.automation
import backend.app.models.custom_field
import backend.app.models.audit

test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
    echo=False
)

TestAsyncSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestAsyncSessionLocal() as session:
        yield session
        await session.rollback()

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers():
    token = create_access_token(
        subject="user-test-123",
        tenant_id="tenant-alpha",
        roles=["Admin"]
    )
    return {
        "Authorization": f"Bearer {token}",
        "X-Tenant-ID": "tenant-alpha"
    }

@pytest.fixture
def auth_headers_tenant_beta():
    token = create_access_token(
        subject="user-test-456",
        tenant_id="tenant-beta",
        roles=["Admin"]
    )
    return {
        "Authorization": f"Bearer {token}",
        "X-Tenant-ID": "tenant-beta"
    }
