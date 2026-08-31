from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class BillingProrationCalculator:
    @staticmethod
    def calculate_mid_cycle_upgrade(
        old_plan_mrr: float,
        new_plan_mrr: float,
        billing_cycle_start: date,
        billing_cycle_end: date,
        effective_date: date
    ) -> Dict[str, float]:
        total_cycle_days = max(1, (billing_cycle_end - billing_cycle_start).days)
        days_used = max(0, (effective_date - billing_cycle_start).days)
        days_remaining = max(0, (billing_cycle_end - effective_date).days)

        unused_fraction = days_remaining / float(total_cycle_days)

        unused_old_plan_credit = round(old_plan_mrr * unused_fraction, 2)
        prorated_new_plan_charge = round(new_plan_mrr * unused_fraction, 2)
        immediate_charge = max(0.0, round(prorated_new_plan_charge - unused_old_plan_credit, 2))

        return {
            "cycle_days_total": total_cycle_days,
            "days_used": days_used,
            "days_remaining": days_remaining,
            "unused_credit_amount": unused_old_plan_credit,
            "prorated_charge_amount": prorated_new_plan_charge,
            "immediate_amount_due": immediate_charge,
            "next_cycle_mrr": round(new_plan_mrr, 2)
        }
