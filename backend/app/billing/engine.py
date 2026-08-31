from datetime import date, timedelta
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
