from typing import Any, Dict, List, Optional

class PredictiveRenewalRiskModeler:
    @staticmethod
    def predict_contract_renewal(account: Dict[str, Any], days_until_renewal: int) -> Dict[str, Any]:
        health_score = int(account.get("health_score", 50))
        nps = int(account.get("nps", 8))
        sponsor_active = bool(account.get("is_executive_sponsor_engaged", True))

        # Base renewal probability from health score
        base_prob = health_score * 0.7 + (nps * 3.0)
        if not sponsor_active:
            base_prob -= 25.0

        renewal_probability = min(100.0, max(5.0, round(base_prob, 1)))

        risk_category = "High Renewal Risk" if renewal_probability < 50.0 else "Moderate Risk" if renewal_probability < 75.0 else "Safe On-Track Renewal"

        return {
            "account_id": account.get("id"),
            "account_name": account.get("name"),
            "contract_arr": account.get("current_arr"),
            "days_until_renewal": days_until_renewal,
            "health_score": health_score,
            "renewal_probability_percentage": renewal_probability,
            "risk_category": risk_category,
            "action_required": "SCHEDULE_EXECUTIVE_ALIGNMENT" if renewal_probability < 75.0 else "STANDARD_RENEWAL_CADENCE"
        }
