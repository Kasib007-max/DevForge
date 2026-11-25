# Binary Search Tree

DevForge's `BinarySearchTree` stores unique values in a binary search tree
(BST). Every value in a node's left subtree is smaller than the node, and
every value in its right subtree is larger. Values must be mutually
comparable.

## Quick start

```python
from devforge.data_structures import BinarySearchTree

numbers = BinarySearchTree([8, 3, 10, 1, 6, 14, 4, 7, 13])

numbers.insert(5)
print(numbers.search(6))  # True
print(list(numbers))      # [1, 3, 4, 5, 6, 7, 8, 10, 13, 14]

numbers.remove(3)
print(list(numbers))      # [1, 4, 5, 6, 7, 8, 10, 13, 14]
print(numbers.height)     # 4
```

## Operations

- `insert(value)`: add a value and return `True`; return `False` for a
  duplicate. Duplicate values are not stored.
- `search(value)`: return whether a value exists.
- `value in tree`: membership check, equivalent to `search`.
- `remove(value)`: remove a value and return `True`; return `False` if it
  is absent.
- `inorder()`: yield values in ascending order.
- `preorder()`: yield the root before its subtrees.
- `postorder()`: yield the subtrees before the root.
- `height`: return the number of node levels (empty tree: 0, leaf: 1).
- `clear()`, `is_empty()`, and `len(tree)`: reset or inspect the tree.

Normal iteration (`for value in tree`) uses inorder traversal, so values are
visited from smallest to largest.

## How deletion works

Deletion has three cases:

1. **Leaf:** unlink the node from its parent.
2. **One child:** connect the parent directly to the node's only child.
3. **Two children:** copy the smallest value from the right subtree (the
   inorder successor), then unlink the successor from its original position.

The third case preserves the BST ordering rule. The implementation also
reconnects the successor's right child when one exists.

## Complexity

Let `n` be the number of values and `h` the tree height.

| Operation | Time |
|---|---:|
| Insert | O(h) |
| Search / membership | O(h) |
| Remove | O(h) |
| Inorder / preorder / postorder traversal | O(n) |
| Height calculation | O(n) |
| Length / empty check | O(1) |

A balanced tree has height O(log n), making search, insertion, and deletion
O(log n). This implementation does **not** rebalance itself: inserting already
sorted values can create a chain with height O(n), making those operations
O(n). Traversals are iterative, so even a highly skewed tree does not consume
the Python call stack.

## Scope

This is an educational, unbalanced BST. It does not support duplicate values,
custom comparators, or automatic balancing (AVL / red-black rotations).
