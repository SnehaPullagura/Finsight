import hmac
import hashlib
from typing import Any, Dict, Optional

class DatabaseBlindIndexer:
    @staticmethod
    def generate_blind_index(plaintext_value: str, blind_index_key: str) -> str:
        cleaned = plaintext_value.strip().lower()
        b_idx = hmac.new(blind_index_key.encode(), cleaned.encode(), hashlib.sha256).hexdigest()
        return f"bidx_{b_idx[:32]}"
