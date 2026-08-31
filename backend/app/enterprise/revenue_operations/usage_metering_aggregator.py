from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class UsageMeteringAggregator:
    """
    Aggregates high-throughput usage events (API calls, storage GB, AI tokens)
    and computes rating charges based on tiered or graduated pricing models.
    """
    @staticmethod
    def compute_tiered_charge(
        metric_name: str,
        units_consumed: float,
        tiers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        total_charge = 0.0
        remaining_units = units_consumed
        tier_breakdown = []

        for tier in sorted(tiers, key=lambda x: x.get("min_units", 0)):
            min_u = float(tier.get("min_units", 0))
            max_u = float(tier.get("max_units", float("inf")))
            rate = float(tier.get("unit_price", 0.0))

            tier_capacity = max_u - min_u
            if remaining_units > 0:
                units_in_tier = min(remaining_units, tier_capacity)
                tier_cost = round(units_in_tier * rate, 4)
                total_charge += tier_cost
                remaining_units -= units_in_tier

                tier_breakdown.append({
                    "tier_range": f"{int(min_u)} - {int(max_u) if max_u != float('inf') else 'Unlimited'}",
                    "units_rated": units_in_tier,
                    "unit_rate": rate,
                    "tier_total": tier_cost
                })

        return {
            "metric_name": metric_name,
            "total_units_consumed": units_consumed,
            "total_rated_charge": round(total_charge, 2),
            "tier_breakdown": tier_breakdown,
            "rated_at": datetime.now(timezone.utc).isoformat()
        }

    @staticmethod
    def aggregate_account_events(
        account_id: str,
        events: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        totals = {}
        for ev in events:
            metric = ev.get("metric_name", "generic_counter")
            val = float(ev.get("quantity", 1.0))
            totals[metric] = totals.get(metric, 0.0) + val

        return {
            "account_id": account_id,
            "event_count": len(events),
            "aggregated_metrics": totals,
            "aggregated_at": datetime.now(timezone.utc).isoformat()
        }
