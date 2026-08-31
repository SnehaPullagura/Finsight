import time
from typing import Dict
from collections import defaultdict
from backend.app.core.exceptions import RateLimitExceededException
from backend.app.core.config import settings

class InMemoryRateLimiter:
    def __init__(self):
        self._requests: Dict[str, list] = defaultdict(list)
    
    def check_rate_limit(self, client_key: str, limit: int = 120, window_seconds: int = 60):
        now = time.time()
        window_start = now - window_seconds
        self._requests[client_key] = [
            ts for ts in self._requests[client_key] if ts > window_start
        ]
        if len(self._requests[client_key]) >= limit:
            raise RateLimitExceededException(
                f"Rate limit of {limit} requests per {window_seconds}s exceeded."
            )
        self._requests[client_key].append(now)

rate_limiter = InMemoryRateLimiter()
