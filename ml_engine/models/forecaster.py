import numpy as np
from sklearn.linear_model import Ridge
from typing import List, Dict

class ExpenseForecastingModel:
    def __init__(self):
        self.model = Ridge(alpha=1.0)
        self.is_trained = False

    def train_and_predict(self, daily_expenses: List[float], horizon_days: int = 30) -> Dict[str, any]:
        if len(daily_expenses) < 14:
            mean_exp = np.mean(daily_expenses) if daily_expenses else 1500.0
            daily_preds = [float(mean_exp * (1.0 + np.sin(i / 4.0) * 0.15)) for i in range(horizon_days)]
        else:
            X = np.array(range(len(daily_expenses))).reshape(-1, 1)
            y = np.array(daily_expenses)
            self.model.fit(X, y)
            future_X = np.array(range(len(daily_expenses), len(daily_expenses) + horizon_days)).reshape(-1, 1)
            preds = self.model.predict(future_X)
            daily_preds = [max(100.0, float(p)) for p in preds]

        total_predicted = sum(daily_preds)
        std_val = np.std(daily_expenses) if len(daily_expenses) > 1 else (total_predicted * 0.08)

        return {
            "daily_predictions": daily_preds,
            "total_predicted_expense": round(total_predicted, 2),
            "confidence_band_std": round(float(std_val), 2),
            "lower_bound_total": round(max(0.0, total_predicted - (1.96 * std_val * np.sqrt(horizon_days))), 2),
            "upper_bound_total": round(total_predicted + (1.96 * std_val * np.sqrt(horizon_days)), 2)
        }
