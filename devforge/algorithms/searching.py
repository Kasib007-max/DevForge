"""Searching algorithms."""

from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def binary_search(values: Sequence[T], target: T) -> int:
    """Return the index of target in a sorted sequence, or -1 if absent.

    The input must be sorted in ascending order.
    Time complexity: O(log n). Space complexity: O(1).
    """
    left, right = 0, len(values) - 1

    while left <= right:
        middle = left + (right - left) // 2
        current = values[middle]

        if current == target:
            return middle
        if current < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1


def linear_search(values: Sequence[T], target: T) -> int:
    """Return the first matching index, or -1 when target is absent.

    Time complexity: O(n). Space complexity: O(1).
    """
    for index, value in enumerate(values):
        if value == target:
            return index
    return -1
