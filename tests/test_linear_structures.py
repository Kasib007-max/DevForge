"""Unit tests for the stack and queue implementations."""

import unittest

from devforge.data_structures import EmptyStructureError, Queue, Stack


class StackTests(unittest.TestCase):
    def test_stack_uses_last_in_first_out_order(self) -> None:
        stack = Stack[int]()
        stack.push(10)
        stack.push(20)
        stack.push(30)
        self.assertEqual([stack.pop(), stack.pop(), stack.pop()], [30, 20, 10])

    def test_peek_does_not_remove_item(self) -> None:
        stack = Stack(["first", "top"])
        self.assertEqual(stack.peek(), "top")
        self.assertEqual(len(stack), 2)

    def test_empty_stack_operations_raise_clear_error(self) -> None:
        stack: Stack[int] = Stack()
        with self.assertRaisesRegex(EmptyStructureError, "empty stack"):
            stack.pop()
        with self.assertRaisesRegex(EmptyStructureError, "empty stack"):
            stack.peek()

    def test_stack_initialization_iteration_and_clear(self) -> None:
        stack = Stack([1, 2, 3])
        self.assertEqual(list(stack), [3, 2, 1])
        self.assertFalse(stack.is_empty())
        stack.clear()
        self.assertTrue(stack.is_empty())
        self.assertEqual(len(stack), 0)

    def test_stack_can_store_none(self) -> None:
        stack = Stack([None])
        self.assertIsNone(stack.peek())
        self.assertIsNone(stack.pop())
        self.assertTrue(stack.is_empty())


class QueueTests(unittest.TestCase):
    def test_queue_uses_first_in_first_out_order(self) -> None:
        queue = Queue[str]()
        queue.enqueue("first")
        queue.enqueue("second")
        queue.enqueue("third")
        self.assertEqual(
            [queue.dequeue(), queue.dequeue(), queue.dequeue()],
            ["first", "second", "third"],
        )

    def test_peek_does_not_remove_item(self) -> None:
        queue = Queue(["front", "back"])
        self.assertEqual(queue.peek(), "front")
        self.assertEqual(len(queue), 2)

    def test_empty_queue_operations_raise_clear_error(self) -> None:
        queue: Queue[int] = Queue()
        with self.assertRaisesRegex(EmptyStructureError, "empty queue"):
            queue.dequeue()
        with self.assertRaisesRegex(EmptyStructureError, "empty queue"):
            queue.peek()

    def test_queue_initialization_iteration_and_clear(self) -> None:
        queue = Queue([1, 2, 3])
        self.assertEqual(list(queue), [1, 2, 3])
        self.assertFalse(queue.is_empty())
        queue.clear()
        self.assertTrue(queue.is_empty())
        self.assertEqual(len(queue), 0)

    def test_queue_can_store_none(self) -> None:
        queue = Queue([None])
        self.assertIsNone(queue.peek())
        self.assertIsNone(queue.dequeue())
        self.assertTrue(queue.is_empty())


if __name__ == "__main__":
    unittest.main()
