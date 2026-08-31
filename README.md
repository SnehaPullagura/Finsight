# ClientFlow CRM 🚀

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
