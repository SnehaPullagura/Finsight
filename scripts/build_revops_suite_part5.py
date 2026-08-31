import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/sales_enablement/call_transcript_topic_extractor.py
    write_file("backend/app/enterprise/sales_enablement/call_transcript_topic_extractor.py", """import re
from typing import Any, Dict, List, Optional

class CallTranscriptTopicExtractor:
    \"\"\"
    Conversation Intelligence & Topic Modeling:
    Parses call audio transcripts for pricing questions, security concerns, competitor mentions,
    and decision timeline commitments.
    \"\"\"
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
            matches = sum(len(re.findall(r"\\b" + re.escape(kw) + r"\\b", text_lower)) for kw in keywords)
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
""")

    # 2. backend/app/enterprise/sales_enablement/talk_to_listen_ratio_analyzer.py
    write_file("backend/app/enterprise/sales_enablement/talk_to_listen_ratio_analyzer.py", """from typing import Any, Dict, List, Optional

class TalkToListenRatioAnalyzer:
    \"\"\"
    Analyzes rep speech cadence:
    Optimal discovery call benchmark is 45% Rep Talk / 55% Customer Listen.
    \"\"\"
    @staticmethod
    def calculate_cadence(
        rep_speaking_seconds: float,
        customer_speaking_seconds: float,
        silence_seconds: float = 0.0
    ) -> Dict[str, Any]:
        total_time = rep_speaking_seconds + customer_speaking_seconds + silence_seconds
        rep_ratio = round((rep_speaking_seconds / max(1.0, total_time)) * 100.0, 1)
        cust_ratio = round((customer_speaking_seconds / max(1.0, total_time)) * 100.0, 1)

        if rep_ratio <= 48.0:
            rating = "EXCELLENT_ACTIVE_LISTENING"
            coaching = "Superb active listening and question prompting."
        elif rep_ratio <= 60.0:
            rating = "BALANCED_ENGAGEMENT"
            coaching = "Solid conversational exchange; consider leaving more space after questions."
        else:
            rating = "OVER_TALKING_MONOLOGUE"
            coaching = "Rep spoke for majority of call; practice open-ended discovery probing."

        return {
            "rep_talk_percentage": rep_ratio,
            "customer_talk_percentage": cust_ratio,
            "total_call_duration_seconds": total_time,
            "cadence_rating": rating,
            "coaching_feedback": coaching
        }
""")

    # 3. backend/app/enterprise/sales_enablement/rep_coaching_card_generator.py
    write_file("backend/app/enterprise/sales_enablement/rep_coaching_card_generator.py", """from typing import Any, Dict, List, Optional

class RepCoachingCardGenerator:
    \"\"\"
    Synthesizes multi-call data into automated weekly rep coaching cards.
    \"\"\"
    @staticmethod
    def generate_coaching_card(
        rep_name: str,
        calls_analyzed: int,
        avg_talk_ratio: float,
        objection_resolution_rate_pct: float,
        next_steps_secured_pct: float
    ) -> Dict[str, Any]:
        strengths = []
        areas_for_growth = []

        if avg_talk_ratio <= 50.0:
            strengths.append("Exceptional active listening and discovery questioning.")
        else:
            areas_for_growth.append("Reduce talk time below 50% on initial discovery calls.")

        if objection_resolution_rate_pct >= 75.0:
            strengths.append("High-confidence handling of competitive pricing pushback.")
        else:
            areas_for_growth.append("Leverage ROI Battlecard when responding to budget constraints.")

        if next_steps_secured_pct >= 85.0:
            strengths.append("Consistent closing of calendar commitments on every call.")
        else:
            areas_for_growth.append("Reserve 5 minutes at end of call to schedule technical demo.")

        overall_grade = "A" if len(strengths) >= 2 and len(areas_for_growth) <= 1 else "B" if len(strengths) >= 1 else "C"

        return {
            "rep_name": rep_name,
            "calls_analyzed_count": calls_analyzed,
            "coaching_grade": overall_grade,
            "key_strengths": strengths,
            "prescribed_micro_learning": areas_for_growth,
            "recommended_curriculum_module": "Advanced Discovery & Executive Storytelling Masterclass"
        }
""")

    print("Sales enablement suite created successfully.")

if __name__ == "__main__":
    run()
