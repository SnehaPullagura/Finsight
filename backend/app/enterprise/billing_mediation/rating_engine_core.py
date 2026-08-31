from typing import Any, Dict, List, Optional

class RatingEngineCore:
    """
    Calculates metered billing rating charges supporting graduated, volume, and overage pricing models.
    """
    @staticmethod
    def rate_overage_charge(
        included_allowance: float,
        actual_consumed: float,
        overage_unit_price: float
    ) -> Dict[str, Any]:
        overage_units = max(0.0, actual_consumed - included_allowance)
        overage_charge = round(overage_units * overage_unit_price, 2)
        allowance_utilization_pct = round((actual_consumed / max(1.0, included_allowance)) * 100.0, 1)

        return {
            "included_monthly_allowance": included_allowance,
            "actual_units_consumed": actual_consumed,
            "overage_units_rated": overage_units,
            "overage_unit_price": overage_unit_price,
            "total_overage_charge": overage_charge,
            "allowance_utilization_pct": allowance_utilization_pct,
            "is_overage_triggered": overage_units > 0
        }
