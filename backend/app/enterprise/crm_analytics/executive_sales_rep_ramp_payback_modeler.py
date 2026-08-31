from typing import Any, Dict, List, Optional

class RepRampPaybackModeler:
    @staticmethod
    def calculate_hiring_payback(reps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for r in reps:
            name = r.get("rep_name")
            ote_annual = float(r.get("annual_ote", 180000.0))
            monthly_base = ote_annual / 12.0
            cumulative_closed_margin = float(r.get("cumulative_closed_gross_margin", 0.0))
            tenure_months = int(r.get("tenure_months", 6))

            fully_loaded_cost = (monthly_base * tenure_months) * 1.25 # 25% overhead
            net_contribution = cumulative_closed_margin - fully_loaded_cost
            roi_multiple = round(cumulative_closed_margin / max(1.0, fully_loaded_cost), 2)

            results.append({
                "rep_name": name,
                "tenure_months": tenure_months,
                "fully_loaded_hiring_cost": round(fully_loaded_cost, 2),
                "cumulative_gross_margin_generated": cumulative_closed_margin,
                "net_profit_contribution": round(net_contribution, 2),
                "hiring_roi_multiple": roi_multiple,
                "is_payback_achieved": net_contribution > 0
            })

        return sorted(results, key=lambda x: x["hiring_roi_multiple"], reverse=True)
