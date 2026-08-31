from typing import Any, Dict, List, Optional
from collections import defaultdict

class ChannelLTVToCACRatioCube:
    @staticmethod
    def calculate_channel_multiples(channels_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for ch in channels_data:
            name = ch.get("name", "Channel")
            cac = float(ch.get("cac", 1000.0))
            ltv = float(ch.get("ltv", 5000.0))
            ratio = round(ltv / max(1.0, cac), 2)

            grade = "Top Decile (> 5.0x)" if ratio >= 5.0 else "Healthy (3.0x - 5.0x)" if ratio >= 3.0 else "Unprofitable (< 3.0x)"

            results.append({
                "channel_name": name,
                "cac": cac,
                "ltv": ltv,
                "ltv_to_cac_ratio": ratio,
                "unit_economics_grade": grade,
                "is_scalable": ratio >= 3.0
            })

        return sorted(results, key=lambda x: x["ltv_to_cac_ratio"], reverse=True)
