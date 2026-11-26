"""Tests for binary heaps and the stable priority queue."""

import unittest

from devforge.data_structures import BinaryHeap, PriorityQueue


class BinaryHeapTests(unittest.TestCase):
    def test_min_heap_heapifies_and_pops_in_ascending_order(self) -> None:
        heap = BinaryHeap([8, 3, 7, 1, 9, 2])
        self.assertEqual([heap.pop() for _ in range(len(heap))], [1, 2, 3, 7, 8, 9])

    def test_max_heap_pops_in_descending_order(self) -> None:
        heap = BinaryHeap([8, 3, 7, 1, 9, 2], min_heap=False)
        self.assertEqual([heap.pop() for _ in range(len(heap))], [9, 8, 7, 3, 2, 1])

    def test_push_and_peek(self) -> None:
        heap = BinaryHeap[int]()
        heap.push(5)
        heap.push(2)
        heap.push(4)
        self.assertEqual(heap.peek(), 2)
        self.assertEqual(len(heap), 3)

    def test_duplicate_values_are_preserved(self) -> None:
        heap = BinaryHeap([4, 1, 4, 1, 2])
        self.assertEqual([heap.pop() for _ in range(5)], [1, 1, 2, 4, 4])

    def test_empty_peek_and_pop_raise_index_error(self) -> None:
        heap = BinaryHeap[int]()
        with self.assertRaises(IndexError):
            heap.peek()
        with self.assertRaises(IndexError):
            heap.pop()

    def test_clear_and_truthiness(self) -> None:
        heap = BinaryHeap([2, 1])
        self.assertTrue(heap)
        heap.clear()
        self.assertFalse(heap)
        self.assertTrue(heap.is_empty())
        self.assertEqual(heap.to_list(), [])

    def test_constructor_accepts_generator(self) -> None:
        heap = BinaryHeap(number for number in [5, 2, 6, 1])
        self.assertEqual([heap.pop() for _ in range(4)], [1, 2, 5, 6])

    def test_iteration_and_to_list_do_not_expose_mutable_storage(self) -> None:
        heap = BinaryHeap([3, 1, 2])
        snapshot = heap.to_list()
        snapshot.clear()
        self.assertEqual(len(list(heap)), 3)
        self.assertEqual(len(heap), 3)

    def test_incomparable_push_does_not_corrupt_existing_heap(self) -> None:
        heap = BinaryHeap([1, 2, 3])
        with self.assertRaises(TypeError):
            heap.push("not an integer")
        self.assertEqual([heap.pop(), heap.pop(), heap.pop()], [1, 2, 3])


class PriorityQueueTests(unittest.TestCase):
    def test_dequeues_lowest_priority_first(self) -> None:
        queue = PriorityQueue[str, int]()
        queue.enqueue("low urgency", 10)
        queue.enqueue("urgent", 1)
        queue.enqueue("normal", 5)
        self.assertEqual(
            [queue.dequeue(), queue.dequeue(), queue.dequeue()],
            ["urgent", "normal", "low urgency"],
        )

    def test_equal_priorities_are_stable(self) -> None:
        queue = PriorityQueue[str, int]()
        queue.enqueue("first", 2)
        queue.enqueue("second", 2)
        queue.enqueue("third", 2)
        self.assertEqual(
            [queue.dequeue(), queue.dequeue(), queue.dequeue()],
            ["first", "second", "third"],
        )

    def test_items_do_not_need_to_be_comparable(self) -> None:
        class Job:
            pass

        first, second = Job(), Job()
        queue = PriorityQueue[Job, int]()
        queue.enqueue(first, 1)
        queue.enqueue(second, 1)
        self.assertIs(queue.dequeue(), first)
        self.assertIs(queue.dequeue(), second)

    def test_peek_does_not_remove_and_exposes_priority(self) -> None:
        queue = PriorityQueue[str, int]()
        queue.enqueue("backup", 4)
        queue.enqueue("primary", 1)
        self.assertEqual(queue.peek(), "primary")
        self.assertEqual(queue.peek_priority(), 1)
        self.assertEqual(len(queue), 2)

    def test_empty_operations_raise_index_error(self) -> None:
        queue = PriorityQueue[str, int]()
        with self.assertRaises(IndexError):
            queue.peek()
        with self.assertRaises(IndexError):
            queue.peek_priority()
        with self.assertRaises(IndexError):
            queue.dequeue()

    def test_clear_resets_queue(self) -> None:
        queue = PriorityQueue[str, int]()
        queue.enqueue("task", 1)
        queue.clear()
        self.assertTrue(queue.is_empty())
        self.assertFalse(queue)
        self.assertEqual(len(queue), 0)

    def test_negative_and_zero_priorities(self) -> None:
        queue = PriorityQueue[str, int]()
        queue.enqueue("zero", 0)
        queue.enqueue("negative", -3)
        queue.enqueue("positive", 2)
        self.assertEqual(
            [queue.dequeue(), queue.dequeue(), queue.dequeue()],
            ["negative", "zero", "positive"],
        )


if __name__ == "__main__":
    unittest.main()
