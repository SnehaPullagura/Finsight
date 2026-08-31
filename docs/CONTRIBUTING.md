# ClientFlow CRM — Contribution Guidelines

## 1. Development Principle
- Layered architecture must be strictly respected: `API` ➔ `Router` ➔ `Schema` ➔ `Service` ➔ `Repository` ➔ `Database`.
- Multi-tenancy must never be bypassed: all entity queries must enforce `tenant_id`.
- Zero artificial code inflation: write clean, maintainable, production-ready code.

## 2. Git Branching
- `main`: Production release branch.
- `develop`: Primary integration branch.
- `feature/*`: Specific domain features.
