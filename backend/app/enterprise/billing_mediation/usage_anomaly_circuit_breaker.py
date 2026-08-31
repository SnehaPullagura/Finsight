from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class UsageAnomalyCircuitBreaker:
    """
    Fraud & Usage Surge Circuit Breaker:
    Halts automated billing charges if sudden 10x usage spikes are detected (e.g. runaway customer script).
    """
    @staticmethod
    def inspect_usage_spike(
        baseline_daily_average: float,
        today_usage: float,
        spike_multiplier_threshold: float = 5.0
    ) -> Dict[str, Any]:
        ratio = round(today_usage / max(1.0, baseline_daily_average), 2)
        is_tripped = ratio >= spike_multiplier_threshold

        return {
            "baseline_daily_average": baseline_daily_average,
            "current_day_usage": today_usage,
            "usage_surge_multiple": ratio,
            "circuit_breaker_tripped": is_tripped,
            "protection_status": "CHARGING_HALTED_MANUAL_AUDIT" if is_tripped else "NORMAL_STREAMING",
            "prescribed_remedy": "Notify customer tech lead of unusual traffic surge before invoicing." if is_tripped else "None"
        }
