import os
from scripts.common import write_file

def enhance_repo():
    print("Enhancing repository with CI/CD workflows, security tests, and rich test suites...")

    # 1. GitHub Actions CI Workflows
    write_file(".github/workflows/ci.yml", """name: FinSight CI Pipeline

on:
  push:
    branches: [ main, feature/* ]
  pull_request:
    branches: [ main ]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .

    - name: Run Backend Pytest & Coverage
      run: |
        pytest tests/ -v --cov=backend/app --cov=ml_engine --cov-report=xml --cov-report=term

    - name: Run ML Engine Evaluation
      run: |
        python -m ml_engine.evaluation.evaluate_models

  frontend-build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20.x'
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json

    - name: Build Frontend SPA
      run: |
        cd frontend
        npm ci || npm install
        npm run build
""")

    write_file(".github/workflows/cd.yml", """name: FinSight CD Pipeline

on:
  push:
    tags:
      - 'v*'

jobs:
  docker-build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: actions/setup-buildx-action@v3

    - name: Build Backend Container
      uses: docker/build-push-action@v5
      with:
        context: .
        file: backend/Dockerfile
        push: false
        tags: finsight-backend:latest

    - name: Build Frontend Container
      uses: docker/build-push-action@v5
      with:
        context: ./frontend
        file: frontend/Dockerfile
        push: false
        tags: finsight-frontend:latest
""")

    # 2. Security & Masking Tests
    write_file("tests/security/test_masking_security.py", """
import pytest
from backend.app.core.masking import (
    mask_account_number, mask_credit_card, mask_pan_or_ssn,
    mask_email, sanitize_transaction_description, redact_sensitive_dict
)

def test_masking_algorithms():
    # Bank Account
    assert mask_account_number("123456789012") == "XXXX-XXXX-9012"
    assert mask_account_number("1234") == "XXXX"

    # Credit Card
    assert mask_credit_card("4111222233334444") == "•••• •••• •••• 4444"

    # Email
    assert mask_email("chaitanya.tech@finsight.app") == "c***h@finsight.app"

    # Description sanitization
    dirty = "Payment for loan card 4111222233334444 to account 123456789012"
    clean = sanitize_transaction_description(dirty)
    assert "4111222233334444" not in clean
    assert "123456789012" not in clean

    # Redact dictionary
    sensitive = {
        "user": "Chaitanya",
        "password": "SecretPassword123!",
        "token": "bearer xyz-jwt",
        "access_token": "abc-123",
        "public_data": "visible"
    }
    redacted = redact_sensitive_dict(sensitive)
    assert redacted["password"] == "[REDACTED]"
    assert redacted["token"] == "[REDACTED]"
    assert redacted["access_token"] == "[REDACTED]"
    assert redacted["public_data"] == "visible"
""")

    # 3. End-to-End Scenario & Cash-Flow Lifecycle Tests
    write_file("tests/e2e/test_scenarios_e2e.py", """
import pytest
import datetime
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_full_scenario_simulation_e2e(client: AsyncClient):
    # 1. Register & Login
    await client.post("/api/v1/auth/register", json={
        "email": "e2e.user@finsight.app",
        "password": "Password123!",
        "full_name": "Scenario Master"
    })
    token = (await client.post("/api/v1/auth/login", json={
        "email": "e2e.user@finsight.app",
        "password": "Password123!"
    })).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Add Checking & Savings Accounts
    await client.post("/api/v1/accounts", json={
        "name": "Salary Account",
        "account_type": "savings",
        "current_balance": 150000.0,
        "is_primary": True
    }, headers=headers)

    # 3. Run Scenario 1: Car Loan Simulation
    sc1 = await client.post("/api/v1/scenarios", json={
        "name": "EV Car Purchase",
        "monthly_income_delta": 0.0,
        "monthly_expense_delta": -2000.0, # fuel savings
        "one_time_lump_sum": 200000.0,
        "loan_amount": 600000.0,
        "loan_tenure_months": 36,
        "loan_interest_rate": 8.5
    }, headers=headers)
    assert sc1.status_code == 201
    d1 = sc1.json()
    assert d1["calculated_monthly_emi"] > 0
    assert d1["is_feasible"] == True

    # 4. Run Scenario 2: High Risk Infeasible Purchase
    sc2 = await client.post("/api/v1/scenarios", json={
        "name": "Luxury Yacht Purchase",
        "monthly_income_delta": 0.0,
        "monthly_expense_delta": 50000.0,
        "one_time_lump_sum": 500000.0,
        "loan_amount": 2000000.0,
        "loan_tenure_months": 24,
        "loan_interest_rate": 14.0
    }, headers=headers)
    assert sc2.status_code == 201
    d2 = sc2.json()
    assert d2["is_feasible"] == False
    assert d2["health_score_delta"] < 0

    # 5. Side-by-side comparison
    cmp_res = await client.get("/api/v1/scenarios/compare", headers=headers)
    assert cmp_res.status_code == 200
    assert len(cmp_res.json()["scenarios"]) == 2
""")

    print("Repository enhanced successfully!")

if __name__ == "__main__":
    enhance_repo()
