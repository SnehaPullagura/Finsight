from datetime import date
from typing import Any, Dict, List, Optional

class ClawbackPolicyHandler:
    @staticmethod
    def evaluate_churn_clawback(
        subscription_start_date: date,
        churn_date: date,
        paid_commission_amount: float,
        clawback_window_days: int = 180
    ) -> Dict[str, Any]:
        days_active = max(0, (churn_date - subscription_start_date).days)
        is_clawback_triggered = days_active < clawback_window_days

        if not is_clawback_triggered:
            return {
                "days_active": days_active,
                "is_clawback_triggered": False,
                "clawback_amount": 0.0,
                "reason": "Customer remained active past 180-day clawback protection window"
            }

        # Prorate clawback based on remaining unfulfilled window
        unfulfilled_fraction = (clawback_window_days - days_active) / float(clawback_window_days)
        clawback_amount = round(paid_commission_amount * unfulfilled_fraction, 2)

        return {
            "days_active": days_active,
            "is_clawback_triggered": True,
            "paid_commission": paid_commission_amount,
            "clawback_amount": clawback_amount,
            "clawback_percentage": round(unfulfilled_fraction * 100, 1),
            "reason": f"Customer churned after only {days_active} days (inside {clawback_window_days}-day window)"
        }
