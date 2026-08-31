from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class CreativeFatigueAlertQueue:
    @staticmethod
    def queue_fatigued_creatives(fatigued_ads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        alerts = []
        for ad in fatigued_ads:
            alerts.append({
                "alert_id": f"cfa_{int(datetime.now(timezone.utc).timestamp() * 1000)}",
                "creative_id": ad.get("id"),
                "creative_title": ad.get("title"),
                "current_cpa": ad.get("cpa"),
                "cpa_inflation_pct": ad.get("cpa_inflation_pct"),
                "dispatched_at": datetime.now(timezone.utc).isoformat(),
                "action_status": "AUTO_PAUSED_AND_REPLACED"
            })
        return alerts
