import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/cpq_rules/volume_discount_matrix.py
    write_file("backend/app/enterprise/cpq_rules/volume_discount_matrix.py", """import math
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
""")

    # 2. backend/app/enterprise/cpq_rules/bundle_configurator.py
    write_file("backend/app/enterprise/cpq_rules/bundle_configurator.py", """from typing import Any, Dict, List, Optional, Set

class BundleOptionRule:
    def __init__(
        self,
        option_id: str,
        product_code: str,
        name: str,
        is_required: bool = False,
        default_qty: int = 1,
        min_qty: int = 0,
        max_qty: Optional[int] = None,
        price_modifier_pct: float = 0.0,
        incompatible_with: Optional[Set[str]] = None
    ):
        self.option_id = option_id
        self.product_code = product_code
        self.name = name
        self.is_required = is_required
        self.default_qty = default_qty
        self.min_qty = min_qty
        self.max_qty = max_qty
        self.price_modifier_pct = price_modifier_pct
        self.incompatible_with = incompatible_with or set()

class ProductBundleDefinition:
    def __init__(self, bundle_code: str, bundle_name: str, base_price: float, options: List[BundleOptionRule]):
        self.bundle_code = bundle_code
        self.bundle_name = bundle_name
        self.base_price = base_price
        self.options = {opt.product_code: opt for opt in options}

    def validate_configuration(self, selected_options: Dict[str, int]) -> Dict[str, Any]:
        errors = []
        warnings = []
        selected_codes = set(selected_options.keys())

        # 1. Check required options
        for code, opt in self.options.items():
            if opt.is_required and code not in selected_codes:
                errors.append(f"Required option '{opt.name}' ({code}) is missing.")

        # 2. Check quantities & incompatibilities
        total_bundle_price = self.base_price

        for code, qty in selected_options.items():
            if code not in self.options:
                errors.append(f"Invalid option code '{code}' for bundle '{self.bundle_name}'.")
                continue

            opt = self.options[code]
            if qty < opt.min_qty:
                errors.append(f"Quantity for '{opt.name}' cannot be less than minimum {opt.min_qty}.")
            if opt.max_qty is not None and qty > opt.max_qty:
                errors.append(f"Quantity for '{opt.name}' cannot exceed maximum {opt.max_qty}.")

            # Incompatibility check
            conflicts = opt.incompatible_with.intersection(selected_codes)
            if conflicts:
                errors.append(f"Option '{opt.name}' cannot be selected alongside conflicting option(s): {', '.join(conflicts)}.")

        is_valid = len(errors) == 0

        return {
            "bundle_code": self.bundle_code,
            "bundle_name": self.bundle_name,
            "is_valid": is_valid,
            "errors": errors,
            "warnings": warnings,
            "selected_count": len(selected_options)
        }
""")

    print("Created volume discount matrix and bundle configurator.")

if __name__ == '__main__':
    run()
