# ClientFlow CRM — Changelog

## [1.0.0] - Enterprise Baseline Release
### Added
- **Backend Foundation**: Layered FastAPI architecture, async SQLAlchemy 2.0, Argon2id security, JWT authentication, TOTP MFA.
- **Multi-Tenancy & RBAC**: Organization hierarchy, membership management, teams, permissions.
- **Core CRM**: Contacts with fuzzy deduplication, Companies with parent-subsidiary trees, Leads with configurable scoring engine.
- **Sales Engine**: Pipelines, stages, SLAs, Deal Kanban board with stage validations.
- **Quote-to-Cash**: Product catalog, Proposals, Quotes, Invoices with payment reconciliation.
- **Customer Operations**: Omnichannel support tickets, SLA alerts, Customer Success plans with automated health scoring.
- **Intelligence & Automation**: Marketing campaigns, visual workflow automation engine, AI Copilot assistant.
- **Search & Analytics**: Global CRM search, Executive KPI dashboard with funnel metrics.
- **Frontend SPA**: Modern React 18 + TypeScript + Vite + Tailwind CSS application.
- **Workers & DevOps**: Celery worker suite with Redis broker, Docker compose orchestration, GitHub Actions CI/CD.
