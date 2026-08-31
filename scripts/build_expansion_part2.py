import os
import sys
sys.path.insert(0, os.path.abspath("."))
from scripts.common import write_file

def run():
    # 1. backend/app/enterprise/ml_models/churn_classifier.py
    write_file("backend/app/enterprise/ml_models/churn_classifier.py", """import math
from typing import Any, Dict, List, Optional

class DecisionTreeNode:
    def __init__(self, feature: Optional[str] = None, threshold: Optional[float] = None, left: Optional['DecisionTreeNode'] = None, right: Optional['DecisionTreeNode'] = None, value: Optional[float] = None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

    def predict(self, sample: Dict[str, float]) -> float:
        if self.value is not None:
            return self.value
        val = sample.get(self.feature, 0.0)
        if val <= self.threshold:
            return self.left.predict(sample) if self.left else 0.0
        else:
            return self.right.predict(sample) if self.right else 1.0

class CustomerChurnDecisionTreeClassifier:
    def __init__(self):
        # Pre-trained decision tree logic for SaaS customer retention
        # Root: Product Usage Intensity (logins / week)
        # Left: Low usage (<= 3.0 logins/week) -> Check Support Tickets
        # Right: High usage (> 3.0 logins/week) -> Check NPS
        low_usage_ticket_node = DecisionTreeNode(
            feature="unresolved_tickets",
            threshold=2.0,
            left=DecisionTreeNode(value=0.45),  # Low usage but low tickets -> 45% churn risk
            right=DecisionTreeNode(value=0.88)  # Low usage and high tickets -> 88% churn risk (High Risk)
        )

        high_usage_nps_node = DecisionTreeNode(
            feature="nps_score",
            threshold=6.0,
            left=DecisionTreeNode(value=0.30),  # High usage but detractors -> 30% churn risk
            right=DecisionTreeNode(value=0.05)  # High usage and promoters -> 5% churn risk (Healthy)
        )

        self.root = DecisionTreeNode(
            feature="logins_per_week",
            threshold=3.0,
            left=low_usage_ticket_node,
            right=high_usage_nps_node
        )

    def evaluate_customer_churn_risk(self, customer_metrics: Dict[str, float]) -> Dict[str, Any]:
        risk_probability = self.root.predict(customer_metrics)
        risk_pct = round(risk_probability * 100.0, 1)

        tier = "Critical" if risk_pct >= 75.0 else "Elevated" if risk_pct >= 40.0 else "Normal"

        recommendations = []
        if customer_metrics.get("logins_per_week", 0) <= 3.0:
            recommendations.append("Conduct proactive user re-engagement and feature adoption training")
        if customer_metrics.get("unresolved_tickets", 0) >= 2.0:
            recommendations.append("Escalate open support tickets to Senior Engineering Lead")
        if customer_metrics.get("nps_score", 10) <= 6.0:
            recommendations.append("Schedule VP Executive Alignment meeting to address customer feedback")

        return {
            "churn_risk_probability": risk_probability,
            "churn_risk_percentage": risk_pct,
            "risk_tier": tier,
            "recommended_interventions": recommendations,
            "features_evaluated": customer_metrics
        }
""")

    # 2. backend/app/enterprise/ml_models/time_series_arima.py
    write_file("backend/app/enterprise/ml_models/time_series_arima.py", """import math
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
""")

    print("Created churn classifier and time series ARIMA.")

if __name__ == '__main__':
    run()
