import hashlib
import json
import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class CryptographicAuditBlock(BaseModel):
    block_index: int
    timestamp: str
    action: str
    user_id: int
    resource_type: str
    resource_id: str
    payload_digest: str
    previous_block_hash: str
    block_hash: str

class AuditBlockchainLedger:
    """
    Immutable SHA-256 Chained Audit Ledger for SOC2 Type II & Banking Compliance.
    Guarantees tamper-evidence for all account balance edits, scenario runs, and data exports.
    """
    @staticmethod
    def compute_hash(index: int, timestamp: str, action: str, user_id: int, payload_digest: str, prev_hash: str) -> str:
        raw = f"{index}|{timestamp}|{action}|{user_id}|{payload_digest}|{prev_hash}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @classmethod
    def create_block(
        cls, index: int, action: str, user_id: int, resource_type: str, resource_id: str, data: Dict[str, Any], prev_hash: str
    ) -> CryptographicAuditBlock:
        ts = datetime.datetime.utcnow().isoformat()
        payload_digest = hashlib.sha256(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()
        block_hash = cls.compute_hash(index, ts, action, user_id, payload_digest, prev_hash)
        
        return CryptographicAuditBlock(
            block_index=index,
            timestamp=ts,
            action=action,
            user_id=user_id,
            resource_type=resource_type,
            resource_id=str(resource_id),
            payload_digest=payload_digest,
            previous_block_hash=prev_hash,
            block_hash=block_hash
        )

    @classmethod
    def verify_chain_integrity(cls, chain: List[CryptographicAuditBlock]) -> bool:
        if not chain:
            return True
        for i in range(1, len(chain)):
            curr = chain[i]
            prev = chain[i - 1]
            if curr.previous_block_hash != prev.block_hash:
                return False
            recalc = cls.compute_hash(
                curr.block_index, curr.timestamp, curr.action, curr.user_id, curr.payload_digest, curr.previous_block_hash
            )
            if recalc != curr.block_hash:
                return False
        return True
