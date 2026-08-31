from datetime import date
from typing import Any, Dict, List, Optional

class InvoiceProrationCalculator:
    """
    Calculates exact day-level proration credits and charges for mid-cycle seat additions and tier upgrades.
    """
    @staticmethod
    def calculate_mid_cycle_proration(
        days_in_month: int,
        days_remaining: int,
        current_monthly_rate: float,
        new_monthly_rate: float,
        additional_seats: int = 1
    ) -> Dict[str, Any]:
        rate_diff = (new_monthly_rate - current_monthly_rate) * additional_seats
        daily_rate = rate_diff / max(1, days_in_month)
        prorated_charge = round(daily_rate * days_remaining, 2)

        return {
            "days_in_billing_cycle": days_in_month,
            "days_remaining_in_cycle": days_remaining,
            "additional_seats_added": additional_seats,
            "monthly_rate_difference": round(rate_diff, 2),
            "prorated_charge_due_now": prorated_charge,
            "next_full_cycle_charge": round(new_monthly_rate * additional_seats, 2)
        }
