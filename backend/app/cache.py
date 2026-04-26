from collections import OrderedDict
from collections.abc import Hashable
from typing import Any


class Cache:
    def __init__(self, capacity: int = 100_000):
        self.capacity = capacity
        self._items: OrderedDict[Hashable, Any] = OrderedDict()

    def get(self, key: Hashable) -> Any | None:
        return self._items.get(key)

    def put(self, key: Hashable, value: Any) -> None:
        if key not in self._items and len(self._items) >= self.capacity:
            self._items.popitem(last=False)
        self._items[key] = value

    def has(self, key: Hashable) -> bool:
        return key in self._items

    def clear(self) -> None:
        self._items.clear()
