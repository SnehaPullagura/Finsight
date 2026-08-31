import math
from datetime import datetime, date, timedelta
from typing import Any, Dict, List, Optional, Tuple

class SalesVelocityMatrix:
    @staticmethod
    def compute_funnel_conversion_rates(stage_counts: Dict[str, int]) -> Dict[str, Any]:
        stages = ["lead", "discovery", "scoping", "proposal", "negotiation", "won"]
        conversion_steps = []
        
        for i in range(len(stages) - 1):
            curr_stage = stages[i]
            next_stage = stages[i + 1]
            curr_count = stage_counts.get(curr_stage, 0)
            next_count = stage_counts.get(next_stage, 0)
            
            rate = round((next_count / max(1, curr_count)) * 100.0, 2)
            conversion_steps.append({
                "from_stage": curr_stage,
                "to_stage": next_stage,
                "from_count": curr_count,
                "to_count": next_count,
                "conversion_rate_pct": min(100.0, rate)
            })

        overall_lead_count = stage_counts.get("lead", 1)
        overall_won_count = stage_counts.get("won", 0)
        overall_conversion = round((overall_won_count / max(1, overall_lead_count)) * 100.0, 2)

        return {
            "funnel_steps": conversion_steps,
            "overall_conversion_rate": overall_conversion,
            "total_leads_entered": overall_lead_count,
            "total_deals_won": overall_won_count
        }

    @staticmethod
    def calculate_stage_bottlenecks(stage_durations: Dict[str, List[float]], benchmark_days: Dict[str, float]) -> List[Dict[str, Any]]:
        bottlenecks = []
        for stage, durations in stage_durations.items():
            if not durations:
                continue
            avg_duration = sum(durations) / float(len(durations))
            benchmark = benchmark_days.get(stage, 14.0)
            excess = avg_duration - benchmark
            
            is_bottleneck = excess > 3.0
            bottlenecks.append({
                "stage": stage,
                "average_days": round(avg_duration, 1),
                "benchmark_days": benchmark,
                "excess_days": round(excess, 1),
                "is_bottleneck": is_bottleneck,
                "severity": "high" if excess > 7.0 else "medium" if is_bottleneck else "normal"
            })
        return sorted(bottlenecks, key=lambda b: b["excess_days"], reverse=True)
