"""Tests for the binary search tree."""

import unittest

from devforge.data_structures import BinarySearchTree


class BinarySearchTreeTests(unittest.TestCase):
    def test_empty_tree(self) -> None:
        tree = BinarySearchTree[int]()
        self.assertEqual(len(tree), 0)
        self.assertEqual(tree.height, 0)
        self.assertTrue(tree.is_empty())
        self.assertEqual(list(tree), [])
        self.assertEqual(list(tree.preorder()), [])
        self.assertEqual(list(tree.postorder()), [])

    def test_constructor_and_inorder_iteration(self) -> None:
        tree = BinarySearchTree([8, 3, 10, 1, 6, 14, 4, 7, 13])
        self.assertEqual(list(tree), [1, 3, 4, 6, 7, 8, 10, 13, 14])
        self.assertEqual(len(tree), 9)

    def test_insert_returns_false_for_duplicates(self) -> None:
        tree = BinarySearchTree([5, 3, 7])
        self.assertFalse(tree.insert(3))
        self.assertEqual(len(tree), 3)
        self.assertEqual(list(tree), [3, 5, 7])

    def test_search_and_membership(self) -> None:
        tree = BinarySearchTree([8, 3, 10, 1, 6])
        self.assertTrue(tree.search(6))
        self.assertIn(8, tree)
        self.assertNotIn(99, tree)
        self.assertNotIn("not comparable", tree)

    def test_traversal_orders(self) -> None:
        tree = BinarySearchTree([8, 3, 10, 1, 6, 14, 4, 7, 13])
        self.assertEqual(list(tree.inorder()), [1, 3, 4, 6, 7, 8, 10, 13, 14])
        self.assertEqual(list(tree.preorder()), [8, 3, 1, 6, 4, 7, 10, 14, 13])
        self.assertEqual(list(tree.postorder()), [1, 4, 7, 6, 3, 13, 14, 10, 8])

    def test_height_is_measured_in_nodes(self) -> None:
        tree = BinarySearchTree([8, 3, 10, 1, 6, 14, 4, 7, 13])
        self.assertEqual(tree.height, 4)
        tree.clear()
        tree.insert(42)
        self.assertEqual(tree.height, 1)

    def test_remove_leaf(self) -> None:
        tree = BinarySearchTree([8, 3, 10, 1])
        self.assertTrue(tree.remove(1))
        self.assertEqual(list(tree), [3, 8, 10])
        self.assertEqual(len(tree), 3)

    def test_remove_node_with_only_left_child(self) -> None:
        tree = BinarySearchTree([8, 3, 10, 1])
        self.assertTrue(tree.remove(3))
        self.assertEqual(list(tree), [1, 8, 10])

    def test_remove_node_with_only_right_child(self) -> None:
        tree = BinarySearchTree([8, 3, 10, 14])
        self.assertTrue(tree.remove(10))
        self.assertEqual(list(tree), [3, 8, 14])

    def test_remove_node_with_two_children(self) -> None:
        tree = BinarySearchTree([8, 3, 10, 1, 6, 14, 4, 7, 13])
        self.assertTrue(tree.remove(3))
        self.assertEqual(list(tree), [1, 4, 6, 7, 8, 10, 13, 14])
        self.assertEqual(len(tree), 8)

    def test_two_child_removal_relinks_successor_right_child(self) -> None:
        tree = BinarySearchTree([50, 30, 70, 60, 80, 65])
        self.assertTrue(tree.remove(50))
        self.assertEqual(list(tree), [30, 60, 65, 70, 80])
        self.assertEqual(len(tree), 5)

    def test_remove_root_with_one_child(self) -> None:
        tree = BinarySearchTree([8, 3, 1])
        self.assertTrue(tree.remove(8))
        self.assertEqual(list(tree), [1, 3])
        self.assertEqual(tree.height, 2)

    def test_remove_last_node(self) -> None:
        tree = BinarySearchTree([42])
        self.assertTrue(tree.remove(42))
        self.assertTrue(tree.is_empty())
        self.assertEqual(tree.height, 0)

    def test_remove_missing_value_is_safe(self) -> None:
        tree = BinarySearchTree([2, 1, 3])
        self.assertFalse(tree.remove(99))
        self.assertEqual(list(tree), [1, 2, 3])
        self.assertEqual(len(tree), 3)

    def test_clear_resets_tree(self) -> None:
        tree = BinarySearchTree([4, 2, 6])
        tree.clear()
        self.assertTrue(tree.is_empty())
        self.assertEqual(len(tree), 0)
        self.assertEqual(tree.height, 0)

    def test_skewed_tree_traversal_does_not_use_recursion(self) -> None:
        tree = BinarySearchTree(range(1500))
        self.assertEqual(tree.height, 1500)
        self.assertEqual(list(tree), list(range(1500)))
        self.assertEqual(len(list(tree.preorder())), 1500)
        self.assertEqual(len(list(tree.postorder())), 1500)


if __name__ == "__main__":
    unittest.main()
