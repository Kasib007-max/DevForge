"""An unbalanced binary search tree with iterative operations and traversals."""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class _Node(Generic[T]):
    """Internal tree node."""

    value: T
    left: _Node[T] | None = None
    right: _Node[T] | None = None


class BinarySearchTree(Generic[T]):
    """Store unique, mutually comparable values in sorted tree order.

    Values smaller than a node go left; larger values go right. Duplicate
    values are ignored by :meth:`insert`. This implementation is not
    self-balancing, so insert, search, and remove are O(h), where h is the
    tree height (O(log n) for a balanced tree and O(n) in the worst case).

    Traversals are iterative, avoiding Python recursion limits on skewed trees.
    """

    def __init__(self, values: Iterable[T] = ()) -> None:
        self._root: _Node[T] | None = None
        self._size = 0
        for value in values:
            self.insert(value)

    def insert(self, value: T) -> bool:
        """Insert *value*; return False when an equal value already exists."""
        new_node = _Node(value)
        if self._root is None:
            self._root = new_node
            self._size = 1
            return True

        current = self._root
        while True:
            if value == current.value:
                return False
            if value < current.value:
                if current.left is None:
                    current.left = new_node
                    self._size += 1
                    return True
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    self._size += 1
                    return True
                current = current.right

    def _find_node(self, value: T) -> _Node[T] | None:
        current = self._root
        while current is not None:
            if value == current.value:
                return current
            current = current.left if value < current.value else current.right
        return None

    def search(self, value: T) -> bool:
        """Return whether *value* is present in the tree."""
        return self._find_node(value) is not None

    def __contains__(self, value: object) -> bool:
        try:
            return self.search(value)  # type: ignore[arg-type]
        except TypeError:
            return False

    def remove(self, value: T) -> bool:
        """Remove *value* and return True; return False when it is absent.

        A node with two children is replaced by its inorder successor (the
        smallest value in its right subtree).
        """
        parent: _Node[T] | None = None
        node = self._root

        while node is not None and node.value != value:
            parent = node
            node = node.left if value < node.value else node.right

        if node is None:
            return False

        if node.left is not None and node.right is not None:
            successor_parent = node
            successor = node.right
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left

            node.value = successor.value
            parent = successor_parent
            node = successor

        child = node.left if node.left is not None else node.right
        if parent is None:
            self._root = child
        elif parent.left is node:
            parent.left = child
        else:
            parent.right = child

        self._size -= 1
        return True

    def inorder(self) -> Iterator[T]:
        """Yield values from smallest to largest."""
        stack: list[_Node[T]] = []
        current = self._root
        while current is not None or stack:
            while current is not None:
                stack.append(current)
                current = current.left
            current = stack.pop()
            yield current.value
            current = current.right

    def preorder(self) -> Iterator[T]:
        """Yield the root, then the left and right subtrees."""
        if self._root is None:
            return
        stack = [self._root]
        while stack:
            node = stack.pop()
            yield node.value
            if node.right is not None:
                stack.append(node.right)
            if node.left is not None:
                stack.append(node.left)

    def postorder(self) -> Iterator[T]:
        """Yield the left and right subtrees before the root."""
        if self._root is None:
            return
        stack: list[tuple[_Node[T], bool]] = [(self._root, False)]
        while stack:
            node, visited = stack.pop()
            if visited:
                yield node.value
                continue
            stack.append((node, True))
            if node.right is not None:
                stack.append((node.right, False))
            if node.left is not None:
                stack.append((node.left, False))

    @property
    def height(self) -> int:
        """Return tree height measured in nodes; an empty tree has height 0."""
        if self._root is None:
            return 0

        height = 0
        level = deque([self._root])
        while level:
            height += 1
            for _ in range(len(level)):
                node = level.popleft()
                if node.left is not None:
                    level.append(node.left)
                if node.right is not None:
                    level.append(node.right)
        return height

    def clear(self) -> None:
        """Remove all values from the tree."""
        self._root = None
        self._size = 0

    def is_empty(self) -> bool:
        """Return whether the tree contains no values."""
        return self._size == 0

    def __iter__(self) -> Iterator[T]:
        """Iterate over values in ascending order."""
        return self.inorder()

    def __len__(self) -> int:
        return self._size
