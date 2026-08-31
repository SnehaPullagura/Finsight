from typing import Any, Dict, List, Optional

class BurnMultipleCalculator:
    @staticmethod
    def calculate_burn_efficiency(net_cash_burned: float, net_new_arr_added: float) -> Dict[str, Any]:
        burn_multiple = round(net_cash_burned / max(1.0, net_new_arr_added), 2)

        tier = "Top Tier Capital Efficiency (< 1.0x)" if burn_multiple < 1.0 else "Good Efficiency (1.0x - 1.5x)" if burn_multiple <= 1.5 else "Moderate Burn (1.5x - 2.0x)" if burn_multiple <= 2.0 else "High Cash Burn (> 2.0x)"

        return {
            "net_cash_burned": net_cash_burned,
            "net_new_arr_added": net_new_arr_added,
            "burn_multiple": burn_multiple,
            "capital_efficiency_tier": tier,
            "is_venture_efficient": burn_multiple <= 1.5
        }
