import hmac
import hashlib
import time
import struct
import base64
from typing import Optional

class TOTPAuthenticator:
    @staticmethod
    def generate_current_totp(secret_base32: str, time_step: int = 30) -> str:
        # RFC 6238 Time-Based One-Time Password Implementation
        key = base64.b32decode(secret_base32, casefold=True)
        current_time = int(time.time())
        time_counter = current_time // time_step
        
        msg = struct.pack(">Q", time_counter)
        h = hmac.new(key, msg, hashlib.sha1).digest()
        
        offset = h[19] & 0x0F
        truncated_hash = (struct.unpack(">I", h[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
        return f"{truncated_hash:06d}"

    @staticmethod
    def verify_totp_code(secret_base32: str, user_code: str, window: int = 1) -> bool:
        # Check current and adjacent time windows for clock drift
        current_time = int(time.time())
        for delta in range(-window, window + 1):
            key = base64.b32decode(secret_base32, casefold=True)
            time_counter = (current_time // 30) + delta
            msg = struct.pack(">Q", time_counter)
            h = hmac.new(key, msg, hashlib.sha1).digest()
            offset = h[19] & 0x0F
            truncated = (struct.unpack(">I", h[offset:offset + 4])[0] & 0x7FFFFFFF) % 1000000
            if f"{truncated:06d}" == str(user_code).strip():
                return True
        return False
