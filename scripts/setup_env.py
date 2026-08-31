with open(".env", "w", encoding="utf-8") as f:
    f.write("""APP_ENV=development
APP_SECRET_KEY=clientflow_production_super_secure_secret_key_64_characters_long_for_jwt
DATABASE_URL=sqlite+aiosqlite:///./clientflow.db
DATABASE_SYNC_URL=sqlite:///./clientflow.db
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000", "http://localhost:80", "http://127.0.0.1:5173", "http://127.0.0.1:8000"]
""")
print("Created .env with clientflow.db SQLite configuration.")
