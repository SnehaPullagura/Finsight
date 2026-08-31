from typing import Any, Dict, List, Optional

class CSChurnInterceptorEngine:
    @staticmethod
    def generate_instant_interception_payload(account: Dict[str, Any]) -> Dict[str, Any]:
        cname = account.get("name")
        health = int(account.get("health_score", 50))
        arr = account.get("current_arr", "$50,000")

        return {
            "account_id": account.get("id"),
            "account_name": cname,
            "current_health": health,
            "at_risk_arr": arr,
            "prescribed_interception_actions": [
                "Deploy proactive CS engineering hotline",
                "Execute complimentary feature optimization audit",
                "Lock in 1-year price freeze upon early renewal execution"
            ],
            "interception_status": "INTERVENTION_DEPLOYED"
        }
