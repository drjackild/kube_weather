import datetime
import typing as t
from dataclasses import dataclass


class InMemoryCache:
    default_ttl = 600

    @dataclass
    class Entry:
        ts: float
        data: dict

        @property
        def age(self) -> float:
            return datetime.datetime.now().timestamp() - self.ts

    def __init__(self, ttl: t.Optional[int] = None):
        """
        :param ttl: time-to-live in seconds
        """
        self.ttl = ttl or self.default_ttl
        self._cache: t.Dict[str, InMemoryCache.Entry] = {}

    def get(self, key: str) -> dict | None:
        entry = self._cache.get(key)
        if not entry or entry.age > self.ttl:
            if entry:
                del self._cache[key]
            return None
        return entry.data

    def set(self, key: str, data: dict):
        self._cache[key] = self.Entry(datetime.datetime.now().timestamp(), data)


def get_cache() -> InMemoryCache:
    return InMemoryCache()
