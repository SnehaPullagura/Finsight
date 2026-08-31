# ClientFlow CRM — System Architecture & Technical Design

## 1. Overview
ClientFlow CRM is an enterprise-grade, high-velocity Customer Relationship Management and Customer Operations platform designed for high concurrency, multi-tenant isolation, and modular domain separation.

## 2. Layered Architectural Hierarchy
ClientFlow enforces a strict unidirectional layered architecture:
```
Client Request (React SPA / Mobile / Webhook)
      │
      ▼
Reverse Proxy & Gateway (Nginx / Cloud Load Balancer)
      │
      ▼
FastAPI Application (ASGI Server / Uvicorn Workers)
      │
      ├─► Middleware Pipeline (Tracing, CORS, Security Headers, Tenant Resolution)
      │
      ├─► Routers & Endpoints (`backend/app/api/v1/endpoints/`)
      │
      ├─► DTO & Validation Schemas (`backend/app/schemas/`)
      │
      ├─► Domain Business Services (`backend/app/services/`)
      │
      ├─► Data Access Repositories (`backend/app/repositories/`)
      │
      └─► Persistence Models & ORM (`backend/app/models/`)
            │
            ├─► PostgreSQL 16 (Relational Multi-Tenant Primary Store)
            ├─► Redis 7 (Cache, Token Blacklist, Celery Message Broker)
            └─► OpenSearch / ElasticSearch (Global Full-Text Search)
```

## 3. Core Architectural Principles
1. **Zero Artificial Duplication**: Clean, DRY, generic repository and service base classes with typed SQLAlchemy 2.0 async sessions.
2. **Strict Multi-Tenant Isolation**: Every tenant-bound entity derives from `TenantMixin` and enforces `tenant_id` filtering at the repository layer.
3. **Decoupled Asynchronous Processing**: Heavy computations (campaign dispatch, SLA breach checks, health score rollups, AI syntheses) are delegated to Celery workers via Redis.
4. **Resilient Domain Event Bus**: In-memory and distributed event handlers allow cross-module coordination without tight coupling.
