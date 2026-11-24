"""Data structures for DevForge."""

from devforge.data_structures.hash_map import HashMap
from devforge.data_structures.linear import EmptyStructureError, Queue, Stack
from devforge.data_structures.linked import DoublyLinkedList, SinglyLinkedList

__all__ = [
    "DoublyLinkedList",
    "EmptyStructureError",
    "HashMap",
    "Queue",
    "SinglyLinkedList",
    "Stack",
]
