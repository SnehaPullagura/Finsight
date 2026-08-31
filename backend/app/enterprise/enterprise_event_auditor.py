import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class AuditBlock:
    def __init__(self, index: int, timestamp: str, tenant_id: str, actor_id: str, action: str, entity_type: str, entity_id: str, state_diff: Dict[str, Any], previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.tenant_id = tenant_id
        self.actor_id = actor_id
        self.action = action
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.state_diff = state_diff
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        payload = {
            "index": self.index,
            "timestamp": self.timestamp,
            "tenant_id": self.tenant_id,
            "actor_id": self.actor_id,
            "action": self.action,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "diff": self.state_diff,
            "previous_hash": self.previous_hash
        }
        serialized = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

class EnterpriseEventAuditor:
    def __init__(self):
        self.chain: List[AuditBlock] = []
        self._initialize_genesis_block()

    def _initialize_genesis_block(self):
        genesis = AuditBlock(
            index=0,
            timestamp=datetime.now(timezone.utc).isoformat(),
            tenant_id="system",
            actor_id="system",
            action="GENESIS",
            entity_type="SYSTEM",
            entity_id="0",
            state_diff={},
            previous_hash="0" * 64
        )
        self.chain.append(genesis)

    def record_event(self, tenant_id: str, actor_id: str, action: str, entity_type: str, entity_id: str, state_diff: Dict[str, Any]) -> AuditBlock:
        prev_block = self.chain[-1]
        block = AuditBlock(
            index=len(self.chain),
            timestamp=datetime.now(timezone.utc).isoformat(),
            tenant_id=tenant_id,
            actor_id=actor_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            state_diff=state_diff,
            previous_hash=prev_block.hash
        )
        self.chain.append(block)
        return block

    def verify_integrity(self) -> bool:
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if curr.previous_hash != prev.hash:
                return False
            if curr.hash != curr.compute_hash():
                return False
        return True
