from typing import Any, Dict, List, Optional

class SupportTicketRouter:
    CATEGORY_SKILL_MAP = {
        "billing": ["Finance", "Billing Specialist"],
        "technical": ["Tier 2 Support", "DevOps", "Integration Engineer"],
        "security": ["Security Team", "Compliance Officer"],
        "general": ["Tier 1 Support", "Customer Success"]
    }

    @staticmethod
    def calculate_priority_score(
        category: str,
        customer_tier: str, # enterprise, growth, starter
        sentiment_score: float, # -1.0 to 1.0
        is_sla_breached: bool = False
    ) -> str:
        score = 0
        
        # Customer tier weighting
        if customer_tier.lower() == "enterprise":
            score += 40
        elif customer_tier.lower() == "growth":
            score += 20

        # Category weighting
        if category.lower() == "security":
            score += 40
        elif category.lower() == "billing":
            score += 25
        elif category.lower() == "technical":
            score += 20

        # Sentiment factor
        if sentiment_score < -0.5:
            score += 20

        if is_sla_breached:
            score += 30

        if score >= 70:
            return "critical"
        elif score >= 45:
            return "high"
        elif score >= 25:
            return "medium"
        return "low"
