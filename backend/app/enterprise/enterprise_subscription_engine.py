from datetime import date, timedelta
from typing import Any, Dict, List, Optional

class EnterpriseSubscriptionEngine:
    @staticmethod
    def calculate_co_terming_schedule(
        base_subscription: Dict[str, Any],
        add_on_items: List[Dict[str, Any]],
        add_on_effective_date: date
    ) -> Dict[str, Any]:
        sub_end = date.fromisoformat(base_subscription.get("current_period_end", date.today().isoformat()))
        sub_start = date.fromisoformat(base_subscription.get("current_period_start", date.today().isoformat()))

        total_period_days = max(1, (sub_end - sub_start).days)
        proration_days = max(0, (sub_end - add_on_effective_date).days)
        proration_fraction = proration_days / float(total_period_days)

        calculated_items = []
        total_prorated_charge = 0.0

        for item in add_on_items:
            unit_price = float(item.get("unit_price", 0.0))
            qty = int(item.get("quantity", 1))
            full_price = unit_price * qty
            prorated = round(full_price * proration_fraction, 2)
            total_prorated_charge += prorated

            calculated_items.append({
                "item_name": item.get("name"),
                "quantity": qty,
                "full_price": full_price,
                "prorated_charge": prorated,
                "effective_days": proration_days
            })

        return {
            "subscription_id": base_subscription.get("id"),
            "effective_date": add_on_effective_date.isoformat(),
            "period_end": sub_end.isoformat(),
            "prorated_items": calculated_items,
            "immediate_total_due": round(total_prorated_charge, 2)
        }
