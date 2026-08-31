# ClientFlow CRM — Testing Strategy & Quality Assurance

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
