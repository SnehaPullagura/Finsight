# ClientFlow CRM — Configuration Reference

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `APP_ENV` | `production` | Environment (`development`, `test`, `production`) |
| `APP_SECRET_KEY` | *(Required)* | 64+ char secret key for HMAC cryptography |
| `DATABASE_URL` | `postgresql+asyncpg://...` | Async PostgreSQL connection string |
| `DATABASE_SYNC_URL` | `postgresql://...` | Sync PostgreSQL connection string |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis caching instance |
| `CELERY_BROKER_URL` | `redis://localhost:6379/1` | Celery message broker |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Access token lifespan in minutes |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS` | `30` | Refresh token lifespan in days |
| `AI_PROVIDER` | `mock` | AI assistant provider (`mock`, `gemini`, `openai`) |
