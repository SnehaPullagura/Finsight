from typing import Any, Dict, List, Tuple
from collections import defaultdict

class OLAPAggregationEngine:
    @staticmethod
    def compute_multi_dimensional_cube(
        records: List[Dict[str, Any]],
        dimension_keys: List[str],
        metric_key: str = "value"
    ) -> List[Dict[str, Any]]:
        cube = defaultdict(float)
        counts = defaultdict(int)

        for r in records:
            dim_values = tuple(r.get(k, "Unknown") for k in dimension_keys)
            val = float(r.get(metric_key, 0.0))
            cube[dim_values] += val
            counts[dim_values] += 1

        results = []
        for dim_values, total_val in cube.items():
            entry = {dimension_keys[i]: dim_values[i] for i in range(len(dimension_keys))}
            entry[f"total_{metric_key}"] = round(total_val, 2)
            entry["record_count"] = counts[dim_values]
            entry[f"avg_{metric_key}"] = round(total_val / max(1, counts[dim_values]), 2)
            results.append(entry)

        return sorted(results, key=lambda x: x[f"total_{metric_key}"], reverse=True)
