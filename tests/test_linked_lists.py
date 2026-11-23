"""Tests for singly and doubly linked lists."""

import unittest

from devforge.data_structures import DoublyLinkedList, SinglyLinkedList


class SinglyLinkedListTests(unittest.TestCase):
    def test_build_append_prepend_and_iteration(self):
        values = SinglyLinkedList([2, 3])
        values.prepend(1)
        values.append(4)
        self.assertEqual(list(values), [1, 2, 3, 4])
        self.assertEqual(len(values), 4)

    def test_insert_at_start_middle_and_end(self):
        values = SinglyLinkedList([1, 3])
        values.insert(0, 0)
        values.insert(2, 2)
        values.insert(len(values), 4)
        self.assertEqual(list(values), [0, 1, 2, 3, 4])

    def test_insert_rejects_invalid_indexes(self):
        values = SinglyLinkedList([1])
        for index in (-1, 2):
            with self.subTest(index=index), self.assertRaises(IndexError):
                values.insert(index, 9)

    def test_pop_supports_positive_negative_and_default_indexes(self):
        values = SinglyLinkedList([10, 20, 30, 40])
        self.assertEqual(values.pop(1), 20)
        self.assertEqual(values.pop(-2), 30)
        self.assertEqual(values.pop(), 40)
        self.assertEqual(values.pop(0), 10)
        self.assertTrue(values.is_empty())

    def test_pop_rejects_out_of_range_indexes(self):
        values = SinglyLinkedList()
        with self.assertRaises(IndexError):
            values.pop()
        values.append(1)
        for index in (-2, 1):
            with self.subTest(index=index), self.assertRaises(IndexError):
                values.pop(index)

    def test_remove_first_match_and_find(self):
        values = SinglyLinkedList([4, 2, 4, 6])
        self.assertEqual(values.find(4), 0)
        values.remove(4)
        self.assertEqual(list(values), [2, 4, 6])
        self.assertEqual(values.find(4), 1)
        self.assertEqual(values.find(99), -1)

    def test_remove_missing_value_raises(self):
        with self.assertRaises(ValueError):
            SinglyLinkedList([1, 2]).remove(3)

    def test_clear_and_none_values(self):
        values = SinglyLinkedList([None, 1])
        values.clear()
        self.assertEqual(len(values), 0)
        self.assertEqual(list(values), [])
        values.append(None)
        self.assertEqual(list(values), [None])


class DoublyLinkedListTests(unittest.TestCase):
    def test_build_append_prepend_and_bidirectional_iteration(self):
        values = DoublyLinkedList([2, 3])
        values.prepend(1)
        values.append(4)
        self.assertEqual(list(values), [1, 2, 3, 4])
        self.assertEqual(list(reversed(values)), [4, 3, 2, 1])

    def test_insert_at_start_middle_and_end(self):
        values = DoublyLinkedList([1, 3])
        values.insert(0, 0)
        values.insert(2, 2)
        values.insert(len(values), 4)
        self.assertEqual(list(values), [0, 1, 2, 3, 4])
        self.assertEqual(list(reversed(values)), [4, 3, 2, 1, 0])

    def test_insert_rejects_invalid_indexes(self):
        values = DoublyLinkedList([1])
        for index in (-1, 2):
            with self.subTest(index=index), self.assertRaises(IndexError):
                values.insert(index, 9)

    def test_pop_supports_positive_negative_and_default_indexes(self):
        values = DoublyLinkedList([10, 20, 30, 40])
        self.assertEqual(values.pop(1), 20)
        self.assertEqual(values.pop(-2), 30)
        self.assertEqual(values.pop(), 40)
        self.assertEqual(values.pop(0), 10)
        self.assertTrue(values.is_empty())

    def test_pop_rejects_out_of_range_indexes(self):
        values = DoublyLinkedList()
        with self.assertRaises(IndexError):
            values.pop()
        values.append(1)
        for index in (-2, 1):
            with self.subTest(index=index), self.assertRaises(IndexError):
                values.pop(index)

    def test_remove_first_match_and_find(self):
        values = DoublyLinkedList([4, 2, 4, 6])
        self.assertEqual(values.find(4), 0)
        values.remove(4)
        self.assertEqual(list(values), [2, 4, 6])
        self.assertEqual(list(reversed(values)), [6, 4, 2])
        self.assertEqual(values.find(4), 1)
        self.assertEqual(values.find(99), -1)

    def test_remove_missing_value_raises(self):
        with self.assertRaises(ValueError):
            DoublyLinkedList([1, 2]).remove(3)

    def test_clear_and_none_values(self):
        values = DoublyLinkedList([None, 1])
        values.clear()
        self.assertEqual(len(values), 0)
        self.assertEqual(list(values), [])
        values.append(None)
        self.assertEqual(list(values), [None])


if __name__ == "__main__":
    unittest.main()
