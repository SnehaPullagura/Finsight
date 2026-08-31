import numpy as np
from sklearn.ensemble import IsolationForest
from typing import List, Dict

class FinancialAnomalyDetectionModel:
    def __init__(self, contamination: float = 0.05):
        self.iso_forest = IsolationForest(contamination=contamination, random_state=42)
        self.is_fitted = False

    def detect_anomalies(self, feature_matrix: List[List[float]]) -> List[Dict[str, any]]:
        if len(feature_matrix) < 10:
            return [{"is_anomaly": False, "anomaly_score": 0.10} for _ in feature_matrix]

        X = np.array(feature_matrix)
        self.iso_forest.fit(X)
        raw_scores = self.iso_forest.score_samples(X)
        min_s, max_s = np.min(raw_scores), np.max(raw_scores)
        norm_scores = 1.0 - ((raw_scores - min_s) / (max_s - min_s + 1e-5))

        results = []
        for s in norm_scores:
            results.append({
                "is_anomaly": bool(s > 0.75),
                "anomaly_score": round(float(s), 3)
            })
        return results
