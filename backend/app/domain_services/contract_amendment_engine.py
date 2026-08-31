from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class ContractAmendmentEngine:
    @staticmethod
    def create_co_termed_amendment(
        original_contract: Dict[str, Any],
        added_products: List[Dict[str, Any]],
        amendment_effective_date: date
    ) -> Dict[str, Any]:
        contract_end = date.fromisoformat(original_contract.get("termination_date", date.today().isoformat()))
        contract_start = date.fromisoformat(original_contract.get("effective_date", date.today().isoformat()))

        total_days = max(1, (contract_end - contract_start).days)
        remaining_days = max(0, (contract_end - amendment_effective_date).days)
        proration_factor = remaining_days / float(total_days)

        amendment_items = []
        total_amendment_cost = 0.0

        for p in added_products:
            annual_price = float(p.get("unit_price", 0.0)) * int(p.get("quantity", 1))
            prorated_price = round(annual_price * proration_factor, 2)
            total_amendment_cost += prorated_price

            amendment_items.append({
                "product_id": p.get("product_id"),
                "name": p.get("name"),
                "quantity": p.get("quantity", 1),
                "full_period_price": annual_price,
                "prorated_cost": prorated_price,
                "days_remaining": remaining_days
            })

        return {
            "original_contract_id": original_contract.get("id"),
            "effective_date": amendment_effective_date.isoformat(),
            "co_termed_termination_date": contract_end.isoformat(),
            "amendment_items": amendment_items,
            "total_amendment_cost": round(total_amendment_cost, 2),
            "new_annualized_contract_value": round(float(original_contract.get("contract_value", {}).get("total_amount", 0.0)) + sum(p.get("unit_price", 0.0) * p.get("quantity", 1) for p in added_products), 2)
        }
