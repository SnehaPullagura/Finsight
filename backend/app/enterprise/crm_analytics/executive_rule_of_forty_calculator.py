from typing import Any, Dict, List, Optional

class RuleOfFortyCalculator:
    @staticmethod
    def calculate_efficiency_score(arr_growth_rate_pct: float, fcf_margin_pct: float) -> Dict[str, Any]:
        rule_of_40_score = round(arr_growth_rate_pct + fcf_margin_pct, 1)

        rating = "Elite Venture Grade (> 50%)" if rule_of_40_score >= 50.0 else "Top Quartile SaaS (40% - 50%)" if rule_of_40_score >= 40.0 else "Sub-Scale / Growth Needed (< 40%)"

        return {
            "arr_growth_rate_percentage": arr_growth_rate_pct,
            "free_cash_flow_margin_percentage": fcf_margin_pct,
            "rule_of_40_score": rule_of_40_score,
            "is_rule_of_40_passed": rule_of_40_score >= 40.0,
            "valuation_multiple_tier": rating
        }
