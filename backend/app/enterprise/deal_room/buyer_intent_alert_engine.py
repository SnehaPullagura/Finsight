from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class BuyerIntentAlertEngine:
    """
    Dispatches Slack and webhook notifications when an economic buyer views the pricing table or forwards the proposal.
    """
    @staticmethod
    def evaluate_intent_trigger(
        visitor_email: str,
        page_viewed: str,
        dwell_seconds: int
    ) -> Dict[str, Any]:
        is_pricing = "pricing" in page_viewed.lower() or "quote" in page_viewed.lower()
        is_high_intent = is_pricing and dwell_seconds >= 60

        return {
            "visitor_email": visitor_email,
            "page_viewed": page_viewed,
            "dwell_seconds": dwell_seconds,
            "is_high_intent_event": is_high_intent,
            "alert_priority": "P1_INSTANT_REP_NOTIFICATION" if is_high_intent else "P3_PASSIVE_LOG",
            "recommended_sales_action": "Call/Email buyer immediately while proposal is open." if is_high_intent else "None",
            "triggered_at": datetime.now(timezone.utc).isoformat()
        }
