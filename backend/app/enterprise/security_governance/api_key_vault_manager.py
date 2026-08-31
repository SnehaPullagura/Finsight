import secrets
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

class APIKeyVaultManager:
    @staticmethod
    def generate_scoped_api_key(tenant_id: str, name: str, scopes: List[str], expires_in_days: int = 90) -> Dict[str, Any]:
        raw_token = f"cfk_{secrets.token_urlsafe(32)}"
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        expires_at = datetime.now(timezone.utc) + timedelta(days=expires_in_days)

        return {
            "key_id": f"key_{token_hash[:12]}",
            "name": name,
            "tenant_id": tenant_id,
            "masked_key": f"{raw_token[:7]}...{raw_token[-4:]}",
            "raw_key_plain": raw_token, # Only returned once upon creation
            "token_hash": token_hash,
            "scopes": scopes,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": expires_at.isoformat()
        }
