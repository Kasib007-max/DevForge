"""Singly and doubly linked-list implementations."""

from collections.abc import Iterable, Iterator
from typing import Generic, TypeVar

T = TypeVar("T")


class _SinglyNode(Generic[T]):
    __slots__ = ("value", "next")

    def __init__(self, value: T, next_node: "_SinglyNode[T] | None" = None) -> None:
        self.value = value
        self.next = next_node


class SinglyLinkedList(Generic[T]):
    """A singly linked list with O(1) insertion at either end."""

    def __init__(self, items: Iterable[T] = ()) -> None:
        self._head: _SinglyNode[T] | None = None
        self._tail: _SinglyNode[T] | None = None
        self._size = 0
        for item in items:
            self.append(item)

    def append(self, item: T) -> None:
        """Add an item after the tail."""
        node = _SinglyNode(item)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def prepend(self, item: T) -> None:
        """Add an item before the head."""
        self._head = _SinglyNode(item, self._head)
        if self._tail is None:
            self._tail = self._head
        self._size += 1

    def insert(self, index: int, item: T) -> None:
        """Insert before index; valid indexes are 0 through len(self)."""
        if index < 0 or index > self._size:
            raise IndexError("linked-list insertion index out of range")
        if index == 0:
            self.prepend(item)
        elif index == self._size:
            self.append(item)
        else:
            previous = self._head
            for _ in range(index - 1):
                assert previous is not None
                previous = previous.next
            assert previous is not None
            previous.next = _SinglyNode(item, previous.next)
            self._size += 1

    def pop(self, index: int = -1) -> T:
        """Remove and return an item; defaults to the final item."""
        if index < 0:
            index += self._size
        if index < 0 or index >= self._size:
            raise IndexError("linked-list pop index out of range")

        if index == 0:
            assert self._head is not None
            removed = self._head
            self._head = removed.next
            if self._size == 1:
                self._tail = None
        else:
            previous = self._head
            for _ in range(index - 1):
                assert previous is not None
                previous = previous.next
            assert previous is not None and previous.next is not None
            removed = previous.next
            previous.next = removed.next
            if removed is self._tail:
                self._tail = previous

        removed.next = None
        self._size -= 1
        return removed.value

    def remove(self, item: T) -> None:
        """Remove the first equal item, or raise ValueError if absent."""
        previous: _SinglyNode[T] | None = None
        current = self._head
        while current is not None:
            if current.value == item:
                if previous is None:
                    self._head = current.next
                else:
                    previous.next = current.next
                if current is self._tail:
                    self._tail = previous
                current.next = None
                self._size -= 1
                return
            previous, current = current, current.next
        raise ValueError(f"{item!r} is not in the linked list")

    def find(self, item: T) -> int:
        """Return the first matching index, or -1 when absent."""
        for index, value in enumerate(self):
            if value == item:
                return index
        return -1

    def clear(self) -> None:
        """Remove all items and detach the nodes."""
        current = self._head
        while current is not None:
            following = current.next
            current.next = None
            current = following
        self._head = self._tail = None
        self._size = 0

    def is_empty(self) -> bool:
        """Return whether the list contains no items."""
        return self._size == 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        current = self._head
        while current is not None:
            yield current.value
            current = current.next


class _DoublyNode(Generic[T]):
    __slots__ = ("value", "previous", "next")

    def __init__(
        self,
        value: T,
        previous: "_DoublyNode[T] | None" = None,
        next_node: "_DoublyNode[T] | None" = None,
    ) -> None:
        self.value = value
        self.previous = previous
        self.next = next_node


class DoublyLinkedList(Generic[T]):
    """A linked list that supports traversal from either end."""

    def __init__(self, items: Iterable[T] = ()) -> None:
        self._head: _DoublyNode[T] | None = None
        self._tail: _DoublyNode[T] | None = None
        self._size = 0
        for item in items:
            self.append(item)

    def append(self, item: T) -> None:
        """Add an item after the tail."""
        node = _DoublyNode(item, previous=self._tail)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def prepend(self, item: T) -> None:
        """Add an item before the head."""
        node = _DoublyNode(item, next_node=self._head)
        if self._head is None:
            self._head = self._tail = node
        else:
            self._head.previous = node
            self._head = node
        self._size += 1

    def _node_at(self, index: int) -> _DoublyNode[T]:
        """Find a node, starting from whichever endpoint is nearer."""
        if index < self._size // 2:
            current = self._head
            for _ in range(index):
                assert current is not None
                current = current.next
        else:
            current = self._tail
            for _ in range(self._size - index - 1):
                assert current is not None
                current = current.previous
        assert current is not None
        return current

    def insert(self, index: int, item: T) -> None:
        """Insert before index; valid indexes are 0 through len(self)."""
        if index < 0 or index > self._size:
            raise IndexError("linked-list insertion index out of range")
        if index == 0:
            self.prepend(item)
        elif index == self._size:
            self.append(item)
        else:
            following = self._node_at(index)
            previous = following.previous
            assert previous is not None
            node = _DoublyNode(item, previous=previous, next_node=following)
            previous.next = node
            following.previous = node
            self._size += 1

    def pop(self, index: int = -1) -> T:
        """Remove and return an item; defaults to the final item."""
        if index < 0:
            index += self._size
        if index < 0 or index >= self._size:
            raise IndexError("linked-list pop index out of range")

        removed = self._node_at(index)
        previous, following = removed.previous, removed.next
        if previous is None:
            self._head = following
        else:
            previous.next = following
        if following is None:
            self._tail = previous
        else:
            following.previous = previous
        removed.previous = removed.next = None
        self._size -= 1
        return removed.value

    def remove(self, item: T) -> None:
        """Remove the first equal item, or raise ValueError if absent."""
        current = self._head
        while current is not None:
            if current.value == item:
                previous, following = current.previous, current.next
                if previous is None:
                    self._head = following
                else:
                    previous.next = following
                if following is None:
                    self._tail = previous
                else:
                    following.previous = previous
                current.previous = current.next = None
                self._size -= 1
                return
            current = current.next
        raise ValueError(f"{item!r} is not in the linked list")

    def find(self, item: T) -> int:
        """Return the first matching index, or -1 when absent."""
        for index, value in enumerate(self):
            if value == item:
                return index
        return -1

    def clear(self) -> None:
        """Remove all items and detach the nodes."""
        current = self._head
        while current is not None:
            following = current.next
            current.previous = current.next = None
            current = following
        self._head = self._tail = None
        self._size = 0

    def is_empty(self) -> bool:
        """Return whether the list contains no items."""
        return self._size == 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[T]:
        current = self._head
        while current is not None:
            yield current.value
            current = current.next

    def __reversed__(self) -> Iterator[T]:
        current = self._tail
        while current is not None:
            yield current.value
            current = current.previous
