import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath("."))
from backend.app.core.database import AsyncSessionLocal
from backend.app.services.auth import AuthService
from backend.app.schemas.auth import UserLoginRequest

async def test_multi_login():
    for i in range(1, 4):
        async with AsyncSessionLocal() as db:
            service = AuthService(db)
            login_schema = UserLoginRequest(email="admin@clientflow.internal", password="AdminSecret123!")
            result, user = await service.authenticate(login_schema)
            print(f"Login #{i} SUCCESS! Token: {result.access_token[:20]}...")
            
            # Logout session
            await service.logout(user.id, result.refresh_token)
            print(f"Logout #{i} SUCCESS!")

if __name__ == '__main__':
    asyncio.run(test_multi_login())
