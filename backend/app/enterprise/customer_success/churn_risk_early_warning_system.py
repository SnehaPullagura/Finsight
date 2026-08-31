from datetime import date
from typing import Any, Dict, List, Optional

class ChurnRiskEarlyWarningSystem:
    @staticmethod
    def evaluate_account_risk_signals(account: Dict[str, Any]) -> Dict[str, Any]:
        risk_score = 0
        signals = []

        dau_drop = float(account.get("dau_drop_pct_30d", 0.0))
        if dau_drop >= 30.0:
            risk_score += 40
            signals.append(f"Product active usage dropped {dau_drop}% in last 30 days")

        nps = int(account.get("latest_nps_score", 8))
        if nps <= 6:
            risk_score += 30
            signals.append(f"Detractor NPS survey response ({nps}/10)")

        overdue_days = int(account.get("invoice_days_overdue", 0))
        if overdue_days > 14:
            risk_score += 25
            signals.append(f"Billing invoice overdue by {overdue_days} days")

        tier = "Critical Churn Risk" if risk_score >= 60 else "Elevated Risk" if risk_score >= 30 else "Healthy"

        return {
            "account_id": account.get("id"),
            "account_name": account.get("name"),
            "churn_risk_score": min(100, risk_score),
            "risk_tier": tier,
            "risk_signals": signals,
            "is_intervention_required": risk_score >= 30
        }
