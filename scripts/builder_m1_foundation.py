import os

def write_file(rel_path, content):
    full_path = os.path.join(os.getcwd(), rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {rel_path}")

write_file("LICENSE", """MIT License

Copyright (c) 2026 ClientFlow CRM Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""")

write_file(".env.example", """# Application Configuration
APP_NAME=ClientFlow CRM
APP_ENV=development
APP_DEBUG=true
APP_SECRET_KEY=super_secure_clientflow_enterprise_secret_key_2026_change_in_prod
APP_URL=http://localhost:3000
API_V1_PREFIX=/api/v1

# Security & CORS
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:8000","http://127.0.0.1:3000"]
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30
ALGORITHM=HS256

# Database (PostgreSQL)
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=clientflow_db
POSTGRES_USER=clientflow_user
POSTGRES_PASSWORD=clientflow_secret_password
DATABASE_URL=postgresql+asyncpg://clientflow_user:clientflow_secret_password@localhost:5432/clientflow_db
DATABASE_SYNC_URL=postgresql+psycopg2://clientflow_user:clientflow_secret_password@localhost:5432/clientflow_db

# Redis & Celery
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# OpenSearch / Elasticsearch
OPENSEARCH_HOST=localhost
OPENSEARCH_PORT=9200
OPENSEARCH_USER=admin
OPENSEARCH_PASSWORD=admin
OPENSEARCH_USE_SSL=false

# Storage Provider (local | s3 | minio)
STORAGE_PROVIDER=local
STORAGE_LOCAL_ROOT=./media_uploads

# Email & SMS Providers (mock | smtp | sendgrid | twilio)
EMAIL_PROVIDER=mock
EMAILS_FROM_EMAIL=no-reply@clientflow.internal
EMAILS_FROM_NAME=ClientFlow CRM
SMS_PROVIDER=mock

# AI Assistant Provider (mock | gemini | openai)
AI_PROVIDER=mock
AI_MODEL_NAME=gemini-1.5-pro
GEMINI_API_KEY=
OPENAI_API_KEY=

# Rate Limiting
RATE_LIMIT_PER_MINUTE=120""")

write_file("README.md", """# ClientFlow CRM 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18.3+-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-336791.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ed.svg)](https://www.docker.com/)

**ClientFlow CRM** is an enterprise-grade, multi-tenant Customer Relationship Management (CRM) platform designed for high-velocity sales teams, customer success organizations, and omnichannel support operations.

---

## 🏗️ Architecture

ClientFlow CRM follows a strict layered architecture:
`API` ➔ `Router` ➔ `Schema` ➔ `Service` ➔ `Repository` ➔ `Database`.

```
clientflowCRM/
├── backend/          # FastAPI async backend with SQLAlchemy 2.0 & Pydantic v2
├── frontend/         # React 18 + TypeScript + Vite + Tailwind CSS SPA
├── workers/          # Celery background workers and scheduled task runners
├── infrastructure/   # Nginx, PostgreSQL, OpenSearch & Prometheus configs
├── scripts/          # Seed data, migrations, tests, and LOC measurement
├── docs/             # Complete architectural and operational specifications
└── tests/            # Pytest test suite (Unit, Integration, Security, E2E)
```

---

## 🚀 Quick Start

```bash
# 1. Clone repository and setup environment
cp .env.example .env

# 2. Launch full stack with Docker Compose
docker compose up -d --build

# 3. Access applications:
# Frontend App:       http://localhost:3000
# Backend API Docs:   http://localhost:8000/docs
```
""")

write_file("docker-compose.yml", """version: "3.8"

services:
  postgres:
    image: postgres:16-alpine
    container_name: clientflow_postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-clientflow_user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-clientflow_secret_password}
      POSTGRES_DB: ${POSTGRES_DB:-clientflow_db}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./infrastructure/docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-clientflow_user} -d ${POSTGRES_DB:-clientflow_db}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: clientflow_redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    container_name: clientflow_backend
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    env_file:
      - .env
    environment:
      - DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER:-clientflow_user}:${POSTGRES_PASSWORD:-clientflow_secret_password}@postgres:5432/${POSTGRES_DB:-clientflow_db}
      - DATABASE_SYNC_URL=postgresql+psycopg2://${POSTGRES_USER:-clientflow_user}:${POSTGRES_PASSWORD:-clientflow_secret_password}@postgres:5432/${POSTGRES_DB:-clientflow_db}
      - REDIS_URL=redis://redis:6379/0
      - CELERY_BROKER_URL=redis://redis:6379/1
      - CELERY_RESULT_BACKEND=redis://redis:6379/2
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app/backend
      - ./media_uploads:/app/media_uploads

  worker:
    build:
      context: .
      dockerfile: workers/Dockerfile
    container_name: clientflow_worker
    restart: unless-stopped
    depends_on:
      backend:
        condition: service_started
      redis:
        condition: service_healthy
    env_file:
      - .env
    environment:
      - DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER:-clientflow_user}:${POSTGRES_PASSWORD:-clientflow_secret_password}@postgres:5432/${POSTGRES_DB:-clientflow_db}
      - CELERY_BROKER_URL=redis://redis:6379/1
      - CELERY_RESULT_BACKEND=redis://redis:6379/2
    volumes:
      - ./backend:/app/backend
      - ./workers:/app/workers
      - ./media_uploads:/app/media_uploads

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: clientflow_frontend
    restart: unless-stopped
    ports:
      - "3000:80"
    depends_on:
      - backend

  reverse-proxy:
    image: nginx:alpine
    container_name: clientflow_gateway
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - ./infrastructure/nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - frontend
      - backend

volumes:
  postgres_data:
  redis_data:
""")

write_file("backend/requirements.txt", """fastapi>=0.111.0,<1.0.0
uvicorn[standard]>=0.30.0,<1.0.0
pydantic>=2.7.0,<3.0.0
pydantic-settings>=2.2.0,<3.0.0
sqlalchemy>=2.0.30,<3.0.0
asyncpg>=0.29.0,<1.0.0
psycopg2-binary>=2.9.9,<3.0.0
alembic>=1.13.1,<2.0.0
redis>=5.0.4,<6.0.0
celery>=5.4.0,<6.0.0
passlib[bcrypt,argon2]>=1.7.4
bcrypt>=4.1.3,<5.0.0
argon2-cffi>=23.1.0
pyjwt>=2.8.0,<3.0.0
python-multipart>=0.0.9
jinja2>=3.1.4,<4.0.0
reportlab>=4.2.0,<5.0.0
httpx>=0.27.0,<1.0.0
pytest>=8.2.0,<9.0.0
pytest-asyncio>=0.23.6,<1.0.0
pytest-cov>=5.0.0,<6.0.0
pyotp>=2.9.0,<3.0.0
qrcode>=7.4.2,<8.0.0
python-dotenv>=1.0.1
email-validator>=2.1.1
""")

write_file("backend/pyproject.toml", """[tool.pytest.ini_options]
minversion = "8.0"
addopts = "-ra -q --asyncio-mode=auto"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
filterwarnings = [
    "ignore::DeprecationWarning",
    "ignore::UserWarning",
]

[tool.ruff]
line-length = 100
target-version = "py311"
""")

write_file("backend/Dockerfile", """FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential \\
    libpq-dev \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend /app/backend

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""")

write_file("workers/Dockerfile", """FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential \\
    libpq-dev \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend /app/backend
COPY workers /app/workers

CMD ["celery", "-A", "workers.celery_app.celery_app", "worker", "--loglevel=info", "--concurrency=4"]
""")

write_file("infrastructure/nginx/default.conf", """server {
    listen 80;
    server_name localhost;

    client_max_body_size 50M;

    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /docs {
        proxy_pass http://backend:8000/docs;
        proxy_set_header Host $host;
    }

    location /openapi.json {
        proxy_pass http://backend:8000/openapi.json;
        proxy_set_header Host $host;
    }

    location / {
        proxy_pass http://frontend:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
""")

write_file("infrastructure/docker/postgres/init.sql", """-- Enable pgvector and full text extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "unaccent";
""")

write_file("frontend/package.json", """{
  "name": "clientflow-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@tanstack/react-query": "^5.37.1",
    "axios": "^1.7.2",
    "clsx": "^2.1.1",
    "date-fns": "^3.6.0",
    "lucide-react": "^0.379.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-hook-form": "^7.51.4",
    "react-router-dom": "^6.23.1",
    "recharts": "^2.12.7",
    "tailwind-merge": "^2.3.0",
    "zustand": "^4.5.2"
  },
  "devDependencies": {
    "@types/node": "^20.12.12",
    "@types/react": "^18.3.2",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.3",
    "typescript": "^5.4.5",
    "vite": "^5.2.11"
  }
}
""")

write_file("frontend/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
""")

write_file("frontend/tsconfig.node.json", """{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
""")

write_file("frontend/vite.config.ts", """import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 3000,
    host: true,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
""")

write_file("frontend/tailwind.config.js", """/** @type {import("tailwindcss").Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#f0fdf4",
          100: "#dcfce7",
          500: "#22c55e",
          600: "#16a34a",
          700: "#15803d",
          800: "#166534",
          900: "#14532d",
        },
      },
    },
  },
  plugins: [],
}
""")

write_file("frontend/postcss.config.js", """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
""")

write_file("frontend/index.html", """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ClientFlow CRM</title>
  </head>
  <body class="bg-gray-50 text-gray-900 antialiased">
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
""")

write_file("frontend/Dockerfile", """FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
""")

write_file("backend/alembic.ini", """[alembic]
script_location = backend/alembic
prepend_sys_path = .
version_path_separator = os

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
""")

write_file("backend/alembic/script.py.mako", """\"\"\"${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

\"\"\"
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}

def upgrade() -> None:
    ${upgrades if upgrades else "pass"}

def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
""")

write_file("backend/alembic/env.py", """import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.app.core.config import settings
from backend.app.models.base import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = settings.DATABASE_SYNC_URL or str(settings.DATABASE_URL).replace("+asyncpg", "")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = str(settings.DATABASE_URL)
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
""")

print("Milestone 1 executed successfully!")
