"""Unit tests for DevForge algorithms."""

import unittest

from devforge.algorithms.searching import binary_search, linear_search
from devforge.algorithms.sorting import merge_sort


class SearchTests(unittest.TestCase):
    def test_binary_search_finds_first_middle_and_last(self) -> None:
        values = [2, 4, 6, 8, 10]
        self.assertEqual(binary_search(values, 2), 0)
        self.assertEqual(binary_search(values, 6), 2)
        self.assertEqual(binary_search(values, 10), 4)

    def test_binary_search_missing_and_empty(self) -> None:
        self.assertEqual(binary_search([1, 3, 5], 4), -1)
        self.assertEqual(binary_search([], 1), -1)

    def test_linear_search_returns_first_duplicate(self) -> None:
        self.assertEqual(linear_search([3, 5, 5, 7], 5), 1)

    def test_linear_search_missing(self) -> None:
        self.assertEqual(linear_search([1, 2], 9), -1)


class SortingTests(unittest.TestCase):
    def test_merge_sort_mixed_values(self) -> None:
        values = [8, 3, 7, 4, 9, 2, 6, 5, 1]
        result = merge_sort(values)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertIs(result, values)

    def test_merge_sort_empty_and_singleton(self) -> None:
        self.assertEqual(merge_sort([]), [])
        self.assertEqual(merge_sort([42]), [42])

    def test_merge_sort_duplicates_and_negatives(self) -> None:
        self.assertEqual(merge_sort([0, -2, 5, -2, 0]), [-2, -2, 0, 0, 5])


if __name__ == "__main__":
    unittest.main()
