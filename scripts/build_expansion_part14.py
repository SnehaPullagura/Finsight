import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/sales_compensation/commission_accelerator_engine.py
    write_file("backend/app/enterprise/sales_compensation/commission_accelerator_engine.py", """from typing import Any, Dict, List, Optional

class CommissionAcceleratorEngine:
    @staticmethod
    def calculate_progressive_commission(
        quota: float,
        actual_revenue: float,
        base_rate: float = 0.10
    ) -> Dict[str, Any]:
        attainment_pct = (actual_revenue / max(1.0, quota)) * 100.0

        # Tier 1: 0 - 100% (1.0x accelerator)
        tier1_rev = min(actual_revenue, quota)
        tier1_payout = tier1_rev * base_rate * 1.0

        # Tier 2: 100% - 125% (1.5x accelerator)
        tier2_rev = max(0.0, min(actual_revenue - quota, quota * 0.25))
        tier2_payout = tier2_rev * base_rate * 1.5

        # Tier 3: 125%+ (2.0x accelerator)
        tier3_rev = max(0.0, actual_revenue - (quota * 1.25))
        tier3_payout = tier3_rev * base_rate * 2.0

        total_commission = tier1_payout + tier2_payout + tier3_payout
        effective_rate = (total_commission / max(1.0, actual_revenue)) * 100.0

        return {
            "quota": quota,
            "actual_revenue": actual_revenue,
            "attainment_percentage": round(attainment_pct, 2),
            "tier1_payout": round(tier1_payout, 2),
            "tier2_payout": round(tier2_payout, 2),
            "tier3_payout": round(tier3_payout, 2),
            "total_commission_earned": round(total_commission, 2),
            "effective_commission_rate_pct": round(effective_rate, 2),
            "is_accelerator_unlocked": attainment_pct > 100.0
        }
""")

    # 2. backend/app/enterprise/sales_compensation/clawback_policy_handler.py
    write_file("backend/app/enterprise/sales_compensation/clawback_policy_handler.py", """from datetime import date
from typing import Any, Dict, List, Optional

class ClawbackPolicyHandler:
    @staticmethod
    def evaluate_churn_clawback(
        subscription_start_date: date,
        churn_date: date,
        paid_commission_amount: float,
        clawback_window_days: int = 180
    ) -> Dict[str, Any]:
        days_active = max(0, (churn_date - subscription_start_date).days)
        is_clawback_triggered = days_active < clawback_window_days

        if not is_clawback_triggered:
            return {
                "days_active": days_active,
                "is_clawback_triggered": False,
                "clawback_amount": 0.0,
                "reason": "Customer remained active past 180-day clawback protection window"
            }

        # Prorate clawback based on remaining unfulfilled window
        unfulfilled_fraction = (clawback_window_days - days_active) / float(clawback_window_days)
        clawback_amount = round(paid_commission_amount * unfulfilled_fraction, 2)

        return {
            "days_active": days_active,
            "is_clawback_triggered": True,
            "paid_commission": paid_commission_amount,
            "clawback_amount": clawback_amount,
            "clawback_percentage": round(unfulfilled_fraction * 100, 1),
            "reason": f"Customer churned after only {days_active} days (inside {clawback_window_days}-day window)"
        }
""")

    # 3. backend/app/enterprise/ai_copilot/sentiment_analysis_engine.py
    write_file("backend/app/enterprise/ai_copilot/sentiment_analysis_engine.py", """import re
from typing import Any, Dict, List, Optional

class RuleBasedSentimentEngine:
    POSITIVE_WORDS = {
        "love", "excellent", "great", "awesome", "perfect", "fantastic", "amazing",
        "excited", "pleased", "impressed", "approve", "agree", "proceed", "ready",
        "valuable", "seamless", "fast", "efficient", "stellar", "recommend"
    }

    NEGATIVE_WORDS = {
        "budget", "freeze", "delay", "cancel", "frustrated", "slow", "broken",
        "issue", "bug", "terrible", "bad", "expensive", "competitor", "stalled",
        "blocker", "risk", "unhappy", "difficult", "complain", "fail"
    }

    @staticmethod
    def analyze_communication_sentiment(text: str) -> Dict[str, Any]:
        tokens = re.findall(r"\b[a-zA-Z]+\b", text.lower())
        if not tokens:
            return {"sentiment": "neutral", "score": 0.0, "positive_count": 0, "negative_count": 0}

        pos_count = sum(1 for t in tokens if t in RuleBasedSentimentEngine.POSITIVE_WORDS)
        neg_count = sum(1 for t in tokens if t in RuleBasedSentimentEngine.NEGATIVE_WORDS)

        total_emotional = pos_count + neg_count
        if total_emotional == 0:
            score = 0.0
            sentiment = "neutral"
        else:
            score = round((pos_count - neg_count) / float(total_emotional), 2)
            sentiment = "positive" if score > 0.2 else "negative" if score < -0.2 else "neutral"

        return {
            "sentiment": sentiment,
            "score": score,
            "positive_count": pos_count,
            "negative_count": neg_count,
            "total_words_analyzed": len(tokens)
        }
""")

    # 4. backend/app/enterprise/ai_copilot/intent_classification_engine.py
    write_file("backend/app/enterprise/ai_copilot/intent_classification_engine.py", """import re
from typing import Any, Dict, List, Optional

class IntentClassificationEngine:
    INTENT_RULES = {
        "pricing_inquiry": [r"\b(price|pricing|cost|quote|discount|rates|fee)\b"],
        "meeting_request": [r"\b(schedule|meet|call|demo|calendar|zoom|talk|connect)\b"],
        "technical_support": [r"\b(error|bug|issue|broken|help|api|failure|down)\b"],
        "contract_procurement": [r"\b(contract|nda|terms|msa|legal|signature|dpa|sign)\b"],
        "cancellation_risk": [r"\b(cancel|unsubscribe|churn|terminate|refund|stop)\b"]
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
""")

    print("Created commission accelerator, clawback handler, sentiment engine, and intent classifier.")

if __name__ == '__main__':
    run()
