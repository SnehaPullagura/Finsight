from typing import Any, Dict, List, Optional

class CustomerLifetimeValueModel:
    @staticmethod
    def calculate_ltv_projection(
        average_mrr: float,
        gross_margin_percentage: float,
        monthly_churn_rate_pct: float,
        discount_rate_annual_pct: float = 8.0
    ) -> Dict[str, Any]:
        margin_decimal = gross_margin_percentage / 100.0
        monthly_churn_decimal = max(0.001, monthly_churn_rate_pct / 100.0)
        
        # Monthly Discount Rate
        monthly_discount_rate = (1.0 + (discount_rate_annual_pct / 100.0)) ** (1.0 / 12.0) - 1.0

        # LTV Formula: (ARPU * Gross Margin) / (Monthly Churn + Monthly Discount Rate)
        average_lifespan_months = round(1.0 / monthly_churn_decimal, 1)
        discounted_ltv = round((average_mrr * margin_decimal) / (monthly_churn_decimal + monthly_discount_rate), 2)
        simple_ltv = round((average_mrr * margin_decimal) / monthly_churn_decimal, 2)

        return {
            "average_monthly_revenue": average_mrr,
            "gross_margin_pct": gross_margin_percentage,
            "monthly_churn_rate_pct": monthly_churn_rate_pct,
            "average_lifespan_months": average_lifespan_months,
            "simple_ltv": simple_ltv,
            "discounted_ltv": discounted_ltv,
            "annualized_arr_per_customer": round(average_mrr * 12.0, 2)
        }
