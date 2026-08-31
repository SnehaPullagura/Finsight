import math
import random
from typing import Any, Dict, List, Optional

class EnterprisePipelineSimulator:
    @staticmethod
    def simulate_quarter_outcomes(
        deals: List[Dict[str, Any]],
        trials: int = 1000,
        win_rate_adjustment: float = 1.0
    ) -> Dict[str, Any]:
        random.seed(42)
        total_revenues = []

        for _ in range(trials):
            trial_revenue = 0.0
            for d in deals:
                prob = min(1.0, (float(d.get("probability", 50)) / 100.0) * win_rate_adjustment)
                val = float(d.get("value", 0.0))
                if random.random() <= prob:
                    trial_revenue += val
            total_revenues.append(trial_revenue)

        total_revenues.sort()
        n = len(total_revenues)
        p10 = total_revenues[int(n * 0.10)]
        p25 = total_revenues[int(n * 0.25)]
        p50 = total_revenues[int(n * 0.50)]
        p75 = total_revenues[int(n * 0.75)]
        p90 = total_revenues[int(n * 0.90)]
        avg = sum(total_revenues) / float(n)

        return {
            "trials_count": trials,
            "mean_expected_revenue": round(avg, 2),
            "p10_bear_case": round(p10, 2),
            "p25_lower_quartile": round(p25, 2),
            "p50_median_case": round(p50, 2),
            "p75_upper_quartile": round(p75, 2),
            "p90_bull_case": round(p90, 2)
        }
