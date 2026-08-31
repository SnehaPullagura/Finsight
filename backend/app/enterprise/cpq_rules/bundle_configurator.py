from typing import Any, Dict, List, Optional, Set

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
