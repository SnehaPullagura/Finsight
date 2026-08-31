from typing import Any, Dict, List, Optional

class ExpansionCadenceEngine:
    @staticmethod
    def schedule_expansion_cadence(account: Dict[str, Any]) -> Dict[str, Any]:
        cname = account.get("name")
        health = int(account.get("health_score", 50))

        cadence = [
            {"day": "Day 1", "touchpoint": "CSM Executive Summary Email with Product Usage Metrics"},
            {"day": "Day 4", "touchpoint": "Invite Lead Architect to Feature Roadmap Preview"},
            {"day": "Day 8", "touchpoint": "Present Co-Termed Volume Discount Expansion Proposal"}
        ]

        return {
            "account_name": cname,
            "health_score": health,
            "recommended_cadence_steps": cadence,
            "cadence_status": "CADENCE_INITIALIZED"
        }
