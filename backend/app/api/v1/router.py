from fastapi import APIRouter
from backend.app.auth.router import router as auth_router
from backend.app.accounts.router import router as accounts_router
from backend.app.categories.router import router as categories_router
from backend.app.transactions.router import router as transactions_router
from backend.app.budgets.router import router as budgets_router
from backend.app.goals.router import router as goals_router
from backend.app.recurring.router import router as recurring_router
from backend.app.intelligence.router import router as intelligence_router
from backend.app.cashflow.router import router as cashflow_router
from backend.app.health.router import router as health_router
from backend.app.anomaly.router import router as anomaly_router
from backend.app.forecasting.router import router as forecasting_router
from backend.app.analytics.router import router as analytics_router
from backend.app.scenarios.router import router as scenarios_router
from backend.app.assistant.router import router as assistant_router
from backend.app.notifications.router import router as notifications_router
from backend.app.imports.router import router as imports_router
from backend.app.reports.router import router as reports_router
from backend.app.admin.router import router as admin_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(accounts_router)
api_router.include_router(categories_router)
api_router.include_router(transactions_router)
api_router.include_router(budgets_router)
api_router.include_router(goals_router)
api_router.include_router(recurring_router)
api_router.include_router(intelligence_router)
api_router.include_router(cashflow_router)
api_router.include_router(health_router)
api_router.include_router(anomaly_router)
api_router.include_router(forecasting_router)
api_router.include_router(analytics_router)
api_router.include_router(scenarios_router)
api_router.include_router(assistant_router)
api_router.include_router(notifications_router)
api_router.include_router(imports_router)
api_router.include_router(reports_router)
api_router.include_router(admin_router)
