# Data Structures

DevForge provides generic linear data structures in `devforge.data_structures`:
a stack, a queue, a singly linked list, and a doubly linked list. Each accepts
an optional iterable of initial items.

## Stack (LIFO)

A stack follows **last in, first out**. The most recently added item is removed
first. It is useful for undo history, expression evaluation, and depth-first
search.

```python
from devforge.data_structures import Stack

history = Stack(["open", "edit"])
history.push("save")

print(history.peek())  # save
print(history.pop())   # save
print(len(history))    # 2
```

- `push(item)`: add an item to the top.
- `pop()`: remove and return the top item.
- `peek()`: inspect the top item without removing it.
- `is_empty()`, `clear()`, and `len(stack)`: inspect or reset the stack.

Iteration visits the top item first.

## Queue (FIFO)

A queue follows **first in, first out**. The earliest added item is removed
first. It is useful for task scheduling, printer jobs, and breadth-first search.

```python
from devforge.data_structures import Queue

jobs = Queue(["report.pdf", "notes.txt"])
jobs.enqueue("slides.pptx")

print(jobs.peek())     # report.pdf
print(jobs.dequeue())  # report.pdf
print(list(jobs))      # ['notes.txt', 'slides.pptx']
```

- `enqueue(item)`: add an item to the back.
- `dequeue()`: remove and return the front item.
- `peek()`: inspect the front item without removing it.
- `is_empty()`, `clear()`, and `len(queue)`: inspect or reset the queue.

Iteration visits items from front to back. The queue uses Python's
`collections.deque`, avoiding the costly front-removal behavior of a list.

## Singly linked list

A singly linked list stores each value in a node that points to the next node.
It keeps references to both its head and tail, so adding at either end is O(1).

```python
from devforge.data_structures import SinglyLinkedList

tasks = SinglyLinkedList(["plan", "build"])
tasks.prepend("design")
tasks.insert(2, "test")

print(list(tasks))  # ['design', 'plan', 'test', 'build']
print(tasks.pop())  # build
tasks.remove("plan")
print(tasks.find("test"))  # 1
```

- `append(item)` / `prepend(item)`: add at the tail / head.
- `insert(index, item)`: insert before an index from 0 through the list length.
- `pop(index=-1)`: remove and return an item; negative indexes are supported.
- `remove(item)`: remove the first equal value, raising `ValueError` if absent.
- `find(item)`: return the first matching index, or -1.
- `clear()`, `is_empty()`, iteration, and `len(list)` are also supported.

Iteration follows head-to-tail order. The structure uses O(n) additional memory
for n nodes; it does not provide constant-time random access.

## Doubly linked list

A doubly linked list stores both a next and previous reference in every node.
This allows traversal from either end and efficient removal of a known endpoint.

```python
from devforge.data_structures import DoublyLinkedList

history = DoublyLinkedList(["one", "two", "three"])
history.prepend("zero")
history.append("four")

print(list(history))            # ['zero', 'one', 'two', 'three', 'four']
print(list(reversed(history)))  # ['four', 'three', 'two', 'one', 'zero']
print(history.pop())            # four
```

It supports the same insertion, removal, search, clearing, length, and
iteration methods as `SinglyLinkedList`. Normal iteration moves from head to
tail; `reversed(values)` moves from tail to head. Indexed traversal starts at
the nearer endpoint.

## Empty structures and index rules

Calling `pop()` on an empty linked list raises `IndexError`. Calling
`remove(item)` for a missing value raises `ValueError`. The `insert`
method accepts only indexes from 0 through the current length; `pop` accepts
negative indexes like Python sequences.

Stack and queue operations on empty structures raise `EmptyStructureError`,
an `IndexError` subclass.

## Complexity

| Operation | Stack | Queue | Singly linked | Doubly linked |
|---|---:|---:|---:|---:|
| Add at front | O(1) | — | O(1) | O(1) |
| Add at back | O(1) amortized | O(1) | O(1) | O(1) |
| Remove front | — | O(1) | O(1) | O(1) |
| Remove back | O(1) amortized | — | O(n) | O(1) |
| Insert / remove by index | — | — | O(n) | O(n) |
| Scan / iterate | O(n) | O(n) | O(n) | O(n) |
| Peek | O(1) | O(1) | O(1) at head | O(1) at head |
| Length / empty check | O(1) | O(1) | O(1) | O(1) |

The stack uses a Python list and the queue uses a deque. The linked lists use
explicit node objects. These structures are single-threaded and do not provide
synchronization for concurrent producers or consumers.

## Related structures

- [Hash Map](HASH_MAP.md) — key-value storage with separate chaining.
- [Binary Search Tree](BINARY_SEARCH_TREE.md) — ordered values, search, deletion,
  and inorder, preorder, and postorder traversal.
