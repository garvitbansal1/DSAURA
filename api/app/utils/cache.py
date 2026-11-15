"""
DSAURA In-Memory TTL Cache
Phase 18 Optimization
Caches heavy analytics calculations (Knowledge Graph, Topic Listings, Mastery)
with automatic expiration.
"""

from typing import Any, Optional, Callable
import time
from functools import wraps


class SimpleTTLCache:
    def __init__(self, default_ttl_seconds: int = 60):
        self._cache = {}
        self.default_ttl = default_ttl_seconds

    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            val, expiry = self._cache[key]
            if time.time() < expiry:
                return val
            else:
                del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        expiry = time.time() + (ttl or self.default_ttl)
        self._cache[key] = (value, expiry)

    def invalidate(self, key: str) -> None:
        self._cache.pop(key, None)

    def clear(self) -> None:
        self._cache.clear()


# Global cache instance for high-throughput analytics
analytics_cache = SimpleTTLCache(default_ttl_seconds=30)
