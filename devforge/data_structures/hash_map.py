"""A generic hash map using separate chaining for collision handling."""

from collections.abc import Iterable, Iterator, MutableMapping
from math import isfinite
from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class HashMap(MutableMapping[K, V], Generic[K, V]):
    """A hash table that resolves collisions with separate chaining.

    Buckets are stored in a power-of-two-sized array. When the load factor
    exceeds `max_load_factor`, the bucket array doubles and existing entries
    are redistributed.

    Expected lookup, insertion, and deletion time is O(1) with well-distributed
    hashes. A single operation can take O(n) in the worst case when many keys
    collide. Iteration order is unspecified.
    """

    DEFAULT_CAPACITY = 8

    def __init__(
        self,
        items: Iterable[tuple[K, V]] = (),
        *,
        initial_capacity: int = DEFAULT_CAPACITY,
        max_load_factor: float = 0.75,
    ) -> None:
        if isinstance(initial_capacity, bool) or not isinstance(initial_capacity, int):
            raise TypeError("initial_capacity must be an integer")
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be at least 1")
        if isinstance(max_load_factor, bool) or not isinstance(max_load_factor, (int, float)):
            raise TypeError("max_load_factor must be a number")
        if not isfinite(max_load_factor) or max_load_factor <= 0:
            raise ValueError("max_load_factor must be a finite number greater than 0")

        capacity = 1
        while capacity < initial_capacity:
            capacity <<= 1

        self._buckets: list[list[tuple[K, V]]] = [[] for _ in range(capacity)]
        self._size = 0
        self._max_load_factor = float(max_load_factor)

        for key, value in items:
            self[key] = value

    @property
    def capacity(self) -> int:
        """Return the current number of buckets."""
        return len(self._buckets)

    @property
    def load_factor(self) -> float:
        """Return the number of stored entries divided by bucket count."""
        return self._size / self.capacity

    def _bucket_index(self, key: K) -> int:
        return hash(key) & (self.capacity - 1)

    def __getitem__(self, key: K) -> V:
        bucket = self._buckets[self._bucket_index(key)]
        for stored_key, value in bucket:
            if stored_key is key or stored_key == key:
                return value
        raise KeyError(key)

    def __setitem__(self, key: K, value: V) -> None:
        bucket = self._buckets[self._bucket_index(key)]
        for index, (stored_key, _) in enumerate(bucket):
            if stored_key is key or stored_key == key:
                bucket[index] = (stored_key, value)
                return

        bucket.append((key, value))
        self._size += 1
        if self.load_factor > self._max_load_factor:
            self._resize(self.capacity * 2)

    def __delitem__(self, key: K) -> None:
        bucket = self._buckets[self._bucket_index(key)]
        for index, (stored_key, _) in enumerate(bucket):
            if stored_key is key or stored_key == key:
                del bucket[index]
                self._size -= 1
                return
        raise KeyError(key)

    def __iter__(self) -> Iterator[K]:
        for bucket in self._buckets:
            for key, _ in bucket:
                yield key

    def __len__(self) -> int:
        return self._size

    def _resize(self, new_capacity: int) -> None:
        old_buckets = self._buckets
        self._buckets = [[] for _ in range(new_capacity)]

        for bucket in old_buckets:
            for key, value in bucket:
                self._buckets[self._bucket_index(key)].append((key, value))

    def clear(self) -> None:
        """Remove all entries while retaining the current bucket capacity."""
        self._buckets = [[] for _ in range(self.capacity)]
        self._size = 0
