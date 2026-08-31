from typing import Any, Dict, List, Optional

class CustomerSuccessLifecycleEngine:
    @staticmethod
    def evaluate_renewal_risk(
        health_score: int,
        days_until_renewal: int,
        unresolved_tickets: int,
        contract_value: float
    ) -> Dict[str, Any]:
        risk_factors = []
        score = health_score

        if days_until_renewal <= 60 and health_score < 70:
            risk_factors.append("Upcoming renewal within 60 days with sub-70 health score")
        if unresolved_tickets >= 3:
            risk_factors.append(f"{unresolved_tickets} unresolved support tickets")
        if health_score < 50:
            risk_factors.append("Critical low product usage engagement")

        risk_category = "high_risk" if len(risk_factors) >= 2 or health_score < 40 else "medium_risk" if risk_factors else "healthy"

        return {
            "contract_value": contract_value,
            "days_until_renewal": days_until_renewal,
            "health_score": health_score,
            "renewal_risk_category": risk_category,
            "risk_factors": risk_factors,
            "requires_executive_sponsor": risk_category == "high_risk"
        }
