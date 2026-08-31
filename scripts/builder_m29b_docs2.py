import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. docs/AUTOMATION_ENGINE.md
    write_file("docs/AUTOMATION_ENGINE.md", """# ClientFlow CRM — Workflow Automation Engine

## 1. Trigger-Condition-Action Architecture
The Automation Engine allows organizations to define event-driven business rules:

```
Domain Event (e.g. `deal.stage_changed`, `lead.created`)
        │
        ▼
Trigger Matching Filter
        │
        ▼
Conditional Evaluation Engine (eq, gt, gte, lt, lte, contains)
        │
        ▼
Sequential Action Dispatch (Task Creation, Email Notification, Webhook, Status Update)
        │
        ▼
Execution Log & Audit Ledger
```

## 2. Supported Conditions & Operators
- `gt`, `gte`, `lt`, `lte`: Numeric evaluations (e.g., deal value > $50,000).
- `eq`: Exact string or numeric equality.
- `contains`: Substring matching on text attributes.
""")

    # 2. docs/AI_INTEGRATION.md
    write_file("docs/AI_INTEGRATION.md", """# ClientFlow CRM — AI Intelligence Engine

## 1. Capabilities
- **Customer 360 & Lead Fit Synthesis**: Generates qualification rationales, key strengths, risk factors, and recommended next steps.
- **Deal Risk & Momentum Scoring**: Evaluates stage age, stakeholder engagement, and probability to flag high-risk deals early.
- **Context-Aware Email Drafter**: Creates customized outreach messages based on CRM conversation topic and objective.
- **Natural Language Querying**: Translates conversational questions into structured CRM filters and summaries.

## 2. Architecture
Pluggable provider architecture with fallbacks for Gemini, OpenAI, Claude, and built-in offline heuristic reasoning.
""")

    # 3. docs/DEPLOYMENT_GUIDE.md
    write_file("docs/DEPLOYMENT_GUIDE.md", """# ClientFlow CRM — Production Deployment Guide

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
""")

    # 4. docs/CONFIGURATION_REFERENCE.md
    write_file("docs/CONFIGURATION_REFERENCE.md", """# ClientFlow CRM — Configuration Reference

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
""")

    # 5. docs/TESTING_STRATEGY.md
    write_file("docs/TESTING_STRATEGY.md", """# ClientFlow CRM — Testing Strategy & Quality Assurance

## 1. Test Architecture
ClientFlow implements automated testing across 4 key tiers:
1. **Unit Tests** (`tests/unit/`): Pure business logic (qualification scoring rules, condition evaluator).
2. **Integration Tests** (`tests/integration/`): HTTP REST lifecycle with in-memory database.
3. **Security Isolation Tests** (`tests/security/`): Strict multi-tenant data leakage prevention.
4. **End-to-End CRM Lifecycle Tests** (`tests/e2e/`): Complete business flow from registration to customer success.

## 2. Running Test Suite
```bash
pytest tests/ -v
```
""")

    print("Documentation Suite Part 2 generated.")

if __name__ == '__main__':
    run()
