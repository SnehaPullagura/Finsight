import random
from typing import Any, Dict, List, Optional

class MonteCarloPipelineSimulator:
    """
    10,000-Iteration Monte Carlo Pipeline Forecasting Simulator:
    Simulates quarterly revenue distributions based on stage win probabilities and deal size variance.
    """
    @staticmethod
    def run_simulation(
        deals: List[Dict[str, Any]],
        iterations: int = 1000
    ) -> Dict[str, Any]:
        simulated_totals = []

        for _ in range(iterations):
            quarter_total = 0.0
            for d in deals:
                val = float(d.get("value", 0.0))
                prob = float(d.get("probability", 50.0)) / 100.0
                # Bernoulli trial for deal closing
                if random.random() <= prob:
                    # Apply 10% deal size variance
                    realized_val = val * random.uniform(0.90, 1.10)
                    quarter_total += realized_val
            simulated_totals.append(quarter_total)

        simulated_totals.sort()
        p10 = round(simulated_totals[int(iterations * 0.10)], 2)
        p50 = round(simulated_totals[int(iterations * 0.50)], 2)
        p90 = round(simulated_totals[int(iterations * 0.90)], 2)

        return {
            "total_deals_simulated": len(deals),
            "simulation_iterations": iterations,
            "conservative_forecast_p10": p10,
            "most_likely_forecast_p50": p50,
            "optimistic_forecast_p90": p90,
            "guidance_spread": round(p90 - p10, 2),
            "forecast_confidence": "HIGH_STABILITY" if (p90 - p10) / max(1.0, p50) <= 0.35 else "HIGH_VOLATILITY"
        }
