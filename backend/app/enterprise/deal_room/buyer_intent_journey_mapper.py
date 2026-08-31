from typing import Any, Dict, List, Optional

class BuyerIntentJourneyMapper:
    """
    Reconstructs the full buyer journey timeline from initial cold inbound to proposal sign-off.
    """
    @staticmethod
    def map_journey_timeline(events: List[Dict[str, Any]]) -> Dict[str, Any]:
        sorted_events = sorted(events, key=lambda x: x.get("timestamp", ""))
        touchpoints_by_channel = {}

        for ev in sorted_events:
            ch = ev.get("channel", "Web")
            touchpoints_by_channel[ch] = touchpoints_by_channel.get(ch, 0) + 1

        total_touches = len(sorted_events)

        return {
            "total_touchpoints": total_touches,
            "channels_involved": touchpoints_by_channel,
            "primary_sourcing_channel": max(touchpoints_by_channel, key=touchpoints_by_channel.get) if touchpoints_by_channel else "Web",
            "journey_velocity_rating": "FAST_TRACK (< 30d)" if total_touches <= 8 else "ENTERPRISE_MULTI_TOUCH (> 15 touches)",
            "first_touch_event": sorted_events[0] if sorted_events else {},
            "last_touch_event": sorted_events[-1] if sorted_events else {}
        }
