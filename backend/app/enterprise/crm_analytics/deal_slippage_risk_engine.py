from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class DealSlippageRiskEngine:
    @staticmethod
    def evaluate_deal_close_date_risk(deal: Dict[str, Any], push_count: int, stage_days: int) -> Dict[str, Any]:
        close_date_str = deal.get("expected_close_date") or date.today().isoformat()
        close_date = date.fromisoformat(close_date_str)
        today = date.today()

        days_until_close = (close_date - today).days
        risk_score = 0
        risk_signals = []

        if days_until_close < 0:
            risk_score += 50
            risk_signals.append(f"Close date is {abs(days_until_close)} days in the past")
        elif days_until_close <= 5 and deal.get("stage") in ["Discovery", "Scoping"]:
            risk_score += 40
            risk_signals.append("Close date within 5 days but deal is in early stage")

        if push_count >= 3:
            risk_score += 30
            risk_signals.append(f"Close date has been pushed {push_count} times")
        elif push_count >= 1:
            risk_score += 15
            risk_signals.append(f"Close date has been pushed {push_count} time(s)")

        if stage_days > 21:
            risk_score += 20
            risk_signals.append(f"Deal stalled in current stage for {stage_days} days")

        final_risk = min(100, risk_score)
        tier = "Critical Slippage Risk" if final_risk >= 70 else "Elevated Risk" if final_risk >= 40 else "On Schedule"

        return {
            "deal_id": deal.get("id"),
            "deal_name": deal.get("name"),
            "expected_close_date": close_date.isoformat(),
            "slippage_risk_score": final_risk,
            "risk_tier": tier,
            "risk_signals": risk_signals,
            "push_count": push_count,
            "is_slippage_likely": final_risk >= 40
        }
