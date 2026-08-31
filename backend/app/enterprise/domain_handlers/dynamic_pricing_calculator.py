from typing import Any, Dict, List, Optional

class DynamicPricingCalculator:
    @staticmethod
    def calculate_enterprise_quote(
        base_product_price: float,
        user_licenses: int,
        support_tier: str, # standard, gold, platinum
        contract_duration_years: int,
        custom_discount_pct: float = 0.0
    ) -> Dict[str, Any]:
        license_subtotal = base_product_price * user_licenses
        
        # Support tier multiplier
        support_pct = 0.10 if support_tier.lower() == "gold" else 0.20 if support_tier.lower() == "platinum" else 0.0
        support_cost_annual = license_subtotal * support_pct

        annual_gross = license_subtotal + support_cost_annual

        # Multi-year commitment discount
        term_discount_pct = 0.15 if contract_duration_years >= 3 else 0.08 if contract_duration_years >= 2 else 0.0
        
        total_discount_pct = min(0.40, term_discount_pct + (custom_discount_pct / 100.0))
        discount_amount_annual = annual_gross * total_discount_pct

        annual_net = max(0.0, annual_gross - discount_amount_annual)
        total_contract_value = round(annual_net * contract_duration_years, 2)
        monthly_mrr = round(annual_net / 12.0, 2)

        return {
            "user_licenses": user_licenses,
            "contract_duration_years": contract_duration_years,
            "support_tier": support_tier,
            "annual_gross_price": round(annual_gross, 2),
            "term_discount_percentage": round(term_discount_pct * 100, 1),
            "custom_discount_percentage": custom_discount_pct,
            "effective_annual_net": round(annual_net, 2),
            "total_contract_value": total_contract_value,
            "monthly_recurring_revenue": monthly_mrr
        }
