import re
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
        tokens = re.findall(r"[a-zA-Z]+", text.lower())
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
