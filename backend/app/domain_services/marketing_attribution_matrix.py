from typing import Any, Dict, List, Optional

class MarketingAttributionMatrix:
    @staticmethod
    def calculate_w_shaped_attribution(touchpoints: List[Dict[str, Any]], total_revenue: float) -> Dict[str, float]:
        if not touchpoints:
            return {}

        n = len(touchpoints)
        if n == 1:
            return {touchpoints[0]["channel"]: round(total_revenue, 2)}
        elif n == 2:
            return {
                touchpoints[0]["channel"]: round(total_revenue * 0.50, 2),
                touchpoints[1]["channel"]: round(total_revenue * 0.50, 2)
            }

        # W-Shaped: 30% First Touch, 30% Lead Creation Touch, 30% Opportunity Creation Touch, 10% split across remaining
        first_touch = touchpoints[0]["channel"]
        last_touch = touchpoints[-1]["channel"]
        mid_touch = touchpoints[int(n / 2)]["channel"]

        attribution = {}
        attribution[first_touch] = attribution.get(first_touch, 0.0) + round(total_revenue * 0.30, 2)
        attribution[mid_touch] = attribution.get(mid_touch, 0.0) + round(total_revenue * 0.30, 2)
        attribution[last_touch] = attribution.get(last_touch, 0.0) + round(total_revenue * 0.30, 2)

        remaining_count = max(1, n - 3)
        remaining_pool = round(total_revenue * 0.10, 2)
        per_item = remaining_pool / float(remaining_count)

        for i in range(1, n - 1):
            if i != int(n / 2):
                ch = touchpoints[i]["channel"]
                attribution[ch] = attribution.get(ch, 0.0) + round(per_item, 2)

        return attribution
