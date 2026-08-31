import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath("."))
from backend.app.core.database import AsyncSessionLocal
from backend.app.services.auth import AuthService
from backend.app.schemas.auth import UserLoginRequest

async def test_auth():
    async with AsyncSessionLocal() as db:
        service = AuthService(db)
        login_schema = UserLoginRequest(email="admin@clientflow.internal", password="AdminSecret123!")
        result, user = await service.authenticate(login_schema)
        print("Login SUCCESS!")
        print("Access Token:", result.access_token[:30] + "...")
        print("User:", result.email, result.first_name, result.last_name, "Tenant:", result.tenant_id, "Roles:", result.roles)

if __name__ == '__main__':
    asyncio.run(test_auth())
