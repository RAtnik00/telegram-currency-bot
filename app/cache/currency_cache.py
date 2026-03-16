import time


class CurrencyCache:
    def __init__(self, ttl_seconds: int = 300) -> None:
        self._ttl_seconds = ttl_seconds
        self._storage: dict[str, tuple[float, dict[str, float]]] = {}

    def get(self, key: str) -> dict[str, float] | None:
        cached_item = self._storage.get(key)
        if cached_item is None:
            return None

        expires_at, value = cached_item

        if time.time() > expires_at:
            self._storage.pop(key, None)
            return None

        return value

    def set(self, key: str, value: dict[str, float]) -> None:
        expires_at = time.time() + self._ttl_seconds
        self._storage[key] = (expires_at, value)

    def clear(self) -> None:
        self._storage.clear()