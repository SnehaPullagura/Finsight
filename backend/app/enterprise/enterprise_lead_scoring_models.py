from typing import Any, Dict, List, Optional

class EnterpriseLeadScoringModel:
    FIT_WEIGHTS = {
        "industry_tier_1": 30, # Software, FinTech, HealthTech
        "industry_tier_2": 20, # Manufacturing, Retail, Professional Services
        "company_size_enterprise": 30, # 1,000+ employees
        "company_size_midmarket": 20,  # 100-999 employees
        "annual_revenue_50m_plus": 25,
        "annual_revenue_10m_plus": 15,
        "target_country_tier_1": 15 # US, UK, CA, DE, FR, AU, SG
    }

    INTENT_WEIGHTS = {
        "pricing_page_visited": 25,
        "security_whitepaper_downloaded": 20,
        "demo_requested": 40,
        "webinar_attended": 15,
        "multiple_stakeholder_visits": 20
    }

    @staticmethod
    def calculate_composite_score(
        fit_signals: List[str],
        intent_signals: List[str],
        decay_factor: float = 1.0
    ) -> Dict[str, Any]:
        fit_score = sum(EnterpriseLeadScoringModel.FIT_WEIGHTS.get(s, 0) for s in fit_signals)
        intent_score = sum(EnterpriseLeadScoringModel.INTENT_WEIGHTS.get(s, 0) for s in intent_signals) * decay_factor

        total_raw = (fit_score * 0.50) + (intent_score * 0.50)
        final_score = max(0, min(100, int(total_raw)))

        grade = "A" if final_score >= 80 else "B" if final_score >= 65 else "C" if final_score >= 45 else "D"

        return {
            "fit_score": fit_score,
            "intent_score": round(intent_score, 1),
            "final_lead_score": final_score,
            "qualification_grade": grade,
            "is_mql": final_score >= 65,
            "is_sql_ready": final_score >= 80
        }
