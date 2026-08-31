from typing import Any, Dict, List, Tuple

class BulkUpsertCoordinator:
    @staticmethod
    def partition_inserts_and_updates(
        incoming_batch: List[Dict[str, Any]],
        existing_lookup: Dict[str, str], # email/key -> existing_id
        match_key: str = "email"
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        inserts = []
        updates = []

        for row in incoming_batch:
            key_val = (row.get(match_key) or "").lower().strip()
            if key_val in existing_lookup:
                row_copy = dict(row)
                row_copy["id"] = existing_lookup[key_val]
                updates.append(row_copy)
            else:
                inserts.append(row)

        return inserts, updates
