import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. docs/ARCHITECTURE.md
    write_file("docs/ARCHITECTURE.md", """# ClientFlow CRM — System Architecture & Technical Design

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
""")

    # 2. docs/DATABASE_SCHEMA.md
    write_file("docs/DATABASE_SCHEMA.md", """# ClientFlow CRM — Database Schema Reference

## 1. Overview
ClientFlow utilizes PostgreSQL 16 with UUID primary keys (RFC 4122 v4) across all tables, ensuring distributed generation and zero sequential enumeration vulnerability.

## 2. Core Entities & Relationship Graph

### Identity & Access
- `users`: Core user accounts (Argon2id passwords, TOTP MFA, roles).
- `roles` & `permissions`: Granular RBAC definitions with junction table mappings.
- `user_sessions`: Active JWT sessions with IP and user-agent tracing.

### Tenancy & Organizations
- `organizations`: Root tenant entity with plan tiers and custom settings.
- `organization_members`: User-organization membership with owner flags.
- `teams` & `team_members`: Organizational sub-units and team hierarchies.

### CRM Core
- `contacts`: Individual person profiles with lifecycle stages and custom fields.
- `companies`: Corporate organizations with annual revenue, industry, employee scale.
- `leads`: Inbound/outbound prospects with dynamic scores and qualification grades (A-F).
- `lead_scoring_rules`: Multi-criteria heuristic rules.

### Sales & Revenue
- `pipelines` & `pipeline_stages`: Configurable sales pipelines with stage probabilities and SLAs.
- `deals`: Revenue opportunities moving across pipeline stages.
- `products`: Catalog items, service offerings, SKU tracking.
- `proposals` & `proposal_line_items`: Formal customer proposals with acceptance tracking.
- `quotes` & `quote_line_items`: Price quotations with revision control.
- `invoices` & `invoice_payments`: Invoicing engine with payment reconciliation.

### Customer Operations
- `activities`: Polymorphic timeline events across any entity type.
- `tasks`: Action queues with recurring scheduling.
- `calendar_events`: Meeting coordination and attendee status.
- `support_tickets`: SLA-governed customer support tickets.
- `customer_success_plans` & `onboarding_milestones`: Health scoring engine.
- `communication_messages` & `communication_templates`: Multi-channel dispatch.
- `documents` & `document_versions`: File vault with SHA-256 integrity.

### Growth & Engine
- `campaigns` & `campaign_segments`: Targeted marketing broadcasts.
- `automation_workflows`: Trigger-condition-action workflow automation.
- `custom_field_definitions`: Dynamic entity field schema extensibility.
- `audit_logs`: Centralized immutable compliance audit ledger.
""")

    # 3. docs/API_DOCUMENTATION.md
    write_file("docs/API_DOCUMENTATION.md", """# ClientFlow CRM — REST API Documentation

## Base URL
`/api/v1`

## Authentication
Bearer JWT Token passed in `Authorization: Bearer <token>` header, accompanied by `X-Tenant-ID: <tenant_id>`.

## Endpoint Matrix

| Domain | Route | Method | Description |
|---|---|---|---|
| **Health** | `/health` | GET | System health & subsystem diagnostics |
| **Auth** | `/auth/register` | POST | Register new tenant & administrator |
| | `/auth/login` | POST | Authenticate & retrieve JWT tokens |
| | `/auth/refresh` | POST | Refresh expired access token |
| | `/auth/me` | GET | Current user profile |
| | `/auth/mfa/setup` | POST | Generate TOTP secret and QR URI |
| | `/auth/mfa/verify` | POST | Validate TOTP 6-digit code |
| **Organizations** | `/organizations` | POST/GET | Organization management |
| | `/organizations/members` | GET/POST | Team membership |
| **Contacts** | `/contacts` | GET/POST | Contact CRUD |
| | `/contacts/{id}` | GET/PUT/DELETE | Single contact operations |
| | `/contacts/deduplicate` | GET | Fuzzy deduplication search |
| **Companies** | `/companies` | GET/POST | Company CRUD |
| | `/companies/{id}` | GET/PUT/DELETE | Company profile & hierarchies |
| **Leads** | `/leads` | GET/POST | Lead management |
| | `/leads/{id}/qualify` | POST | Trigger rule-based qualification |
| | `/leads/{id}/convert` | POST | 1-Click convert to Contact+Company+Deal |
| **Pipelines & Deals** | `/pipelines` | GET/POST | Pipeline & stage configuration |
| | `/deals` | GET/POST | Deal records |
| | `/deals/kanban` | GET | Board grouped by pipeline stages |
| | `/deals/{id}/stage` | POST | Transition deal stage with SLA validation |
| **Activities** | `/activities/timeline/{type}/{id}` | GET | Polymorphic event timeline |
| | `/activities` | POST | Log call, email, meeting, note |
| **Tasks & Calendar** | `/tasks` | GET/POST | Task queue |
| | `/calendar/events` | GET/POST | Meeting schedule |
| **Quote to Cash** | `/products` | GET/POST | Product catalog |
| | `/proposals` | GET/POST | Proposal generator |
| | `/proposals/{id}/accept` | POST | Proposal customer acceptance |
| | `/quotes` | GET/POST | Quotation management |
| | `/invoices` | GET/POST | Invoices & billing |
| | `/invoices/{id}/payments` | POST | Record invoice payment |
| **Customer Support** | `/support/tickets` | GET/POST | Support tickets |
| | `/support/tickets/{id}/resolve` | POST | Ticket resolution |
| **Customer Success** | `/customer-success/plans` | GET/POST | Success plans & health tracking |
| | `/customer-success/plans/{id}/recalculate-health` | POST | Trigger health score formula |
| **Marketing & Automations** | `/campaigns` | GET/POST | Campaign broadcasts |
| | `/automations` | GET/POST | Workflow rules |
| **Search & Analytics** | `/search?q=...` | GET | Global search engine across CRM |
| | `/analytics/dashboard` | GET | Real-time executive KPIs & funnel |
| **AI Assistant** | `/ai/summarize/lead/{id}` | POST | AI lead synthesis & fit score |
| | `/ai/analyze/deal/{id}` | POST | Deal risk analysis & win probability |
| | `/ai/draft/email` | POST | Contextual email generator |
| | `/ai/query` | POST | Natural language query translator |
""")

    # 4. docs/FRONTEND_ARCHITECTURE.md
    write_file("docs/FRONTEND_ARCHITECTURE.md", """# ClientFlow CRM — Frontend Architecture

## 1. Technology Stack
- **Framework**: React 18 SPA (TypeScript 5.x)
- **Build Tool**: Vite 6 (Fast HMR & Optimized Bundles)
- **Styling**: Tailwind CSS v3 with custom Slate & Emerald enterprise color taxonomy
- **Icons**: Lucide React
- **HTTP Client**: Axios with automatic JWT refresh interceptor & tenant header injection
- **Routing**: React Router v6 with `ProtectedRoute` guards

## 2. Component Organization
```
frontend/src/
├── components/
│   ├── layout/       # AppLayout, Navbar, Sidebar
│   ├── common/       # GlobalSearchModal, DataTable, MetricCard
│   └── ai-assistant/ # AICopilotDrawer
├── context/          # AuthContext & TenantContext
├── pages/            # 16 domain pages (Dashboard, Contacts, Deals, etc.)
├── services/         # Typed API client wrapper
├── types/            # Complete TypeScript interfaces
├── App.tsx           # Route definitions
└── main.tsx          # Application entrypoint
```
""")

    # 5. docs/SECURITY_MODEL.md
    write_file("docs/SECURITY_MODEL.md", """# ClientFlow CRM — Security Architecture & Threat Model

## 1. Authentication & Session Security
- **Password Hashing**: Argon2id with memory-hard parameters (fallback to Bcrypt).
- **JWT Cryptography**: Signed with HMAC-SHA256, strictly validated `exp`, `sub`, `tenant_id`, and `roles` claims.
- **Two-Factor Authentication**: RFC 6238 TOTP with QR provisioning and backup recovery codes.

## 2. Multi-Tenant Isolation Model
- Hard database-level tenant isolation enforced via `TenantMixin` and repository query filters.
- Middleware validates tenant access permissions against authenticated user's organization memberships.

## 3. Defense-in-Depth Measures
- OWASP Top 10 mitigation:
  - Strict input sanitization via Pydantic v2.
  - SQL Injection prevention through parameterized SQLAlchemy ORM queries.
  - Security headers: `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`.
  - Rate limiting & request tracing via unique request correlation IDs (`X-Request-ID`).
""")

    print("Documentation Suite Part 1 generated.")

if __name__ == '__main__':
    run()
