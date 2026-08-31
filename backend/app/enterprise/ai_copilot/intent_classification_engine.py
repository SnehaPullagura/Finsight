import re
from typing import Any, Dict, List, Optional

class IntentClassificationEngine:
    INTENT_RULES = {
        "pricing_inquiry": [r"(price|pricing|cost|quote|discount|rates|fee)"],
        "meeting_request": [r"(schedule|meet|call|demo|calendar|zoom|talk|connect)"],
        "technical_support": [r"(error|bug|issue|broken|help|api|failure|down)"],
        "contract_procurement": [r"(contract|nda|terms|msa|legal|signature|dpa|sign)"],
        "cancellation_risk": [r"(cancel|unsubscribe|churn|terminate|refund|stop)"]
    }

    @staticmethod
    def classify_customer_intent(message_body: str) -> Dict[str, Any]:
        detected_intents = []
        body_lower = message_body.lower()

        for intent_name, patterns in IntentClassificationEngine.INTENT_RULES.items():
            for pat in patterns:
                if re.search(pat, body_lower):
                    detected_intents.append(intent_name)
                    break

        primary_intent = detected_intents[0] if detected_intents else "general_inquiry"

        return {
            "primary_intent": primary_intent,
            "all_detected_intents": detected_intents,
            "urgency": "urgent" if primary_intent in ["cancellation_risk", "technical_support"] else "normal"
        }
