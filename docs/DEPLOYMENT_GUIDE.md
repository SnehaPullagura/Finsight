# ClientFlow CRM — Production Deployment Guide

## 1. Prerequisites
- Docker Engine 24+ & Docker Compose v2
- PostgreSQL 16+
- Redis 7+

## 2. Quick Start with Docker Compose
```bash
# 1. Clone repository
git clone https://github.com/SnehaPullagura/clientflowCRM.git
cd clientflowCRM

# 2. Configure Environment
cp .env.example .env

# 3. Build & Launch Containers
docker compose up -d --build

# 4. Verify Services
docker compose ps
curl http://localhost:8000/api/v1/health
```

## 3. Production Service Topology
- `clientflow_postgres`: Port 5432
- `clientflow_redis`: Port 6379
- `clientflow_backend`: Port 8000 (FastAPI ASGI)
- `clientflow_worker`: Celery task worker
- `clientflow_beat`: Celery scheduled periodic runner
- `clientflow_frontend`: Port 80 (Nginx Reverse Proxy & React SPA)
