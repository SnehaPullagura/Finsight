import re
from typing import Any, Dict, List, Optional

class CallTranscriptTopicExtractor:
    """
    Conversation Intelligence & Topic Modeling:
    Parses call audio transcripts for pricing questions, security concerns, competitor mentions,
    and decision timeline commitments.
    """
    TOPIC_KEYWORDS = {
        "pricing_and_budget": ["discount", "pricing", "budget", "quote", "cost", "expensive", "per seat"],
        "security_and_compliance": ["soc2", "gdpr", "hipaa", "encryption", "sso", "saml", "penetration test"],
        "competitor_intelligence": ["salesforce", "hubspot", "microsoft dynamics", "pipedrive", "zoho"],
        "decision_process": ["economic buyer", "procurement", "legal review", "board approval", "go-live date"]
    }

    @classmethod
    def extract_topics_and_sentiment(cls, transcript_text: str) -> Dict[str, Any]:
        text_lower = transcript_text.lower()
        topic_counts = {}

        for topic, keywords in cls.TOPIC_KEYWORDS.items():
            matches = sum(len(re.findall(r"\b" + re.escape(kw) + r"\b", text_lower)) for kw in keywords)
            topic_counts[topic] = matches

        total_words = len(transcript_text.split())
        question_count = transcript_text.count("?")

        return {
            "total_word_count": total_words,
            "questions_asked_count": question_count,
            "topic_mention_frequencies": topic_counts,
            "primary_conversation_theme": max(topic_counts, key=topic_counts.get) if any(topic_counts.values()) else "general_discovery",
            "security_clearance_required": topic_counts.get("security_and_compliance", 0) >= 2,
            "pricing_objections_raised": topic_counts.get("pricing_and_budget", 0) >= 3
        }
