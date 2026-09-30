import time
from typing import Any


class SimpleCache:
    def __init__(self):
        self.store = {}

    def get(self, key: str) -> Any | None:
        if key in self.store:
            entry = self.store[key]
            if time.time() < entry["expiry"]:
                return entry["value"]
            else:
                del self.store[key]
        return None

    def set(self, key: str, value: Any, ttl_seconds: int):
        self.store[key] = {"value": value, "expiry": time.time() + ttl_seconds}


cache = SimpleCache()
