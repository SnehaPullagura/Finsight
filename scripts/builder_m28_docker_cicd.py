import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. docker/Dockerfile.backend
    write_file("docker/Dockerfile.backend", """# Multi-stage production Dockerfile for ClientFlow CRM Backend
FROM python:3.13-slim AS builder

WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.13-slim AS runner

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 curl && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

COPY backend /app/backend
COPY pyproject.toml /app/pyproject.toml

# Non-root security user
RUN useradd -m -u 1001 clientflow && chown -R clientflow:clientflow /app
USER clientflow

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
""")

    # 2. docker/Dockerfile.frontend
    write_file("docker/Dockerfile.frontend", """# Multi-stage Dockerfile for ClientFlow CRM Frontend SPA
FROM node:20-alpine AS build

WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

FROM nginx:1.27-alpine AS runner

COPY --from=build /app/dist /usr/share/nginx/html
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
""")

    # 3. docker/Dockerfile.worker
    write_file("docker/Dockerfile.worker", """# Celery Background Worker Service
FROM python:3.13-slim

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 curl && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend /app/backend
COPY workers /app/workers
COPY pyproject.toml /app/pyproject.toml

ENV PYTHONPATH=/app

RUN useradd -m -u 1001 clientflow && chown -R clientflow:clientflow /app
USER clientflow

CMD ["celery", "-A", "workers.celery_app.celery_app", "worker", "--loglevel=info", "-c", "4"]
""")

    # 4. docker/nginx.conf
    write_file("docker/nginx.conf", """server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private auth;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/json application/javascript;

    # Security Headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # SPA Router fallback
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Reverse proxy API to backend container
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
""")

    # 5. docker-compose.yml
    write_file("docker-compose.yml", """version: "3.9"

services:
  postgres:
    image: postgres:16-alpine
    container_name: clientflow_postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-clientflow}
      POSTGRES_USER: ${POSTGRES_USER:-clientflow}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-clientflow_secure_password}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-clientflow} -d ${POSTGRES_DB:-clientflow}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: clientflow_redis
    restart: unless-stopped
    command: ["redis-server", "--appendonly", "yes"]
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
      dockerfile: docker/Dockerfile.backend
    container_name: clientflow_backend
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    env_file:
      - .env.example
    environment:
      DATABASE_URL: postgresql+asyncpg://${POSTGRES_USER:-clientflow}:${POSTGRES_PASSWORD:-clientflow_secure_password}@postgres:5432/${POSTGRES_DB:-clientflow}
      DATABASE_SYNC_URL: postgresql://${POSTGRES_USER:-clientflow}:${POSTGRES_PASSWORD:-clientflow_secure_password}@postgres:5432/${POSTGRES_DB:-clientflow}
      REDIS_URL: redis://redis:6379/0
      CELERY_BROKER_URL: redis://redis:6379/1
    ports:
      - "8000:8000"

  celery_worker:
    build:
      context: .
      dockerfile: docker/Dockerfile.worker
    container_name: clientflow_worker
    restart: unless-stopped
    depends_on:
      backend:
        condition: service_started
      redis:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql+asyncpg://${POSTGRES_USER:-clientflow}:${POSTGRES_PASSWORD:-clientflow_secure_password}@postgres:5432/${POSTGRES_DB:-clientflow}
      CELERY_BROKER_URL: redis://redis:6379/1
      CELERY_RESULT_BACKEND: redis://redis:6379/2

  celery_beat:
    build:
      context: .
      dockerfile: docker/Dockerfile.worker
    container_name: clientflow_beat
    restart: unless-stopped
    command: ["celery", "-A", "workers.celery_app.celery_app", "beat", "--loglevel=info"]
    depends_on:
      redis:
        condition: service_healthy
    environment:
      CELERY_BROKER_URL: redis://redis:6379/1

  frontend:
    build:
      context: .
      dockerfile: docker/Dockerfile.frontend
    container_name: clientflow_frontend
    restart: unless-stopped
    depends_on:
      backend:
        condition: service_started
    ports:
      - "80:80"

volumes:
  postgres_data:
  redis_data:
""")

    # 6. .github/workflows/ci.yml
    write_file(".github/workflows/ci.yml", """name: ClientFlow CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  backend-test-suite:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.13
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Install Python Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r backend/requirements.txt
          pip install pytest pytest-asyncio httpx aiosqlite ruff mypy

      - name: Run Code Linter & Format Check
        run: |
          python scripts/check_all_imports.py

      - name: Execute Pytest Suite (Unit, Integration, Security, E2E)
        run: |
          pytest tests/ -v --cov=backend/app --cov-report=xml

  frontend-test-suite:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js 20
        uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Install Frontend Dependencies
        working-directory: frontend
        run: npm ci

      - name: Typecheck TypeScript & Build Production SPA Bundle
        working-directory: frontend
        run: npm run build
""")

    print("Milestone 28 Docker & CI/CD generated successfully!")

if __name__ == '__main__':
    run()
