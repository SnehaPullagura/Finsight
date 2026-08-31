from typing import Any, Dict, List, Optional

class DealSlippageProbabilityScorer:
    """
    Machine learning heuristic estimating the probability of an opportunity slipping past the quarter close date.
    """
    @staticmethod
    def score_slippage_risk(deal: Dict[str, Any]) -> Dict[str, Any]:
        dname = deal.get("name")
        days_in_stage = int(deal.get("days_in_current_stage", 10))
        push_count = int(deal.get("close_date_push_count", 0))
        has_economic_buyer = bool(deal.get("has_economic_buyer_engaged", True))

        risk = 10
        if days_in_stage >= 30:
            risk += 35
        if push_count >= 2:
            risk += 30
        if not has_economic_buyer:
            risk += 25

        final_risk = min(100, risk)

        return {
            "deal_name": dname,
            "slippage_risk_score": final_risk,
            "risk_tier": "CRITICAL_SLIPPAGE_RISK" if final_risk >= 70 else "MODERATE_RISK" if final_risk >= 40 else "LOW_RISK_ON_TRACK",
            "is_slippage_forecasted": final_risk >= 50
        }
