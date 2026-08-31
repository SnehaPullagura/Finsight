from typing import Any, Dict, List, Tuple

class DataReconciliationEngine:
    @staticmethod
    def reconcile_datasets(
        source_records: List[Dict[str, Any]],
        target_records: List[Dict[str, Any]],
        primary_key: str = "id"
    ) -> Dict[str, Any]:
        src_map = {str(r.get(primary_key)): r for r in source_records}
        tgt_map = {str(r.get(primary_key)): r for r in target_records}

        matched_keys = set(src_map.keys()).intersection(set(tgt_map.keys()))
        missing_in_target = set(src_map.keys()) - set(tgt_map.keys())
        missing_in_source = set(tgt_map.keys()) - set(src_map.keys())

        discrepancies = []
        for k in matched_keys:
            s_rec = src_map[k]
            t_rec = tgt_map[k]
            diffs = {}
            for col in s_rec.keys():
                if s_rec.get(col) != t_rec.get(col):
                    diffs[col] = {"source": s_rec.get(col), "target": t_rec.get(col)}
            if diffs:
                discrepancies.append({"id": k, "field_differences": diffs})

        return {
            "total_source_records": len(source_records),
            "total_target_records": len(target_records),
            "perfect_matches_count": len(matched_keys) - len(discrepancies),
            "discrepancies_count": len(discrepancies),
            "missing_in_target_count": len(missing_in_target),
            "missing_in_source_count": len(missing_in_source),
            "discrepancies": discrepancies[:20]
        }
