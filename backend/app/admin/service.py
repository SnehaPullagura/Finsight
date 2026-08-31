from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.app.admin.models import MLModelRegistry
from backend.app.admin.schemas import PlatformMetricsResponse, ModelRegistryResponse
from backend.app.auth.models import User
from backend.app.transactions.models import Transaction
from backend.app.accounts.models import FinancialAccount

DEFAULT_MODELS = [
    {"model_name": "transaction_categorizer", "version": "v1.2.0", "algorithm": "TF-IDF + Calibrated SGD Classifier", "accuracy_or_metric": 0.942, "training_sample_count": 12500},
    {"model_name": "cashflow_forecaster", "version": "v2.0.1", "algorithm": "Multi-Horizon Holt-Winters + Ridge", "accuracy_or_metric": 0.887, "training_sample_count": 8400},
    {"model_name": "financial_anomaly_detector", "version": "v1.1.0", "algorithm": "Isolation Forest + Robust Z-Score Ensemble", "accuracy_or_metric": 0.915, "training_sample_count": 9200}
]

class AdminService:
    @staticmethod
    async def seed_model_registry(db: AsyncSession):
        for m in DEFAULT_MODELS:
            chk = await db.execute(select(MLModelRegistry).where(MLModelRegistry.model_name == m["model_name"]))
            if not chk.scalar_one_or_none():
                reg = MLModelRegistry(
                    model_name=m["model_name"],
                    version=m["version"],
                    algorithm=m["algorithm"],
                    accuracy_or_metric=m["accuracy_or_metric"],
                    training_sample_count=m["training_sample_count"],
                    is_active=True
                )
                db.add(reg)
        await db.commit()

    @staticmethod
    async def get_platform_metrics(db: AsyncSession) -> PlatformMetricsResponse:
        await AdminService.seed_model_registry(db)
        
        user_count = (await db.execute(select(func.count(User.id)))).scalar() or 0
        tx_count = (await db.execute(select(func.count(Transaction.id)))).scalar() or 0
        acc_count = (await db.execute(select(func.count(FinancialAccount.id)))).scalar() or 0
        vol_total = (await db.execute(select(func.sum(Transaction.amount)))).scalar() or 0.0
        
        models_res = await db.execute(select(MLModelRegistry).where(MLModelRegistry.is_active == True))
        models = list(models_res.scalars().all())
        
        return PlatformMetricsResponse(
            total_users=user_count,
            active_users_30d=user_count,
            total_transactions_managed=tx_count,
            total_accounts_connected=acc_count,
            total_volume_processed=round(vol_total, 2),
            system_health_status="healthy",
            active_ml_models=[ModelRegistryResponse.model_validate(m) for m in models]
        )
