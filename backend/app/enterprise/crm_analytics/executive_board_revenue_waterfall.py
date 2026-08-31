from typing import Any, Dict, List, Optional

class BoardRevenueWaterfallModeler:
    @staticmethod
    def calculate_arr_bridge(
        starting_arr: float,
        new_logo_arr: float,
        expansion_arr: float,
        cross_sell_arr: float,
        contraction_arr: float,
        churn_arr: float
    ) -> Dict[str, Any]:
        gross_new_arr = new_logo_arr + expansion_arr + cross_sell_arr
        total_loss_arr = contraction_arr + churn_arr
        net_new_arr = gross_new_arr - total_loss_arr
        ending_arr = starting_arr + net_new_arr

        arr_growth_pct = round((net_new_arr / max(1.0, starting_arr)) * 100.0, 1)

        return {
            "starting_arr": starting_arr,
            "new_logo_arr": new_logo_arr,
            "expansion_arr": expansion_arr,
            "cross_sell_arr": cross_sell_arr,
            "gross_new_arr": gross_new_arr,
            "contraction_arr": contraction_arr,
            "churn_arr": churn_arr,
            "total_loss_arr": total_loss_arr,
            "net_new_arr": net_new_arr,
            "ending_arr": ending_arr,
            "arr_growth_percentage": arr_growth_pct
        }
