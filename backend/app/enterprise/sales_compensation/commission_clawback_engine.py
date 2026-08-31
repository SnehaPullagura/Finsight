from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class CommissionClawbackEngine:
    """
    Audits early contract cancellations and computes commission clawbacks:
    - 0-90 Days: 100% Commission Clawback
    - 91-180 Days: 50% Commission Clawback
    - 181+ Days: 0% Clawback (Standard Retention Risk)
    """
    @staticmethod
    def evaluate_deal_churn_clawback(
        deal_id: str,
        rep_name: str,
        commission_paid: float,
        days_active_before_cancel: int
    ) -> Dict[str, Any]:
        if days_active_before_cancel <= 90:
            clawback_pct = 100.0
        elif days_active_before_cancel <= 180:
            clawback_pct = 50.0
        else:
            clawback_pct = 0.0

        clawback_amount = round(commission_paid * (clawback_pct / 100.0), 2)
        net_retained = round(commission_paid - clawback_amount, 2)

        return {
            "deal_id": deal_id,
            "rep_name": rep_name,
            "original_commission_paid": commission_paid,
            "days_active_before_cancel": days_active_before_cancel,
            "clawback_percentage": clawback_pct,
            "clawback_amount_due": clawback_amount,
            "net_commission_retained": net_retained,
            "clawback_policy_tier": "FULL_CLAWBACK_90D" if clawback_pct == 100.0 else "PARTIAL_CLAWBACK_180D" if clawback_pct == 50.0 else "ZERO_CLAWBACK_SAFE",
            "evaluated_at": datetime.now(timezone.utc).isoformat()
        }
