import math
import statistics
from datetime import datetime, date, timedelta
from typing import Any, Dict, List, Optional, Tuple

class StatisticalForecastModel:
    @staticmethod
    def moving_average_forecast(series: List[float], window_size: int = 3, forecast_periods: int = 3) -> List[float]:
        if len(series) < window_size:
            return [series[-1] if series else 0.0] * forecast_periods

        current_series = list(series)
        forecasts = []

        for _ in range(forecast_periods):
            avg = sum(current_series[-window_size:]) / float(window_size)
            forecasts.append(round(avg, 2))
            current_series.append(avg)

        return forecasts

    @staticmethod
    def linear_trend_regression(series: List[float], forecast_periods: int = 3) -> Dict[str, Any]:
        n = len(series)
        if n < 2:
            return {"slope": 0.0, "intercept": series[0] if series else 0.0, "r_squared": 0.0, "forecast": [0.0] * forecast_periods}

        x = list(range(n))
        y = series

        x_mean = sum(x) / float(n)
        y_mean = sum(y) / float(n)

        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))

        slope = numerator / denominator if denominator != 0 else 0.0
        intercept = y_mean - (slope * x_mean)

        # R-squared calculation
        y_pred = [intercept + slope * xi for xi in x]
        ss_res = sum((y[i] - y_pred[i]) ** 2 for i in range(n))
        ss_tot = sum((y[i] - y_mean) ** 2 for i in range(n))
        r_squared = 1.0 - (ss_res / ss_tot) if ss_tot != 0 else 1.0

        future_x = range(n, n + forecast_periods)
        forecasts = [round(max(0.0, intercept + slope * fx), 2) for fx in future_x]

        return {
            "slope": round(slope, 4),
            "intercept": round(intercept, 2),
            "r_squared": round(max(0.0, min(1.0, r_squared)), 4),
            "forecast": forecasts
        }

    @staticmethod
    def exponential_smoothing(series: List[float], alpha: float = 0.3, forecast_periods: int = 3) -> List[float]:
        if not series:
            return [0.0] * forecast_periods

        smoothed = [series[0]]
        for t in range(1, len(series)):
            st = alpha * series[t] + (1 - alpha) * smoothed[t - 1]
            smoothed.append(st)

        last_smoothed = smoothed[-1]
        return [round(last_smoothed, 2)] * forecast_periods
