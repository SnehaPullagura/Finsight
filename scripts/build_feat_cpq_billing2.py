import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/cpq/engine.py
    write_file("backend/app/cpq/engine.py", """import math
from typing import Dict, List, Optional, Tuple
from decimal import Decimal, ROUND_HALF_UP

CURRENCY_EXCHANGE_RATES: Dict[str, float] = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "CAD": 1.36,
    "AUD": 1.52,
    "JPY": 155.20,
    "INR": 83.45,
    "SGD": 1.35,
    "CHF": 0.91,
}

class CurrencyConversionService:
    @staticmethod
    def convert(amount: float, from_currency: str, to_currency: str) -> float:
        from_curr = from_currency.upper()
        to_curr = to_currency.upper()
        if from_curr == to_curr:
            return round(amount, 2)

        base_usd_rate = CURRENCY_EXCHANGE_RATES.get(from_curr, 1.0)
        target_rate = CURRENCY_EXCHANGE_RATES.get(to_curr, 1.0)

        # Convert to USD base then to target
        amount_usd = amount / base_usd_rate
        converted = amount_usd * target_rate
        return round(converted, 2)

    @staticmethod
    def get_supported_currencies() -> List[str]:
        return list(CURRENCY_EXCHANGE_RATES.keys())

class CPQPricingEngine:
    @staticmethod
    def evaluate_volume_tier(quantity: int, tiers: list) -> Tuple[float, float]:
        selected_discount_pct = 0.0
        selected_flat_amount = 0.0

        for tier in sorted(tiers, key=lambda t: t.tier_order):
            lower = tier.lower_bound
            upper = tier.upper_bound or float("inf")

            if lower <= quantity <= upper:
                selected_discount_pct = float(tier.discount_percentage)
                selected_flat_amount = float(tier.flat_discount_amount or 0.0)
                break

        return selected_discount_pct, selected_flat_amount

    @staticmethod
    def calculate_line_item(
        unit_price: float,
        quantity: int,
        discount_percentage: float = 0.0,
        flat_discount: float = 0.0,
        tax_rate_pct: float = 0.0
    ) -> Dict[str, float]:
        subtotal = round(unit_price * quantity, 2)
        pct_discount_amount = round(subtotal * (discount_percentage / 100.0), 2)
        total_discount = min(subtotal, round(pct_discount_amount + flat_discount, 2))
        
        net_amount = max(0.0, round(subtotal - total_discount, 2))
        tax_amount = round(net_amount * (tax_rate_pct / 100.0), 2)
        total_amount = round(net_amount + tax_amount, 2)

        return {
            "subtotal": subtotal,
            "discount_amount": total_discount,
            "net_amount": net_amount,
            "tax_amount": tax_amount,
            "total_amount": total_amount
        }
""")

    # 2. backend/app/billing/engine.py
    write_file("backend/app/billing/engine.py", """from datetime import date, timedelta
from typing import Dict, List, Optional
from decimal import Decimal

class SubscriptionEngine:
    @staticmethod
    def calculate_proration(
        current_amount: float,
        start_date: date,
        end_date: date,
        effective_date: date
    ) -> float:
        total_days = (end_date - start_date).days
        if total_days <= 0:
            return 0.0

        remaining_days = (end_date - effective_date).days
        if remaining_days <= 0:
            return 0.0

        proration_factor = remaining_days / total_days
        prorated_amount = current_amount * proration_factor
        return round(prorated_amount, 2)

    @staticmethod
    def calculate_subscription_waterfall(
        monthly_base: float,
        frequency: str = "monthly",
        term_months: int = 12
    ) -> Dict[str, float]:
        freq = frequency.lower()
        if freq == "monthly":
            mrr = monthly_base
            arr = mrr * 12.0
            billing_amount = monthly_base
        elif freq == "quarterly":
            mrr = monthly_base
            arr = mrr * 12.0
            billing_amount = monthly_base * 3.0
        elif freq == "annual":
            mrr = monthly_base
            arr = mrr * 12.0
            billing_amount = monthly_base * 12.0 * 0.90 # 10% annual discount
        else:
            mrr = monthly_base
            arr = mrr * 12.0
            billing_amount = monthly_base

        return {
            "mrr": round(mrr, 2),
            "arr": round(arr, 2),
            "billing_amount": round(billing_amount, 2),
            "total_contract_value": round(mrr * term_months, 2)
        }

    @staticmethod
    def calculate_upgrade_delta(
        old_mrr: float,
        new_mrr: float,
        period_start: date,
        period_end: date,
        change_date: date
    ) -> Dict[str, float]:
        total_days = max(1, (period_end - period_start).days)
        unused_days = max(0, (period_end - change_date).days)
        factor = unused_days / total_days

        unused_old_credit = round(old_mrr * factor, 2)
        prorated_new_charge = round(new_mrr * factor, 2)
        net_payable_delta = max(0.0, round(prorated_new_charge - unused_old_credit, 2))

        return {
            "credit_for_unused_old_plan": unused_old_credit,
            "charge_for_new_plan": prorated_new_charge,
            "net_payable_now": net_payable_delta,
            "new_recurring_mrr": new_mrr
        }
""")

    # 3. backend/app/cpq/schemas.py & backend/app/billing/schemas.py
    write_file("backend/app/cpq/schemas.py", """from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class CurrencyConvertRequest(BaseModel):
    amount: float
    from_currency: str = "USD"
    to_currency: str = "EUR"

class CurrencyConvertResponse(BaseModel):
    original_amount: float
    from_currency: str
    converted_amount: float
    to_currency: str
    rate: float

class PriceCalculationItem(BaseModel):
    product_id: str
    unit_price: float
    quantity: int
    discount_percentage: Optional[float] = 0.0
    flat_discount: Optional[float] = 0.0
    tax_rate_pct: Optional[float] = 0.0

class CPQCalculationResponse(BaseModel):
    subtotal: float
    total_discount: float
    net_amount: float
    tax_amount: float
    total_amount: float
    currency: str
    line_breakdowns: List[Dict[str, float]]
""")

    write_file("backend/app/billing/schemas.py", """from datetime import date
from typing import Dict, List, Optional
from pydantic import BaseModel

class SubscriptionCreateRequest(BaseModel):
    company_id: str
    contact_id: Optional[str] = None
    plan_name: str
    billing_frequency: str = "monthly" # monthly, quarterly, annual
    monthly_base_price: float
    currency: str = "USD"
    start_date: Optional[date] = None

class SubscriptionResponse(BaseModel):
    id: str
    company_id: str
    plan_name: str
    status: str
    billing_frequency: str
    currency: str
    mrr_amount: float
    arr_amount: float
    start_date: date
    current_period_start: date
    current_period_end: date
    auto_renew: bool

class UpgradePlanRequest(BaseModel):
    new_plan_name: str
    new_monthly_price: float
    effective_date: Optional[date] = None

class ProrationPreviewResponse(BaseModel):
    credit_for_unused_old_plan: float
    charge_for_new_plan: float
    net_payable_now: float
    new_recurring_mrr: float
""")

    # 4. Endpoints
    write_file("backend/app/api/v1/endpoints/cpq.py", """from fastapi import APIRouter, Depends, status
from backend.app.schemas.cpq import (
    CurrencyConvertRequest,
    CurrencyConvertResponse,
    PriceCalculationItem,
    CPQCalculationResponse
)
from backend.app.cpq.engine import CurrencyConversionService, CPQPricingEngine

router = APIRouter()

@router.post("/convert-currency", response_model=CurrencyConvertResponse)
async def convert_currency(req: CurrencyConvertRequest):
    converted = CurrencyConversionService.convert(req.amount, req.from_currency, req.to_currency)
    rate = round(converted / req.amount, 4) if req.amount > 0 else 1.0
    return CurrencyConvertResponse(
        original_amount=req.amount,
        from_currency=req.from_currency.upper(),
        converted_amount=converted,
        to_currency=req.to_currency.upper(),
        rate=rate
    )

@router.post("/calculate-pricing", response_model=CPQCalculationResponse)
async def calculate_quote_pricing(items: list[PriceCalculationItem], currency: str = "USD"):
    subtotal = 0.0
    total_disc = 0.0
    net = 0.0
    tax = 0.0
    grand_total = 0.0
    breakdowns = []

    for item in items:
        res = CPQPricingEngine.calculate_line_item(
            unit_price=item.unit_price,
            quantity=item.quantity,
            discount_percentage=item.discount_percentage or 0.0,
            flat_discount=item.flat_discount or 0.0,
            tax_rate_pct=item.tax_rate_pct or 0.0
        )
        subtotal += res["subtotal"]
        total_disc += res["discount_amount"]
        net += res["net_amount"]
        tax += res["tax_amount"]
        grand_total += res["total_amount"]
        breakdowns.append(res)

    return CPQCalculationResponse(
        subtotal=round(subtotal, 2),
        total_discount=round(total_disc, 2),
        net_amount=round(net, 2),
        tax_amount=round(tax, 2),
        total_amount=round(grand_total, 2),
        currency=currency.upper(),
        line_breakdowns=breakdowns
    )
""")

    write_file("backend/app/api/v1/endpoints/billing.py", """from datetime import date, timedelta
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.database import get_db
from backend.app.api.deps import get_current_tenant_id
from backend.app.schemas.billing import (
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
""")

    print("CPQ and Billing Engine, Schemas, and Endpoints created.")

if __name__ == '__main__':
    run()
