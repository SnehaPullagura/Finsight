from typing import Any, Dict, List, Optional

class MultiYearPricingGuard:
    @staticmethod
    def audit_pricing_floor(contract_term_years: int, proposed_discount_pct: float, customer_tier: str = "ENTERPRISE") -> Dict[str, Any]:
        max_allowed_discounts = {
            1: 5.0,
            2: 12.0,
            3: 20.0,
            5: 30.0
        }
        max_allowed = max_allowed_discounts.get(contract_term_years, 10.0)
        is_compliant = proposed_discount_pct <= max_allowed

        return {
            "contract_term_years": contract_term_years,
            "proposed_discount_percentage": proposed_discount_pct,
            "max_allowed_discount_floor": max_allowed,
            "is_pricing_guardrail_compliant": is_compliant,
            "required_approval_tier": "AUTOMATED_SYSTEM_PASS" if is_compliant else "CRO_EXECUTIVE_APPROVAL_REQUIRED"
        }
