"""Sorting algorithms implemented for clarity and reuse."""

from collections.abc import MutableSequence
from typing import TypeVar

T = TypeVar("T")


def merge_sort(values: MutableSequence[T]) -> MutableSequence[T]:
    """Sort values in place using merge sort and return the same sequence.

    Time complexity: O(n log n). Auxiliary space: O(n).
    The algorithm is stable: equal elements retain their relative order.
    """
    if len(values) < 2:
        return values

    middle = len(values) // 2
    left = list(values[:middle])
    right = list(values[middle:])
    merge_sort(left)
    merge_sort(right)

    i = j = k = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            values[k] = left[i]
            i += 1
        else:
            values[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        values[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        values[k] = right[j]
        j += 1
        k += 1

    return values
