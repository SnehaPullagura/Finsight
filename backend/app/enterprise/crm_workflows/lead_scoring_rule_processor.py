from typing import Any, Dict, List, Optional

class EnterpriseLeadScoringRuleProcessor:
    @staticmethod
    def evaluate_firmographic_fit(lead_record: Dict[str, Any]) -> Dict[str, Any]:
        score = 0
        reasons = []

        employees = int(lead_record.get("employee_count", 0))
        if employees >= 1000:
            score += 35
            reasons.append("Enterprise Tier 1: 1,000+ employees (+35 pts)")
        elif employees >= 250:
            score += 20
            reasons.append("Mid-Market Tier 2: 250-999 employees (+20 pts)")

        revenue = float(lead_record.get("annual_revenue", 0.0))
        if revenue >= 50000000.0:
            score += 35
            reasons.append("High ARR Company: $50M+ annual revenue (+35 pts)")
        elif revenue >= 10000000.0:
            score += 20
            reasons.append("Mid ARR Company: $10M-$50M annual revenue (+20 pts)")

        country = (lead_record.get("country") or "").upper()
        if country in ["US", "CA", "GB", "DE", "FR", "AU", "SG"]:
            score += 30
            reasons.append(f"Strategic Tier 1 Territory: {country} (+30 pts)")

        final_score = max(0, min(100, score))
        grade = "A" if final_score >= 80 else "B" if final_score >= 60 else "C" if final_score >= 40 else "D"

        return {
            "firmographic_score": final_score,
            "grade": grade,
            "is_sales_qualified": final_score >= 70,
            "scoring_reasons": reasons
        }
