from typing import Any, Dict, List, Optional

class CommissionSplitCalculator:
    @staticmethod
    def calculate_deal_splits(
        deal_value: float,
        split_allocations: List[Dict[str, Any]], # rep_id, percentage, role
        base_rate: float = 0.10
    ) -> Dict[str, Any]:
        total_pct = sum(float(s.get("percentage", 0.0)) for s in split_allocations)
        if total_pct != 100.0:
            raise ValueError(f"Split percentages must sum to exactly 100.0% (current: {total_pct}%).")

        splits = []
        total_commission_pool = deal_value * base_rate

        for s in split_allocations:
            pct = float(s.get("percentage", 0.0))
            rep_id = s.get("rep_id")
            role = s.get("role", "Sales Rep")
            allocated_deal_value = round(deal_value * (pct / 100.0), 2)
            commission_payout = round(total_commission_pool * (pct / 100.0), 2)

            splits.append({
                "rep_id": rep_id,
                "role": role,
                "split_percentage": pct,
                "credited_deal_value": allocated_deal_value,
                "commission_payout": commission_payout
            })

        return {
            "deal_value": deal_value,
            "total_commission_pool": round(total_commission_pool, 2),
            "splits": splits
        }
