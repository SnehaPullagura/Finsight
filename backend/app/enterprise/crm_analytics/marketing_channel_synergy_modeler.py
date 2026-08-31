from typing import Any, Dict, List, Optional
from collections import defaultdict

class MarketingChannelSynergyModeler:
    @staticmethod
    def calculate_multi_touch_synergy_lift(journey_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        single_touch_conversions = 0
        multi_touch_conversions = 0
        single_touch_total = 0
        multi_touch_total = 0

        for j in journey_records:
            channels = j.get("touchpoint_channels", [])
            converted = bool(j.get("is_converted", False))

            if len(channels) <= 1:
                single_touch_total += 1
                if converted:
                    single_touch_conversions += 1
            else:
                multi_touch_total += 1
                if converted:
                    multi_touch_conversions += 1

        single_rate = round((single_touch_conversions / max(1, single_touch_total)) * 100.0, 1)
        multi_rate = round((multi_touch_conversions / max(1, multi_touch_total)) * 100.0, 1)
        synergy_lift = round(multi_rate - single_rate, 1)

        return {
            "single_channel_conversion_pct": single_rate,
            "multi_channel_conversion_pct": multi_rate,
            "synergy_lift_percentage": synergy_lift,
            "is_omnichannel_strategy_validated": synergy_lift > 5.0
        }
