from typing import Any, Dict, List, Optional

class OmnichannelRoutingManager:
    @staticmethod
    def select_best_channel(contact_preferences: Dict[str, Any], message_urgency: str) -> str:
        if message_urgency.lower() == "critical":
            return "sms" if contact_preferences.get("phone") else "email"
        elif contact_preferences.get("prefers_slack"):
            return "slack"
        elif contact_preferences.get("prefers_whatsapp"):
            return "whatsapp"
        return "email"
