from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

class EnterpriseSLAMatrix:
    TIER_TARGETS = {
        "platinum": {"first_response_min": 15, "resolution_hours": 2},
        "gold": {"first_response_min": 60, "resolution_hours": 8},
        "silver": {"first_response_min": 240, "resolution_hours": 24},
        "standard": {"first_response_min": 480, "resolution_hours": 48}
    }

    @staticmethod
    def calculate_sla_deadlines(tier: str, priority: str, created_at: datetime) -> Dict[str, Any]:
        targets = EnterpriseSLAMatrix.TIER_TARGETS.get(tier.lower(), EnterpriseSLAMatrix.TIER_TARGETS["standard"])
        
        # Priority multiplier
        multiplier = 0.5 if priority.lower() == "critical" else 0.75 if priority.lower() == "high" else 1.0

        resp_minutes = int(targets["first_response_min"] * multiplier)
        res_hours = targets["resolution_hours"] * multiplier

        resp_deadline = created_at + timedelta(minutes=resp_minutes)
        res_deadline = created_at + timedelta(hours=res_hours)

        return {
            "tier": tier,
            "priority": priority,
            "response_deadline": resp_deadline.isoformat(),
            "resolution_deadline": res_deadline.isoformat(),
            "target_response_minutes": resp_minutes,
            "target_resolution_hours": round(res_hours, 1)
        }
