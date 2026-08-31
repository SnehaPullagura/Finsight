from datetime import date
from typing import Any, Dict, List, Optional

class PipelineInactivityWatchdog:
    @staticmethod
    def identify_stagnant_deals(deals: List[Dict[str, Any]], max_allowed_inactivity_days: int = 14) -> List[Dict[str, Any]]:
        stagnant = []
        for d in deals:
            dname = d.get("name")
            val = float(d.get("value", 0.0))
            inactive_days = int(d.get("days_since_last_activity", 0))

            if inactive_days >= max_allowed_inactivity_days:
                stagnant.append({
                    "deal_name": dname,
                    "deal_value": val,
                    "days_inactive": inactive_days,
                    "rep_owner": d.get("owner_name", "Unassigned"),
                    "recommended_action": "DISPATCH_REENGAGEMENT_PLAYBOOK",
                    "severity": "CRITICAL" if inactive_days >= 30 else "WARNING"
                })

        return sorted(stagnant, key=lambda x: x["days_inactive"], reverse=True)
