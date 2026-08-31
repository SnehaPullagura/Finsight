import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. Update backend/app/core/config.py
    with open("backend/app/core/config.py", "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace(
        """    ALLOWED_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:3000"]""",
        """    ALLOWED_ORIGINS: Union[List[str], str] = ["*", "http://localhost:5173", "http://localhost:3000", "http://localhost:80", "http://localhost:8000", "http://127.0.0.1:5173", "http://127.0.0.1:8000"]"""
    )
    content = content.replace(
        """    DATABASE_URL: str = "postgresql+asyncpg://clientflow_user:clientflow_secret_password@localhost:5432/clientflow_db\"""",
        """    DATABASE_URL: str = "sqlite+aiosqlite:///./clientflow.db\""""
    )
    content = content.replace(
        """    DATABASE_SYNC_URL: str = "postgresql+psycopg2://clientflow_user:clientflow_secret_password@localhost:5432/clientflow_db\"""",
        """    DATABASE_SYNC_URL: str = "sqlite:///./clientflow.db\""""
    )

    with open("backend/app/core/config.py", "w", encoding="utf-8") as f:
        f.write(content)

    print("Updated config.py with SQLite default and CORS origins.")

if __name__ == '__main__':
    run()
