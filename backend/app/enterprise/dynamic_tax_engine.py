from typing import Any, Dict, List, Optional

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
