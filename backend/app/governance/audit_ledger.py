import hashlib
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

class CryptographicAuditLedger:
    @staticmethod
    def compute_block_hash(
        block_index: int,
        timestamp: str,
        actor_id: str,
        action: str,
        entity_type: str,
        entity_id: str,
        state_diff: Dict[str, Any],
        previous_hash: str
    ) -> str:
        payload = {
            "index": block_index,
            "timestamp": timestamp,
            "actor_id": actor_id,
            "action": action,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "diff": state_diff,
            "prev_hash": previous_hash
        }
        serialized = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
