from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
from collections import defaultdict

class EnterpriseSecurityFirewall:
    def __init__(self, max_attempts: int = 5, lockout_minutes: int = 15):
        self.max_attempts = max_attempts
        self.lockout_minutes = lockout_minutes
        self._login_attempts = defaultdict(list)
        self._locked_ips = {}

    def record_attempt(self, ip_address: str, success: bool) -> bool:
        now = datetime.now(timezone.utc)
        
        # Clean up expired lockouts
        if ip_address in self._locked_ips and now > self._locked_ips[ip_address]:
            del self._locked_ips[ip_address]

        if ip_address in self._locked_ips:
            return False # Blocked

        if success:
            self._login_attempts[ip_address] = []
            return True

        # Failed attempt
        self._login_attempts[ip_address].append(now)
        recent_failures = [t for t in self._login_attempts[ip_address] if now - t < timedelta(minutes=self.lockout_minutes)]
        self._login_attempts[ip_address] = recent_failures

        if len(recent_failures) >= self.max_attempts:
            self._locked_ips[ip_address] = now + timedelta(minutes=self.lockout_minutes)
            return False

        return True
