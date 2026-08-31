import hashlib
import secrets
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

class DSRSecurityPasscodeGuard:
    """
    Two-Factor PIN & Magic Link Security Guard for Executive Deal Rooms.
    """
    @staticmethod
    def generate_access_passcode(visitor_email: str) -> Dict[str, Any]:
        pin = f"{secrets.randbelow(900000) + 100000}"
        salt = secrets.token_hex(8)
        hashed = hashlib.sha256(f"{pin}:{salt}".encode()).hexdigest()

        return {
            "visitor_email": visitor_email,
            "passcode_pin": pin,
            "passcode_hash": hashed,
            "salt": salt,
            "expires_in_minutes": 15,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
