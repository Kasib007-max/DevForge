"""Binary heap and stable priority queue implementations."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from itertools import count
from typing import Generic, TypeVar

T = TypeVar("T")
P = TypeVar("P")


class BinaryHeap(Generic[T]):
    """Array-backed binary min-heap or max-heap.

    Values must be mutually comparable. Iteration exposes the internal heap
    order, not sorted order.
    """

    def __init__(self, values: Iterable[T] = (), *, min_heap: bool = True) -> None:
        self._items = list(values)
        self._min_heap = min_heap

        # Bottom-up heap construction is O(n), unlike repeated insertion.
        for index in range(len(self._items) // 2 - 1, -1, -1):
            self._sift_down(index)

    def _comes_before(self, left: T, right: T) -> bool:
        return left < right if self._min_heap else left > right

    def _sift_up(self, index: int) -> None:
        while index > 0:
            parent = (index - 1) // 2
            if not self._comes_before(self._items[index], self._items[parent]):
                break
            self._items[index], self._items[parent] = (
                self._items[parent],
                self._items[index],
            )
            index = parent

    def _sift_down(self, index: int) -> None:
        size = len(self._items)
        while True:
            left = 2 * index + 1
            right = left + 1
            best = index

            if left < size and self._comes_before(
                self._items[left], self._items[best]
            ):
                best = left
            if right < size and self._comes_before(
                self._items[right], self._items[best]
            ):
                best = right
            if best == index:
                return

            self._items[index], self._items[best] = (
                self._items[best],
                self._items[index],
            )
            index = best

    def push(self, value: T) -> None:
        """Add a value while preserving the heap property in O(log n)."""
        # Find the insertion path before changing storage. If values are not
        # mutually comparable, the operation raises without corrupting the heap.
        index = len(self._items)
        parents: list[int] = []
        while index > 0:
            parent = (index - 1) // 2
            if not self._comes_before(value, self._items[parent]):
                break
            parents.append(parent)
            index = parent

        self._items.append(value)
        hole = len(self._items) - 1
        for parent in parents:
            self._items[hole] = self._items[parent]
            hole = parent
        self._items[hole] = value

    def peek(self) -> T:
        """Return the root value without removing it."""
        if not self._items:
            raise IndexError("peek from an empty heap")
        return self._items[0]

    def pop(self) -> T:
        """Remove and return the root in O(log n)."""
        if not self._items:
            raise IndexError("pop from an empty heap")

        root = self._items[0]
        last = self._items.pop()
        if self._items:
            self._items[0] = last
            self._sift_down(0)
        return root

    def clear(self) -> None:
        """Remove all values."""
        self._items.clear()

    def is_empty(self) -> bool:
        """Return whether the heap contains no values."""
        return not self._items

    def to_list(self) -> list[T]:
        """Return a copy of the internal heap-order array."""
        return self._items.copy()

    def __len__(self) -> int:
        return len(self._items)

    def __bool__(self) -> bool:
        return bool(self._items)

    def __iter__(self) -> Iterator[T]:
        """Iterate in internal heap order (not sorted order)."""
        return iter(self._items)


class PriorityQueue(Generic[T, P]):
    """Stable min-priority queue; lower priority values leave first.

    Items with equal priorities are dequeued in insertion order. Items
    themselves do not need to be comparable.
    """

    def __init__(self) -> None:
        self._heap: BinaryHeap[tuple[P, int, T]] = BinaryHeap()
        self._sequence = count()

    def enqueue(self, item: T, priority: P) -> None:
        """Add an item with its priority in O(log n)."""
        self._heap.push((priority, next(self._sequence), item))

    def peek(self) -> T:
        """Return the next item without removing it."""
        return self._heap.peek()[2]

    def peek_priority(self) -> P:
        """Return the next item's priority without removing the item."""
        return self._heap.peek()[0]

    def dequeue(self) -> T:
        """Remove and return the next item in O(log n)."""
        return self._heap.pop()[2]

    def clear(self) -> None:
        """Remove all queued items and reset insertion-order tracking."""
        self._heap.clear()
        self._sequence = count()

    def is_empty(self) -> bool:
        """Return whether the queue contains no items."""
        return self._heap.is_empty()

    def __len__(self) -> int:
        return len(self._heap)

    def __bool__(self) -> bool:
        return bool(self._heap)
