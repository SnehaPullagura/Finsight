from datetime import date, timedelta
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_tenant_id
from backend.app.billing.schemas import (
    SubscriptionCreateRequest,
    SubscriptionResponse,
    UpgradePlanRequest,
    ProrationPreviewResponse
)
from backend.app.billing.engine import SubscriptionEngine
from backend.app.billing.models import Subscription

router = APIRouter()

@router.post("/subscriptions", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    req: SubscriptionCreateRequest,
    tenant_id: str = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db)
):
    waterfall = SubscriptionEngine.calculate_subscription_waterfall(
        monthly_base=req.monthly_base_price,
        frequency=req.billing_frequency
    )
    st_date = req.start_date or date.today()
    end_date = st_date + timedelta(days=30 if req.billing_frequency == "monthly" else 365)

    sub = Subscription(
        tenant_id=tenant_id,
        company_id=req.company_id,
        contact_id=req.contact_id,
        plan_name=req.plan_name,
        status="active",
        billing_frequency=req.billing_frequency,
        currency=req.currency,
        mrr_amount=waterfall["mrr"],
        arr_amount=waterfall["arr"],
        start_date=st_date,
        current_period_start=st_date,
        current_period_end=end_date,
        auto_renew=True
    )
    db.add(sub)
    await db.flush()
    await db.refresh(sub)
    return sub

@router.post("/subscriptions/preview-upgrade", response_model=ProrationPreviewResponse)
async def preview_upgrade(req: UpgradePlanRequest, current_mrr: float = 1000.0):
    start = date.today() - timedelta(days=10)
    end = date.today() + timedelta(days=20)
    delta = SubscriptionEngine.calculate_upgrade_delta(
        old_mrr=current_mrr,
        new_mrr=req.new_monthly_price,
        period_start=start,
        period_end=end,
        change_date=req.effective_date or date.today()
    )
    return ProrationPreviewResponse(**delta)
