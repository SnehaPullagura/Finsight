from typing import Any, Dict, List, Optional

class MagicNumberTrendAnalyzer:
    @staticmethod
    def calculate_quarterly_magic_numbers(quarterly_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for q in quarterly_data:
            q_name = q.get("quarter", "Q1")
            net_new_arr = float(q.get("net_new_arr", 100000.0))
            sm_spend = float(q.get("sm_spend_prior_quarter", 100000.0))

            magic_num = round(net_new_arr / max(1.0, sm_spend), 2)
            tier = "World Class (> 1.0x)" if magic_num >= 1.0 else "Efficient (0.75x - 1.0x)" if magic_num >= 0.75 else "Spend Inefficient (< 0.75x)"

            results.append({
                "quarter": q_name,
                "net_new_arr": net_new_arr,
                "sm_spend_prior_quarter": sm_spend,
                "magic_number": magic_num,
                "efficiency_tier": tier,
                "is_investable": magic_num >= 0.75
            })

        return results
