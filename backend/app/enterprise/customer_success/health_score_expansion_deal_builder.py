from typing import Any, Dict, List, Optional

class ExpansionQuotePackageBuilder:
    @staticmethod
    def build_quote_proposal(account: Dict[str, Any], expansion_type: str = "SEAT_EXPANSION") -> Dict[str, Any]:
        cname = account.get("name")
        current_seats = int(account.get("current_seats", 50))
        addon_seats = int(current_seats * 0.3)
        seat_price_annual = 1200.0

        subtotal = addon_seats * seat_price_annual
        volume_discount = subtotal * 0.10
        total_amount = subtotal - volume_discount

        return {
            "proposal_title": f"{cname} — Enterprise Expansion Package",
            "expansion_type": expansion_type,
            "additional_seats_quoted": addon_seats,
            "unit_price_annual": seat_price_annual,
            "subtotal": round(subtotal, 2),
            "volume_discount_10pct": round(volume_discount, 2),
            "total_expansion_contract_value": round(total_amount, 2),
            "contract_term": "12 Months (Co-Termed to MSA)"
        }
