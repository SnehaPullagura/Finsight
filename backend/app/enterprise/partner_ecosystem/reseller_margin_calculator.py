from typing import Any, Dict, List, Optional

class ResellerMarginCalculator:
    """
    Computes Wholesale vs Suggested Retail Price (MSRP) margins for multi-tier distribution.
    """
    @staticmethod
    def calculate_reseller_quote(
        list_price: float,
        reseller_discount_pct: float,
        end_user_discount_pct: float = 0.0
    ) -> Dict[str, Any]:
        wholesale_cost = round(list_price * (1.0 - (reseller_discount_pct / 100.0)), 2)
        end_user_quote = round(list_price * (1.0 - (end_user_discount_pct / 100.0)), 2)
        reseller_gross_margin = round(end_user_quote - wholesale_cost, 2)
        reseller_margin_pct = round((reseller_gross_margin / max(1.0, end_user_quote)) * 100.0, 1)

        return {
            "list_price": list_price,
            "reseller_discount_pct": reseller_discount_pct,
            "wholesale_cost_to_reseller": wholesale_cost,
            "end_user_quote_price": end_user_quote,
            "reseller_gross_profit": reseller_gross_margin,
            "reseller_margin_percentage": reseller_margin_pct,
            "is_profitable_for_partner": reseller_gross_margin > 0
        }
