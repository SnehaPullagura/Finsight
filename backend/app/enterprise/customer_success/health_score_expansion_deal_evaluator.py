from typing import Any, Dict, List, Optional

class ExpansionDealHealthEvaluator:
    @staticmethod
    def evaluate_expansion_proposal_health(
        account: Dict[str, Any],
        proposed_discount_pct: float,
        term_months: int
    ) -> Dict[str, Any]:
        health = int(account.get("health_score", 50))
        nps = int(account.get("nps", 8))

        # Margin preservation score
        margin_score = max(0, 100 - int(proposed_discount_pct * 2.5))
        long_term_score = 100 if term_months >= 24 else 85 if term_months >= 12 else 50

        composite_viability = (health * 0.4) + (margin_score * 0.4) + (long_term_score * 0.2)
        score = min(100, int(composite_viability))

        return {
            "account_name": account.get("name"),
            "health_score": health,
            "proposed_discount_pct": proposed_discount_pct,
            "contract_term_months": term_months,
            "expansion_viability_score": score,
            "approval_recommendation": "AUTO_APPROVE" if score >= 80 and proposed_discount_pct <= 15.0 else "MANAGEMENT_SIGN_OFF_REQUIRED"
        }
