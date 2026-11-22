# Linear Data Structures

DevForge provides two generic linear data structures in
`devforge.data_structures`: a stack and a queue. Both accept an optional
iterable of initial items and work with values of any Python type.

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

## Empty structures

Calling `pop()` or `peek()` on an empty stack, or `dequeue()` or `peek()`
on an empty queue, raises `EmptyStructureError`. It is an `IndexError`
subclass, so callers can catch this specific error or the broader built-in
exception.

```python
from devforge.data_structures import EmptyStructureError, Stack

stack = Stack()
try:
    stack.pop()
except EmptyStructureError as error:
    print(error)
```

## Complexity

| Operation | Stack | Queue |
|---|---:|---:|
| Add item | O(1) amortized | O(1) |
| Remove item | O(1) amortized | O(1) |
| Peek | O(1) | O(1) |
| Check empty / length | O(1) | O(1) |
| Iterate all items | O(n) | O(n) |

The stack uses a Python list, while the queue uses a deque. These are
single-threaded data structures and do not provide synchronization for
concurrent producers or consumers.
