# Binary Heap and Priority Queue

DevForge provides an array-backed `BinaryHeap` and a stable min-priority
queue in `devforge.data_structures`. Both use the heap property to keep the
next value at the root.

## Binary heap

A binary heap is a complete binary tree represented in a Python list. For an
element at index `i`, its children are at `2 * i + 1` and `2 * i + 2`,
and its parent is at `(i - 1) // 2`.

A min-heap keeps the smallest value at the root. A max-heap keeps the largest.

```python
from devforge.data_structures import BinaryHeap

minimums = BinaryHeap([8, 3, 7, 1, 9, 2])
print(minimums.peek())  # 1
minimums.push(0)
print(minimums.pop())   # 0

maximums = BinaryHeap([8, 3, 7, 1, 9, 2], min_heap=False)
print(maximums.pop())   # 9
```

The constructor accepts any iterable and builds the heap bottom-up in O(n)
time. Values must be mutually comparable. Iteration and `to_list()` expose
the internal heap order, which is not a sorted sequence; repeatedly calling
`pop()` produces sorted order.

## Stable priority queue

A priority queue removes the item with the lowest numeric or otherwise
comparable priority first. When two items have equal priorities, DevForge
preserves their insertion order. The items themselves do not need to be
comparable.

```python
from devforge.data_structures import PriorityQueue

jobs = PriorityQueue[str, int]()
jobs.enqueue("weekly report", priority=5)
jobs.enqueue("database backup", priority=2)
jobs.enqueue("security alert", priority=1)

print(jobs.peek())          # security alert
print(jobs.peek_priority()) # 1
print(jobs.dequeue())       # security alert
print(jobs.dequeue())       # database backup
```

This is useful for job scheduling, event simulation, and choosing the next
task by urgency. Lower values mean higher priority.

## API and empty behavior

| Class | Method | Behavior |
|---|---|---|
| `BinaryHeap` | `push(value)` | Insert a value |
| `BinaryHeap` | `peek()` | Inspect the root |
| `BinaryHeap` | `pop()` | Remove and return the root |
| `BinaryHeap` | `clear()` | Remove all values |
| `PriorityQueue` | `enqueue(item, priority)` | Add an item |
| `PriorityQueue` | `peek()` | Inspect the next item |
| `PriorityQueue` | `peek_priority()` | Inspect the next priority |
| `PriorityQueue` | `dequeue()` | Remove and return the next item |
| Both | `is_empty()`, `len(...)`, truthiness | Inspect queue state |

Calling `peek()`, `peek_priority()`, or `pop()` / `dequeue()` on an
empty structure raises `IndexError`. `clear()` leaves the structure ready
for reuse.

## Complexity

Let n be the number of stored values.

| Operation | Binary heap | Priority queue |
|---|---:|---:|
| Build from iterable | O(n) | — |
| Insert / enqueue | O(log n) | O(log n) |
| Peek | O(1) | O(1) |
| Remove next / pop | O(log n) | O(log n) |
| Clear | O(n) | O(n) |
| Length / empty check | O(1) | O(1) |

The heap uses O(n) storage. Heap operations are not synchronized for
concurrent access.
