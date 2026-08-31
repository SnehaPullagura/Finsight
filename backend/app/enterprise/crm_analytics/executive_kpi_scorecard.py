from typing import Any, Dict, List, Optional

class ExecutiveKPIScorecard:
    @staticmethod
    def calculate_saas_metrics(
        starting_arr: float,
        ending_arr: float,
        free_cash_flow_margin_pct: float,
        sales_and_marketing_spend: float,
        net_new_arr_added: float,
        average_customer_cac: float,
        average_customer_ltv: float
    ) -> Dict[str, Any]:
        arr_growth_pct = round(((ending_arr - starting_arr) / max(1.0, starting_arr)) * 100.0, 1)
        
        # Rule of 40: Growth Rate % + Free Cash Flow Margin %
        rule_of_40_score = round(arr_growth_pct + free_cash_flow_margin_pct, 1)

        # SaaS Magic Number: Net New ARR / S&M Spend
        magic_number = round(net_new_arr_added / max(1.0, sales_and_marketing_spend), 2)

        # LTV to CAC Ratio
        ltv_cac_ratio = round(average_customer_ltv / max(1.0, average_customer_cac), 2)

        return {
            "arr_growth_percentage": arr_growth_pct,
            "free_cash_flow_margin": free_cash_flow_margin_pct,
            "rule_of_40_score": rule_of_40_score,
            "is_rule_of_40_achieved": rule_of_40_score >= 40.0,
            "magic_number": magic_number,
            "magic_number_health": "Top Tier" if magic_number >= 1.0 else "Good" if magic_number >= 0.75 else "Needs Efficiency",
            "ltv_to_cac_ratio": ltv_cac_ratio,
            "benchmark_status": "World Class SaaS" if rule_of_40_score >= 40.0 and ltv_cac_ratio >= 3.0 else "Healthy Growth"
        }
