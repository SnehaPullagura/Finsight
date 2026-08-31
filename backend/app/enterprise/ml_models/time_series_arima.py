import math
from typing import Any, Dict, List, Optional, Tuple

class TimeSeriesAutoRegression:
    @staticmethod
    def difference_series(series: List[float], order: int = 1) -> List[float]:
        diff = list(series)
        for _ in range(order):
            diff = [diff[i] - diff[i - 1] for i in range(1, len(diff))]
        return diff

    @staticmethod
    def fit_ar_coefficients(series: List[float], lag_p: int = 2) -> List[float]:
        n = len(series)
        if n <= lag_p + 1:
            return [1.0 / lag_p] * lag_p

        # Autoregressive least squares estimator
        coeffs = []
        for p in range(1, lag_p + 1):
            numerator = sum(series[t] * series[t - p] for t in range(p, n))
            denominator = sum(series[t - p] ** 2 for t in range(p, n))
            phi = numerator / max(1e-6, denominator)
            coeffs.append(round(phi, 4))

        return coeffs

    @staticmethod
    def forecast(series: List[float], steps: int = 6, lag_p: int = 2) -> Dict[str, Any]:
        if not series:
            return {"forecast": [0.0] * steps, "confidence_bounds": []}

        coeffs = TimeSeriesAutoRegression.fit_ar_coefficients(series, lag_p=lag_p)
        history = list(series)
        forecasts = []
        bounds = []

        mean_val = sum(series) / float(len(series))
        variance = sum((x - mean_val) ** 2 for x in series) / float(max(1, len(series)))
        std_dev = math.sqrt(variance)

        for step_idx in range(steps):
            pred = 0.0
            for i, phi in enumerate(coeffs):
                lag_idx = -(i + 1)
                pred += phi * history[lag_idx]

            pred_val = round(max(0.0, pred), 2)
            forecasts.append(pred_val)
            history.append(pred_val)

            margin = round(std_dev * math.sqrt(step_idx + 1) * 1.96, 2)
            bounds.append({
                "step": step_idx + 1,
                "forecast": pred_val,
                "lower_95": max(0.0, round(pred_val - margin, 2)),
                "upper_95": round(pred_val + margin, 2)
            })

        return {
            "forecast_steps": steps,
            "point_forecasts": forecasts,
            "confidence_bounds": bounds,
            "ar_coefficients": coeffs
        }
