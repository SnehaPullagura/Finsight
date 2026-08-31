from typing import Any, Dict, List, Optional, Tuple
from collections import defaultdict

class InMemOLAPCube:
    def __init__(self, fact_records: List[Dict[str, Any]], dimensions: List[str], metric_keys: List[str]):
        self.fact_records = fact_records
        self.dimensions = dimensions
        self.metric_keys = metric_keys

    def slice_and_dice(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        filtered = []
        for record in self.fact_records:
            match = True
            for dim, expected in filters.items():
                if record.get(dim) != expected:
                    match = False
                    break
            if match:
                filtered.append(record)
        return filtered

    def aggregate_by(self, group_by_dimensions: List[str]) -> List[Dict[str, Any]]:
        groups = defaultdict(lambda: {k: 0.0 for k in self.metric_keys})
        counts = defaultdict(int)

        for record in self.fact_records:
            key_tuple = tuple(record.get(dim) for dim in group_by_dimensions)
            for m in self.metric_keys:
                groups[key_tuple][m] += float(record.get(m, 0.0))
            counts[key_tuple] += 1

        result = []
        for key_tuple, metric_sums in groups.items():
            entry = {dim: key_tuple[i] for i, dim in enumerate(group_by_dimensions)}
            for m, total_val in metric_sums.items():
                entry[f"total_{m}"] = round(total_val, 2)
                entry[f"avg_{m}"] = round(total_val / max(1, counts[key_tuple]), 2)
            entry["record_count"] = counts[key_tuple]
            result.append(entry)

        return sorted(result, key=lambda x: x.get(f"total_{self.metric_keys[0]}", 0), reverse=True)
