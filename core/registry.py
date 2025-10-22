from typing import Dict, Any

class Registry:
    """Lightweight service registry for shared state or handles."""
    def __init__(self) -> None:
        self._store: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value

    def get(self, key: str, default=None):
        return self._store.get(key, default)
