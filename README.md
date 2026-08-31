# FinSight — AI-Powered Financial Health, Cash-Flow Intelligence & Scenario Simulation Platform

[![Build & Test Status](https://img.shields.io/badge/Tests-Passing%20(100%25)-success?style=flat-square)](https://github.com/SnehaPullagura/Finsight)
[![Architecture](https://img.shields.io/badge/Architecture-Modular%20Monolith%20(19%20Modules)-blue?style=flat-square)](https://github.com/SnehaPullagura/Finsight)
[![ML Models](https://img.shields.io/badge/ML%20Engine-3%20Core%20Models-purple?style=flat-square)](https://github.com/SnehaPullagura/Finsight)
[![License](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)](LICENSE)

---

## Executive Overview
**FinSight** is an enterprise personal and small-business financial decision-support and scenario simulation platform. Built as a high-performance modular monolith with strict service boundaries, FinSight connects multi-institution financial accounts and transforms raw transaction ledgers into actionable forward-looking intelligence.

Unlike generic historical expense trackers, FinSight focuses on **forward-looking decision intelligence** anchored by three core identity pillars:
1. **Financial Health Engine**: Proprietary 6-pillar scoring model (0–100) with explainability and actionable improvement vectors.
2. **Future Cash-Flow Prediction**: Multi-horizon (30/60/90-day) projected balances, safe-to-spend liquidity limits, and shortage probability bands.
3. **What-If Scenario Simulator**: Dynamic multi-variable simulator for evaluating salary increases, major purchases, loans, and EMIs before committing money.

---

## Key Features & 19-Module Architecture

| Domain | Modules | Capabilities |
|---|---|---|
| **Foundation & Security** | `auth`, `accounts`, `categories`, `core` | JWT Authentication, Masked Account Numbers (`XXXX-XXXX-1234`), 30+ Standard Taxonomies, Audit Trails. |
| **Financial Core** | `transactions`, `budgets`, `goals`, `recurring` | Split Transactions, Real-time 50/30/20 Budget Caps, Sufficiency Milestones, Auto-detected Subscriptions & EMIs. |
| **Intelligence & ML** | `intelligence`, `cashflow`, `health`, `anomaly`, `forecasting`, `analytics` | NLP Normalization, 6-Pillar Health Score, Isolation Forest Anomaly Detection, Holt-Winters + Ridge Forecaster. |
| **Simulations & AI** | `scenarios`, `assistant` | What-If Simulator with Balance Deltas, Data-Grounded RAG Financial Assistant with Fact Verification. |
| **Platform Ops** | `notifications`, `imports`, `reports`, `admin` | Real-time In-app Alerts, CSV/Excel Statement ETL Pipeline, Automated Report Exports, ML Model Governance Registry. |

---

## Machine Learning Engine (Exactly 3 Core Models)

1. **Transaction Categorization Model** (`ml_engine/models/categorizer.py`):
   - Hybrid Rule-Based Regex + TF-IDF Vectorizer with Calibrated SGD Classifier.
   - Sub-5ms inference latency with user feedback correction loop.
2. **Expense Forecasting Model** (`ml_engine/models/forecaster.py`):
   - Holt-Winters Exponential Smoothing + Ridge Regression with 95% Confidence Interval bands.
   - Multi-horizon (30/60/90-day) projected cash outlays and shortage risk assessment.
3. **Financial Anomaly Detector** (`ml_engine/models/anomaly_detector.py`):
   - Robust Z-Score + Scikit-Learn Isolation Forest.
   - Flags spending spikes (>3σ vs baseline), duplicate charges, and unusual recurring variances.

---

## Tech Stack
- **Backend**: Python 3.13, FastAPI, SQLAlchemy 2.0 (Async + Sync), Pydantic v2, Scikit-Learn, NumPy, Pandas.
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Lucide React, Modern Glassmorphic Design System.
- **Database**: SQLite (Development / Demo) / PostgreSQL (Production).
- **Background Worker**: Celery + Redis / Async Worker Queue.
- **DevOps**: Docker, Docker Compose, Nginx.

---

## Quick Start & Installation

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- Git

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/SnehaPullagura/Finsight.git
cd Finsight

# Create virtual environment
python -m venv .venv
# Activate on Windows:
.venv\Scripts\activate
# Activate on Linux/macOS:
source .venv/bin/activate

# Install backend dependencies
pip install -e .
```

### 2. Seed Demo Persona (Realistic 90-Day Financial History)
```bash
python -m scripts.seed_demo_data
```
*Creates demo user `chaitanya.tech@finsight.app` (Password: `SecurePassword123!`) with 5 accounts (HDFC, ICICI, Zerodha), 60+ transactions, budgets, goals, and recurring EMIs.*

### 3. Start Backend API Server
```bash
uvicorn backend.app.main:app --reload --port 8000
```
*API Swagger Documentation is available at `http://localhost:8000/docs`.*

### 4. Build & Start Frontend Application
```bash
cd frontend
npm install
npm run build
npm run dev
```
*The FinSight SPA is accessible at `http://localhost:3000`.*

---

## Running Automated Tests & ML Evaluation

### Execute Pytest Test Suite
```bash
pytest tests/ -v --cov=backend/app --cov=ml_engine
```

### Execute ML Engine Evaluation
```bash
python -m ml_engine.evaluation.evaluate_models
```

---

## Docker Deployment

To launch the full production stack using Docker Compose:
```bash
docker-compose up --build -d
```
- Frontend Web App: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- OpenAPI Specification: `http://localhost:8000/api/v1/openapi.json`

---

## Handover & Operational Runbook
Refer to [`docs/handover.md`](docs/handover.md) for full architectural blueprints, disaster recovery runbooks, SLA policies, and contact escalation matrices.

---

## License
Proprietary and Confidential. Copyright © 2026 FinSight Engineering Team. All rights reserved.
