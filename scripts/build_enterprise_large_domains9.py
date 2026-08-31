import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/revenue_recognition_engine.py
    write_file("backend/app/enterprise/revenue_recognition_engine.py", """from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class ASC606RevenueRecognitionEngine:
    @staticmethod
    def generate_amortization_schedule(
        contract_id: str,
        total_contract_value: float,
        start_date: date,
        term_months: int
    ) -> List[Dict[str, Any]]:
        monthly_recognized = round(total_contract_value / float(term_months), 2)
        schedule = []
        cumulative_recognized = 0.0

        for month_idx in range(1, term_months + 1):
            # Last month adjusts rounding difference
            if month_idx == term_months:
                amount = round(total_contract_value - cumulative_recognized, 2)
            else:
                amount = monthly_recognized

            cumulative_recognized += amount
            deferred_remaining = max(0.0, round(total_contract_value - cumulative_recognized, 2))
            
            period_date = start_date + timedelta(days=30 * (month_idx - 1))

            schedule.append({
                "period_number": month_idx,
                "recognition_date": period_date.isoformat(),
                "recognized_amount": amount,
                "cumulative_recognized": round(cumulative_recognized, 2),
                "deferred_revenue_balance": deferred_remaining,
                "compliance_standard": "ASC 606 / IFRS 15"
            })

        return schedule
""")

    # 2. backend/app/enterprise/dynamic_tax_engine.py
    write_file("backend/app/enterprise/dynamic_tax_engine.py", """from typing import Any, Dict, List, Optional

class DynamicTaxEngine:
    JURISDICTION_RATES = {
        "US_CA": 0.0825,
        "US_NY": 0.08875,
        "US_TX": 0.0825,
        "US_WA": 0.0650,
        "GB": 0.20,     # UK VAT
        "DE": 0.19,     # German VAT
        "FR": 0.20,     # French VAT
        "IN": 0.18,     # India GST
        "SG": 0.09      # Singapore GST
    }

    @staticmethod
    def calculate_taxes(
        subtotal: float,
        country: str,
        state: Optional[str] = None,
        is_tax_exempt: bool = False
    ) -> Dict[str, Any]:
        if is_tax_exempt or subtotal <= 0:
            return {"tax_rate_pct": 0.0, "tax_amount": 0.0, "total_with_tax": subtotal, "is_tax_exempt": True}

        code = f"{country.upper()}_{state.upper()}" if state else country.upper()
        rate = DynamicTaxEngine.JURISDICTION_RATES.get(code, DynamicTaxEngine.JURISDICTION_RATES.get(country.upper(), 0.0))

        tax_amount = round(subtotal * rate, 2)
        total_amount = round(subtotal + tax_amount, 2)

        return {
            "jurisdiction": code,
            "tax_rate_pct": round(rate * 100.0, 2),
            "tax_amount": tax_amount,
            "subtotal": round(subtotal, 2),
            "total_with_tax": total_amount,
            "is_tax_exempt": False
        }
""")

    # 3. backend/app/enterprise/predictive_lead_scorer.py
    write_file("backend/app/enterprise/predictive_lead_scorer.py", """import math
from typing import Any, Dict, List, Optional

class PredictiveLeadScorer:
    @staticmethod
    def score_lead(lead_profile: Dict[str, Any]) -> Dict[str, Any]:
        score = 20 # Baseline

        # Industry affinity
        industry = (lead_profile.get("industry") or "").lower()
        if industry in ["technology", "finance", "healthcare"]:
            score += 25
        elif industry in ["manufacturing", "retail"]:
            score += 15

        # Employee count
        employees = int(lead_profile.get("employee_count", 0))
        if employees >= 1000:
            score += 25
        elif employees >= 100:
            score += 15
        elif employees >= 20:
            score += 10

        # Budget estimate
        budget = float(lead_profile.get("estimated_budget", 0.0))
        if budget >= 100000:
            score += 20
        elif budget >= 25000:
            score += 10

        # Engagement signals
        views = int(lead_profile.get("page_views", 0))
        score += min(15, views * 2)

        final_score = max(0, min(100, score))
        grade = "A" if final_score >= 80 else "B" if final_score >= 60 else "C" if final_score >= 40 else "D"
        conversion_prob = round(1.0 / (1.0 + math.exp(-((final_score - 50) / 15.0))), 3)

        return {
            "lead_score": final_score,
            "qualification_grade": grade,
            "conversion_probability": conversion_prob,
            "is_sales_ready": final_score >= 70
        }
""")

    print("Created revenue recognition, tax engine, and predictive lead scorer.")

if __name__ == '__main__':
    run()
