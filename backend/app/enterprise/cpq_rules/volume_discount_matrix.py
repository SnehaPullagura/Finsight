import math
from typing import Any, Dict, List, Optional, Tuple

class VolumeTier:
    def __init__(self, tier_id: str, min_qty: int, max_qty: Optional[int], discount_pct: float, flat_rebate: float = 0.0):
        self.tier_id = tier_id
        self.min_qty = min_qty
        self.max_qty = max_qty
        self.discount_pct = discount_pct
        self.flat_rebate = flat_rebate

    def applies_to(self, quantity: int) -> bool:
        if quantity < self.min_qty:
            return False
        if self.max_qty is not None and quantity > self.max_qty:
            return False
        return True

class VolumeDiscountMatrix:
    def __init__(self, schedule_id: str, schedule_name: str, tiers: List[VolumeTier]):
        self.schedule_id = schedule_id
        self.schedule_name = schedule_name
        self.tiers = sorted(tiers, key=lambda t: t.min_qty)

    def calculate_tiered_discount(self, unit_price: float, quantity: int) -> Dict[str, Any]:
        applicable_tier = None
        for tier in self.tiers:
            if tier.applies_to(quantity):
                applicable_tier = tier
                break

        if not applicable_tier and self.tiers:
            applicable_tier = self.tiers[0]

        discount_percentage = applicable_tier.discount_pct if applicable_tier else 0.0
        flat_rebate = applicable_tier.flat_rebate if applicable_tier else 0.0

        subtotal = round(unit_price * quantity, 2)
        pct_discount = round(subtotal * (discount_percentage / 100.0), 2)
        total_discount = min(subtotal, round(pct_discount + flat_rebate, 2))
        final_price = max(0.0, round(subtotal - total_discount, 2))
        effective_unit_price = round(final_price / max(1, quantity), 2)

        return {
            "schedule_id": self.schedule_id,
            "schedule_name": self.schedule_name,
            "matched_tier_id": applicable_tier.tier_id if applicable_tier else "none",
            "quantity": quantity,
            "list_unit_price": unit_price,
            "subtotal": subtotal,
            "discount_percentage": discount_percentage,
            "flat_rebate": flat_rebate,
            "total_discount_amount": total_discount,
            "final_payable_amount": final_price,
            "effective_unit_price": effective_unit_price
        }

    @staticmethod
    def get_standard_enterprise_schedule() -> "VolumeDiscountMatrix":
        return VolumeDiscountMatrix(
            schedule_id="sch-ent-vol-01",
            schedule_name="Enterprise Volume Discount Schedule 2026",
            tiers=[
                VolumeTier(tier_id="tier-1", min_qty=1, max_qty=10, discount_pct=0.0),
                VolumeTier(tier_id="tier-2", min_qty=11, max_qty=50, discount_pct=10.0),
                VolumeTier(tier_id="tier-3", min_qty=51, max_qty=200, discount_pct=20.0, flat_rebate=500.0),
                VolumeTier(tier_id="tier-4", min_qty=201, max_qty=1000, discount_pct=30.0, flat_rebate=2500.0),
                VolumeTier(tier_id="tier-5", min_qty=1001, max_qty=None, discount_pct=40.0, flat_rebate=10000.0)
            ]
        )
