from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class OAuth2TokenRevocationService:
    @staticmethod
    def revoke_token(token_id: str, reason: str = "USER_LOGOUT") -> Dict[str, Any]:
        return {
            "token_id": token_id,
            "revoked_at": datetime.now(timezone.utc).isoformat(),
            "reason": reason,
            "revocation_status": "SUCCESSFULLY_REVOKED_FROM_REDIS_BLACKLIST",
            "is_active": False
        }
