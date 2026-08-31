from typing import Any, Dict, List, Optional

class CACPaybackModeler:
    @staticmethod
    def calculate_payback_months(
        customer_acquisition_cost: float,
        monthly_arpu: float,
        gross_margin_percentage: float
    ) -> Dict[str, Any]:
        margin_decimal = gross_margin_percentage / 100.0
        monthly_gross_profit = monthly_arpu * margin_decimal

        if monthly_gross_profit <= 0:
            return {"payback_months": 999.0, "status": "unprofitable"}

        payback_months = round(customer_acquisition_cost / monthly_gross_profit, 1)

        return {
            "customer_acquisition_cost": customer_acquisition_cost,
            "monthly_arpu": monthly_arpu,
            "gross_margin_percentage": gross_margin_percentage,
            "monthly_gross_profit_per_customer": round(monthly_gross_profit, 2),
            "payback_period_months": payback_months,
            "capital_efficiency_grade": "Top Decile (< 12 Mo)" if payback_months <= 12.0 else "Healthy (12-18 Mo)" if payback_months <= 18.0 else "High Burn (> 18 Mo)"
        }
