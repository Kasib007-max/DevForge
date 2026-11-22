"""Array-backed stack and deque-backed queue implementations."""

from collections import deque
from collections.abc import Iterable, Iterator
from typing import Generic, TypeVar

T = TypeVar("T")


class EmptyStructureError(IndexError):
    """Raised when an item is requested from an empty data structure."""


class Stack(Generic[T]):
    """A last-in, first-out (LIFO) collection.

    Iteration visits the top item first. Appending and removing the top item
    are amortized O(1) operations.
    """

    def __init__(self, items: Iterable[T] = ()) -> None:
        self._items = list(items)

    def push(self, item: T) -> None:
        """Add an item to the top of the stack."""
        self._items.append(item)

    def pop(self) -> T:
        """Remove and return the top item, raising if the stack is empty."""
        if self.is_empty():
            raise EmptyStructureError("cannot pop from an empty stack")
        return self._items.pop()

    def peek(self) -> T:
        """Return the top item without removing it."""
        if self.is_empty():
            raise EmptyStructureError("cannot peek at an empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Return whether the stack contains no items."""
        return not self._items

    def clear(self) -> None:
        """Remove every item from the stack."""
        self._items.clear()

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[T]:
        return reversed(self._items)


class Queue(Generic[T]):
    """A first-in, first-out (FIFO) collection backed by deque.

    Iteration visits the front item first. Enqueueing and dequeueing are
    approximately O(1) operations at either end of the deque.
    """

    def __init__(self, items: Iterable[T] = ()) -> None:
        self._items: deque[T] = deque(items)

    def enqueue(self, item: T) -> None:
        """Add an item to the back of the queue."""
        self._items.append(item)

    def dequeue(self) -> T:
        """Remove and return the front item, raising if the queue is empty."""
        if self.is_empty():
            raise EmptyStructureError("cannot dequeue from an empty queue")
        return self._items.popleft()

    def peek(self) -> T:
        """Return the front item without removing it."""
        if self.is_empty():
            raise EmptyStructureError("cannot peek at an empty queue")
        return self._items[0]

    def is_empty(self) -> bool:
        """Return whether the queue contains no items."""
        return not self._items

    def clear(self) -> None:
        """Remove every item from the queue."""
        self._items.clear()

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)
